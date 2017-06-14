# -*- coding: utf-8 -*-
import re

def tokenize(line):
    """Translation of tokenize() in frequencies.jl. See that file for docstring.
    When this function is updated, that one should be too, and vice versa."""
    for char in ['%', ',', ';', '"', '?', '!', ':', '(', ')', '“', '”']:
        line = line.replace(char, " " + char + " ")
    line = re.sub(r"\s`(.+)'\s", r" ` \1 ' ", line)
    line = re.sub(r"\s‘(.+)’\s", r" ‘ \1 ’ ", line)
    line = re.sub(r"'s\s", r" 's ", line)
    line = re.sub(r"([0-9])-([a-z])", r"\1 - \2", line)
    line = re.sub(r"([^A-Z][a-z]+)-([a-z])", r"\1 - \2", line)
    line = re.sub(r"([^\. ][A-Za-z0-9])\.\s", r"\1 .", line)
    tokens = line.split()
    if tokens[-1] == ".":
        return tokens[:-1]
    else:
        return tokens
