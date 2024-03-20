#!/usr/bin/env python3

import re

example_input = """
2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
"""

def numbers(s):
    for x in re.findall(r'\d+', s):
        yield int(x)

def sum_metadata(g):
    num_nodes = next(g, -1)
    num_metadata = next(g, -1)
    nodes = [sum_metadata(g) for _ in range(num_nodes)]
    metadata = [next(g) for _ in range(num_metadata)]
    if nodes:
        ret = 0
        for n in metadata:
            k = n-1
            if k < 0 or len(nodes) <= k:
                continue
            ret += nodes[k]
        return ret
    return sum(metadata)
    return ret

def run(inp):
    return sum_metadata(numbers(inp))

assert (got := run(example_input)) == 66, got

with open('inputs/day08.input.txt') as f:
    real_input = f.read()
print(run(real_input)) # => 16695
