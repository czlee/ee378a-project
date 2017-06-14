"""Estimates the entropy of a 1T5 fingerprint using the sparse matrix version
of the JVHW entropy estimator.

Chuan-Zheng Lee
EE378A project: Fundamental limits in language modeling
June 2017
"""

from est_entro_fingerprint import est_entro_JVHW_from_fingerprint_dict
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("fingerprintfile", type=argparse.FileType('r'), help="File containing the fingerprint")
args = parser.parse_args()

fingerprint = dict()

for line in args.fingerprintfile:
    k, v = line.split()
    fingerprint[int(k)] = int(v)

args.fingerprintfile.close()

print("There are {} entries in the fingerprint.".format(len(fingerprint)))
print("The estimated entropy is:")
print(est_entro_JVHW_from_fingerprint_dict(fingerprint))
