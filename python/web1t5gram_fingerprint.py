"""Produces the fingerprint of a Web1T5gram dataset and writes it to a file.

Chuan-Zheng Lee
EE378A project: Fundamental limits in language modeling
June 2017
"""

import argparse
import os
import gzip
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("n", type=int, choices=[1, 2, 3, 4, 5])
parser.add_argument("fingerprintfile", type=argparse.FileType('w'), metavar="FINGERPRINTFILE", help="Write fingerprint to this file")
parser.add_argument("-d", "--directory", type=str, default=None,
    help="Input directory where the n-gram files are")
args = parser.parse_args()

ngramlength = args.n
fingerprintfile = args.fingerprintfile

if args.directory is not None:
    directory = args.directory
elif ngramlength in [1, 2, 3]:
    directory = "/afs/ir/data/linguistic-data/Web1T5gram/data/{:d}gms/".format(ngramlength)
elif ngramlength in [4, 5]:
    directory = "/home/czlee/{:d}gms/".format(ngramlength)
if not os.path.isdir(directory):
    print("Error: {} is not a directory.".format(directory))
    exit(1)
else:
    print("Looking in {}".format(directory))

if ngramlength == 1:
    filenames = ["vocab.gz"]
else:
    filenames = [x for x in os.listdir(directory) if x.endswith(".gz")]

fingerprint = Counter()

for filename in sorted(filenames):
    filepath = os.path.join(directory, filename)
    vocabfile = gzip.open(filepath)
    print("-------------------------------------------------------------------")
    print("  File: {}".format(filename))
    print("")

    for i, line in enumerate(vocabfile):
        words, freq = line.rsplit(None, 1)
        n = int(freq)
        fingerprint[n] += 1
        if i % 1e6 == 0:
            print("{i} {words}, fingerprint[{n}] = {count}, len(fingerprint) = {len}".format(
                i=i, words=words, n=n, count=fingerprint[n], len=len(fingerprint)))

    vocabfile.close()

for n in sorted(fingerprint.keys()):
    fingerprintfile.write("{n}\t{count}\n".format(n=n, count=fingerprint[n]))
fingerprintfile.close()
