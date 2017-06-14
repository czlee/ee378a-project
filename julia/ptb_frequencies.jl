# Compile table of n-frequencies from Penn Treebank data.
#
# Chuan-Zheng Lee
# EE378A project: Fundamental limits in language modeling
# June 2017

using ArgParse
using DataStructures
using GZip

argsettings = ArgParseSettings()
@add_arg_table argsettings begin
    "n"
        help = "Length of the n-gram to analyze"
        arg_type = Int
        required = true
    "-s", "--sourcedir"
        help = "Source directory, where the XX/wsj_XXYY files are"
        default = "/afs/ir/data/linguistic-data/Treebank/LDC95T7_Treebank-2/raw/wsj/"
    "-O", "--outputdir"
        help = "Output directory, where to put the Ngms-0001.gz files, default: <n>gms (e.g. 1gms if n = 1)"
        default = nothing
end
args = parse_args(argsettings)

n = args["n"]
sourcedirectory = args["sourcedir"]
if !isdir(sourcedirectory)
    println("Error: $sourcedirectory is not a directory.")
    exit(1)
end
outputdirectory = args["outputdir"]
if outputdirectory ≡ nothing
    outputdirectory = "ptb/$(n)gms"
end
if ispath(outputdirectory) && !isdir(outputdirectory):
    println("Error: $outputdirectory is not a directory.")
    exit(1)
end


"""Preprocess a line to split it into tokens. Rules:

 - The following characters are always their own token: " , ; % ? !
 - Where there is a space followed by a backtick, the backtick is its own token,
   and the first subsequent single quotation mark followed by a space is its own
   token. (These are assumed to be quote marked using single quotation marks.)
 - "'s" is always its own token
 - Hyphens between two lower-case letters are separated, as are hyphens between
   a number and a lower-case letter.
 - A full stop is its own token, so long as the character two before it is not
   a dot.

There is a translation of this in python/ngrams.py. When this function is
updated, that one should be too, and vice versa.
"""
function tokenize(line)
    for char in ['%', ',', ';', '"', '?', '!', ':', '(', ')', '“', '”']
        line = replace(line, "$char", " $char ")
    end
    line = replace(line, r"\s`(.+)'\s", s" ` \1 ' ")
    line = replace(line, r"\s‘(.+)’\s", s" ‘ \1 ’ ")
    line = replace(line, r"'s\s", " 's ")
    line = replace(line, r"([0-9])-([a-z])", s"\1 - \2")
    line = replace(line, r"([^A-Z][a-z]+)-([a-z])", s"\1 - \2")
    line = replace(line, r"([^\. ][A-Za-z0-9])\.\s", s"\1 .")
    tokens = split(line)
    if tokens[end] == "."
        return tokens[1:end-1]
    else
        return tokens
    end
end


"""Parse a single file of WSJ sentences in the Penn Treebank.
Returns a dictionary mapping n-grams to counts, the number of times that n-gram
occurred in the file.
"""
function parsefile(file)

    counts = counter(String)

    # Get past the start line
    line = readline(file)
    if line != ".START \n"
        println("Warning: file doesn't start with the .START token")
    end

    for line in eachline(file)
        if isspace(line)
            continue
        end
        tokens = tokenize(line)
        if n > 1
            tokens = vcat(tokens, "</S>")
        end

        for i = 1:length(tokens)-n+1
            ngram = join(tokens[i:i+n-1], " ")
            push!(counts, ngram)
        end
    end

    return counts
end


# Execution starts here

counts = counter(String)

for (root, dirs, filenames) in walkdir(sourcedirectory)
    println("Looking in $root")
    for filename in filenames
        filepath = joinpath(root, filename)
        datafile = open(filepath)
        filecounts = parsefile(datafile)
        close(datafile)
        counts = merge(counts, filecounts)
    end
end

mkpath(outputdirectory)
ngrams = sort(collect(keys(counts)))
perfile = 10000000
outfile = gzopen(joinpath(outputdirectory, "$(n)gms-0001.gz"), "w")

for (i, ngram) in enumerate(ngrams)
    if i % perfile == 1
        close(outfile)
        fileno = i ÷ perfile + 1
        outfilepath = joinpath(outputdirectory, "$(n)gms-$(lpad(fileno, 4, '0')).gz")
        outfile = gzopen(outfilepath, "w")
        println("Writing to $outfilepath")
    end
    write(outfile, "$ngram\t$(counts[ngram])\n")
end
close(outfile)
