#!/usr/bin/env python3

from collections import defaultdict

example_input = """
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
"""

def deltas(s1, s2):
    assert len(s1) == len(s2), (s1, s2)
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            yield i

def closest_pair(inp):
    words = inp.strip().splitlines()
    for i in range(len(words)):
        for j in range(i+1, len(words)):
            kk = list(deltas(words[i], words[j]))
            if len(kk) != 1:
                continue
            k = kk[0]
            return words[i][:k] + words[i][k+1:]
assert (got := closest_pair(example_input)) == 'fgij', got

with open('inputs/day02.input.txt') as f:
    real_input = f.read()

print(closest_pair(real_input)) # => lujnogabetpmsydyfcovzixaw



