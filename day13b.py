#!/usr/bin/env python3

import math

from collections import namedtuple

example_input = r"""
/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
"""

Point = namedtuple('Point', ['x', 'y'])
up    = lambda p: Point(p.x,   p.y - 1)
down  = lambda p: Point(p.x,   p.y + 1)
left  = lambda p: Point(p.x - 1, p.y)
right = lambda p: Point(p.x + 1, p.y)

def parse(inp):
    grid = {}
    carts = {}
    for y, line in enumerate(inp.lstrip('\n').splitlines()):
        for x, ch in enumerate(line):
            if ch == ' ':
                continue
            grid[Point(x,y)] = ch
    for p, d in grid.items():
        if d in 'v<^>':
            assert p not in carts
            carts[p] = (d, 'L')  # 'L' is choice at next intersection
        if d in '><':
            grid[p] = '-'
        elif d in '^v':
            grid[p] = '|'
    return grid, carts

def draw(grid, carts):
    right, bottom = -math.inf, -math.inf
    for p in grid:
        if p.x > right:
            right = p.x
        if p.y > bottom:
            bottom = p.y
    chars = []
    for y in range(bottom+1):
        for x in range(right+1):
            p = Point(x,y)
            if (x := carts.get(p, None)):
                d, _ = x
                chars.append(d)
            elif (ch := grid.get(p, None)):
                chars.append(ch)
            else:
                chars.append(' ')
        chars.append('\n')
    return ''.join(chars)

LEFT = {'<': 'v', 'v': '>', '>': '^', '^': '<'}
RIGHT = {'<': '^', '^': '>', '>': 'v', 'v': '<'}

def rotate(d, m):
    assert m in 'LSR', m
    assert d in '^v<>', d
    if m == 'L':
        d2 = LEFT[d]
        m2 = 'S'
    elif m == 'S':
        d2 = d
        m2 = 'R'
    elif m == 'R':
        d2 = RIGHT[d]
        m2 = 'L'
    return (d2, m2)

@dataclass
class Collision(Exception):
    p: Point

SLASH = {'>': '^', '^': '>', '<': 'v', 'v': '<'}
BACKSLASH = {'>': 'v', 'v': '>', '<': '^', '^': '<'}

def move1(grid, carts):
    cc = list(carts.keys())
    cc.sort(key=lambda p: (p.y, p.x))
    for p in cc:
        if p not in carts:
            continue
        d, m = carts[p]
        if d == 'v':
            q = down(p)
        elif d == '^':
            q = up(p)
        elif d == '<':
            q = left(p)
        elif d == '>':
            q = right(p)
        else:
            assert False, (d, m, p)
        assert q in grid, q
        ch = grid[q]
        m2 = m
        if ch == '+':
            d2, m2 = rotate(d, m)
        elif ch == '/':
            d2 = SLASH[d]
        elif ch == '\\':
            d2 = BACKSLASH[d]
        elif ch in '|-':
            d2 = d
        else:
            assert False, (ch, p, q, d, m)
        if q in carts:
            # Collision! Remove both!
            del carts[q]
            del carts[p]
            continue
        del carts[p]
        carts[q] = (d2, m2)

def crash(inp):
    grid, carts = parse(inp)
    while len(carts) > 1:
        move1(grid, carts)
    return list(carts.keys())[0]
            
assert (got := crash(example_input)) == Point(6,4), got

with open('inputs/day13.input.txt') as f:
    real_input = f.read()
print(crash(real_input))  # 91,25
