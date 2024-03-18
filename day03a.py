#!/usr/bin/env python3

import re

from collections import defaultdict, namedtuple

example_input = """
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2
"""

Claim = namedtuple('Claim', ['id', 'left', 'top', 'width', 'height'])

def numbers(s):
    return [int(x) for x in re.findall(r'\d+', s)]

def parse(inp):
    return [Claim(*numbers(line)) for line in inp.strip().splitlines()]

def overlaps(claims):
    oo = defaultdict(int)
    for c in claims:
        for x in range(c.left, c.left+c.width):
            for y in range(c.top, c.top+c.height):
                oo[(x,y)] += 1
    return sum(1 if m > 1 else 0 for m in oo.values())
assert (got := overlaps(parse(example_input))) == 4, got

with open('inputs/day03.input.txt') as f:
    real_input = f.read()
print(overlaps(parse(real_input))) # => 119572
