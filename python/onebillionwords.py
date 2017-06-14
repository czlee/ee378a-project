"""Process One Billion Words data to produce JVHW or PML estimates, or index
files that can be fed into other estimators.

Chuan-Zheng Lee
EE378A project: Fundamental limits in language modeling
June 2017
"""

from est_entro import est_entro_JVHW
from pml import estimate_entropy_PML_approximate
from utils import tokenize
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("n", type=int, help="Length of n-gram")
parser.add_argument("-d", "--directory", type=str,
    default="/home/czlee/1-billion-word-language-modeling-benchmark/",
    help="Base directory of the 1 billion word repository")
parser.add_argument("outfile", type=argparse.FileType('w'), metavar="FILE", help="Write results to this file")
parser.add_argument("-t", "--pre-tokenized", action="store_false", dest="tokenize", help="Use pre-tokenized input data", default=True)
parser.add_argument("-Q", "--indices", action="store_true", default=False, help="Converts each n-gram to an integer and writes it to FILE")
parser.add_argument("-J", "--jvhw", action="store_true", default=False, help="Computes JVHW estimates and writes the result to FILE")
parser.add_argument("-P", "--pml", action="store_true", default=False, help="Computes PML estimates and writes the result to FILE")
args = parser.parse_args()

if not (args.indices or args.jvhw or args.pml):
    parser.error("At least one of -Q/--indices-file, -J/--jvhw-file and -P/--pml-file must be used")
if args.indices and (args.jvhw or args.pml):
    parser.error("-Q/--indices-file is incompatible with either -J/--jvhw-file or -P/--pml-file")

n = args.n
outfile = args.outfile

if args.tokenize:
    directory = os.path.join(args.directory, "training-monolingual")
else:
    directory = os.path.join(args.directory, "training-monolingual.tokenized.shuffled")
if not os.path.isdir(directory):
    print("Error: {} is not a directory.".format(directory))
    exit(1)
else:
    print("Looking in {}".format(directory))

ngrams = dict()  # key: ngram string, value: unique index
indices = list()
nindices = 0
counter = 1
last_index_write = 0

for filename in sorted(os.listdir(directory)):
    filepath = os.path.join(directory, filename)
    datafile = open(filepath)

    for line in datafile:
        if line.isspace():
            continue
        if args.tokenize:
            tokens = tokenize(line)
        else:
            tokens = line.split()
        if n > 1:
            tokens = tokens + ["</S>"]

        for i in range(0, len(tokens)-n):
            ngram = " ".join(tokens[i:i+n])
            index = ngrams.setdefault(ngram, len(ngrams))

            if args.indices:
                outfile.write(str(index) + "\n")

            if args.jvhw or args.pml: # heavy operation, only do if it will be used
                indices.append(index)

        # Note: `indices`, and (`jvhw`/`pml`) are mutually exclusive.
        # These two blocks will interfere with each other if they both run.

        if args.indices:
            nindices += len(tokens)-n

            if nindices - last_index_write > 1000:
                outfile.flush()
                last_index_write = nindices

            if nindices > counter * 1000000:
                print("{nindices}: {line}".format(nindices=nindices, line=line[:50]))
                counter += 1

        if (args.jvhw or args.pml) and len(indices) > counter * 100000:
            info = "{filename}, N = {N}".format(filename=filename, N=len(indices))

            if args.jvhw:
                jvhw_estimate = est_entro_JVHW(indices)[0]
                info += ", JVHW estimate = {jvhw}".format(jvhw=jvhw_estimate)

            if args.pml:
                pml_estimate = estimate_entropy_PML_approximate(indices)
                info += ", PML estimate = {pml}".format(pml=pml_estimate)

            print(info)
            outfile.write(info + "\n")
            outfile.flush()
            counter += 1

    datafile.close()

outfile.close()
