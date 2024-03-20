#!/usr/bin/env python3

import re

example_input = """
2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
"""

def numbers(s):
    for x in re.findall(r'\d+', s):
        yield int(x)

def sum_metadata(g):
    ret = 0
    num_nodes = next(g, -1)
    num_metadata = next(g, -1)
    for i in range(num_nodes):
        ret += sum_metadata(g)
    for i in range(num_metadata):
        ret += next(g)
    return ret

def run(inp):
    return sum_metadata(numbers(inp))

assert (got := run(example_input)) == 138, got

with open('inputs/day08.input.txt') as f:
    real_input = f.read()
print(run(real_input)) # => 36627
