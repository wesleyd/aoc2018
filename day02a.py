#!/usr/bin/env python3

from collections import defaultdict

example_input = """
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
"""

def checksum(inp):
    n2 = 0
    n3 = 0
    for s in inp.strip().splitlines():
        histo = defaultdict(int)
        for c in s:
            histo[c] += 1
        if 2 in histo.values():
            n2 += 1
        if 3 in histo.values():
            n3 += 1
    return n2 * n3

assert (got := checksum(example_input)) == 12, got

with open('inputs/day02.input.txt') as f:
    real_input = f.read()

print(checksum(real_input)) # => 9633



