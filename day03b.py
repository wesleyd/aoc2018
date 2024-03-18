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

def inches(c: Claim):
    """Yields all the squares in c."""
    for x in range(c.left, c.left+c.width):
        for y in range(c.top, c.top+c.height):
            yield (x,y)

def isolated(claims):
    oo = defaultdict(int)
    for c in claims:
        for p in inches(c):
            oo[p] += 1
    for c in claims:
        for p in inches(c):
            if oo[p] != 1:
                break
        else:
            return c.id
assert (got := isolated(parse(example_input))) == 3, got

with open('inputs/day03.input.txt') as f:
    real_input = f.read()
print(isolated(parse(real_input))) # => 775
