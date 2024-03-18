#!/usr/bin/env python3

import itertools
import re

with open('inputs/day01.input.txt') as f:
    real_input = f.read()

def numbers(s):
    return [int(x) for x in re.findall(r'[+-]?\d+', s)]

def run(inp, freq=0):
    prev = set([freq])
    for n in itertools.cycle(numbers(inp)):
        freq += n
        if freq in prev:
            return freq
        prev.add(freq)

print(run(real_input)) # => 55250

