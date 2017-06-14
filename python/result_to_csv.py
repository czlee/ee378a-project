#!/usr/bin/python3
"""Converts entropy result files to CSV.
Does one result file at a time, so run once for JVHW then once for PML."""

import csv
import os
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('dataset', choices=['ptb','1bw'])
parser.add_argument('directory')
parser.add_argument('estimate_type', choices=['jvhw', 'pml'])
args = parser.parse_args()

prefixes = ['uni', 'bi', 'tri', 'quadri', 'quinti', 'sexi', 'septi']

if args.dataset == 'ptb':
    filetemplate = "{prefix}grams.txt"
    pattern = r"wsj_\d+, n = (\d+), .*" + args.estimate_type.upper() + " estimate = ([\d.]+)"
elif args.dataset == '1bw':
    filetemplate = "{prefix}grams-pretokenized.txt"
    pattern = r"news.en-\d{5}-of-\d{5}, N = (\d+), .*" + args.estimate_type.upper() + " estimate = ([\d.]+)"
filepath = os.path.join(args.directory, filetemplate)
outfilepath = "../matlab/{dataset}/" + args.estimate_type.lower() + "/{i}grams.csv"

for i, prefix in enumerate(prefixes, start=1):
    filename = os.path.join(filepath.format(prefix=prefix))
    if not os.path.exists(filename):
        print("Warning: {filename} does not exist, skipping".format(filename=filename))
        continue

    with open(filename) as infile, open(outfilepath.format(dataset=args.dataset,i=i), mode='w', newline='') as outfile:
        outwriter = csv.writer(outfile)
        for line in infile:
            m = re.match(pattern, line)
            if m is None:
                print("Warning: No match match found in line: {line}".format(line=line))
                continue
            outwriter.writerow(m.groups())
