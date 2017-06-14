# Estimate entropy based on a corpus, using a naïve plug-in method (using the
# empirical distribution).
#
# Can be used on either Web 1T 5-gram data (directly), or data from the
# Penn Treebank preprocessed using frequencies.jl.
#
# Chuan-Zheng Lee
# EE378A project: Fundamental limits in language modeling
# June 2017

using ArgParse
using GZip

argsettings = ArgParseSettings()
@add_arg_table argsettings begin
    "dataset"
        range_tester = x -> x ∈ ["ptb", "1t5"]
        required = true
    "n"
        help = "Length of N-gram"
        arg_type = Int
        required = true
    "--directory"
        help = "Directory where the input files are"
        default = nothing
end
args = parse_args(argsettings)

ngramlength = args["n"]

if args["directory"] ≢ nothing
    directory = args["directory"]
elseif args["dataset"] == "ptb"
    directory = "ptb/$(ngramlength)gms/"
elseif args["dataset"] == "1t5"
    if ngramlength ∈ [1, 2, 3]
        directory = "/afs/ir/data/linguistic-data/Web1T5gram/data/$(ngramlength)gms/"
    elseif ngramlength ∈ [4, 5]
        directory = "/home/czlee/$(ngramlength)gms/"
    end
end
if !isdir(directory)
    println("Error: $directory is not a directory.")
    exit(1)
end
println("Source directory: $directory")
println()

if args["dataset"] == "1t5" && ngramlength == 1
    filenames = ["vocab.gz"]   # Don't use vocab_cs.gz
else
    filenames = filter(x -> endswith(x, ".gz"), readdir(directory))
end


N = 0
sum_nlogn = 0
entropy = 0     # define so that it exists outside the for loop
perplexity = 0  # define so that it exists outside the for loop


for filename in filenames
    filepath = joinpath(directory, filename)
    vocabfile = gzopen(filepath)
    println("-----------------------------------------------------------------")
    println("  File: $filename")
    println()

    for (i, line) in enumerate(eachline(vocabfile))
        parts = split(line)
        words = join(parts[1:end-1], " ")
        freq = parts[end]
        n = parse(Int64, freq)
        N += n
        nlogn = n*log2(n)
        sum_nlogn += nlogn
        entropy = log2(N) - sum_nlogn/N
        perplexity = 2^entropy
        if i % 1e6 == 0
            println("$i ($words), N = $N, sum_nlogn = $sum_nlogn")
            println("                 entropy = $entropy, perplexity = $perplexity")
            println()
        end
    end

    close(vocabfile)
end

println("final result:")
println("           N = $N")
println("   sum_nlogn = $sum_nlogn")
println("     entropy = $entropy")
println("  perplexity = $perplexity")
