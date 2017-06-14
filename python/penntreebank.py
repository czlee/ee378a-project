"""Process Penn Treebank data to produce JVHW estimates, or index files that can
be fed into the PML or VV estimators.

Chuan-Zheng Lee
EE378A project: Fundamental limits in language modeling
June 2017
"""

from est_entro import est_entro_JVHW
from utils import tokenize
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("n", type=int, help="Length of n-gram")
parser.add_argument("-d", "--directory", type=str,
    default="/afs/ir/data/linguistic-data/Treebank/LDC95T7_Treebank-2/raw/wsj/",
    help="Input directory where WSJ files are")
action = parser.add_mutually_exclusive_group(required=True)
action.add_argument("-Q", "--indices-file", type=argparse.FileType('w'), metavar="FILE",
    help="Converts each n-gram to an integer and writes it to FILE")
action.add_argument("-J", "--jvhw-file", type=argparse.FileType('w'), metavar="FILE",
    help="Computes JVHW estimates and writes the result to FILE")
parser.add_argument("-M", "--ngrams-file", type=argparse.FileType('w'), metavar="FILE",
    help="Also writes the n-grams and their counts to FILE")
args = parser.parse_args()

n = args.n
directory = args.directory
indices_file = args.indices_file
jvhw_file = args.jvhw_file
ngrams_file = args.ngrams_file

if not os.path.isdir(directory):
    print("Error: {} is not a directory.".format(directory))
    exit(1)
else:
    print("Looking in {}".format(directory))

def parse_file(datafile, ngrams):
    """Parses a file, looking up each ngram in `ngrams`, adding it if it isn't
    already there. Returns a list of indices corresponding to the words in
    `datafile`."""

    line = datafile.readline()
    if line != ".START \n":
        print("Warning: file doesn't start with the .START token")

    indices = []

    for line in datafile:
        if line.isspace():
            continue
        tokens = tokenize(line)
        if n > 1:
            tokens = tokens + ["</S>"]

        for i in range(1, len(tokens)-n):
            ngram = " ".join(tokens[i:i+n])
            index = ngrams.setdefault(ngram, len(ngrams))
            indices.append(index)

    return indices


ngrams = dict()  # key: ngram string, value: unique index
indices = list()

for root, dirs, filenames in os.walk(directory):
    for filename in filenames:
        filepath = os.path.join(root, filename)
        datafile = open(filepath)

        new_indices = parse_file(datafile, ngrams)

        if indices_file:
            indices_str = "\n".join([str(i) for i in new_indices]) + "\n"
            indices_file.write(indices_str)
            indices_file.flush()
            if filename.endswith("99"):
                print("done {}".format(filename))

        if jvhw_file:
            indices.extend(new_indices)
            jvhw_estimate = est_entro_JVHW(indices)[0]
            jvhw_info = "{filename}, n = {n}, JVHW estimate = {jvhw}".format(
                    filename=filename, n=len(indices), jvhw=jvhw_estimate)
            print(jvhw_info)
            jvhw_file.write(jvhw_info + "\n")
            jvhw_file.flush()

        datafile.close()

if ngrams_file:
    for ngram, index in ngrams.items():
        ngrams_file.write("{index}\t{ngram}\n".format(index=index, ngram=ngram))
    ngrams_file.close()
