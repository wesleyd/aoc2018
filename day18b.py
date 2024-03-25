#!/usr/bin/env python3

import copy

from collections import namedtuple

example_input = """
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
"""

def parse(inp):
    return [list(line) for line in inp.strip().splitlines()]

Point = namedtuple('Point', ['x', 'y'])
up    = lambda p: Point(p.x,     p.y - 1)
down  = lambda p: Point(p.x,     p.y + 1)
left  = lambda p: Point(p.x - 1, p.y    )
right = lambda p: Point(p.x + 1, p.y    )

def around(p):
    yield up(p)
    yield down(p)
    yield left(p)
    yield right(p)
    yield up(left(p))
    yield up(right(p))
    yield down(left(p))
    yield down(right(p))

def at(forest, p):
    if 0 <= p.y < len(forest) and 0 <= p.x < len(forest[p.y]):
        return forest[p.y][p.x]
    return '.'

def explore(forest):
    for y, line in enumerate(forest):
        for x in range(len(line)):
            yield Point(x, y)

def magic1(forest, p):
    adjacent = [at(forest, q) for q in around(p)]
    c = at(forest, p)
    ntrees = sum(1 for a in adjacent if a == '|')
    nlumberyards = sum(1 for a in adjacent if a == '#')
    if c == '.':
        return '|' if ntrees >= 3 else '.'
    elif c == '|':
        return '#' if nlumberyards >= 3 else '|'
    elif c == '#':
        return '#' if nlumberyards >= 1 and ntrees >= 1 else '.'

def magic(forest):
    forest2 = copy.deepcopy(forest)
    for p in explore(forest):
        forest2[p.y][p.x] = magic1(forest, p)
    return forest2

def petrify(forest):
    return '\n'.join(''.join(line) for line in forest)

def count(forest, c):
    return sum(1 for p in explore(forest) if at(forest, p) == c)

def resource_value(forest):
    ntrees = count(forest, '|')
    nlumberyards = count(forest, '#')
    return ntrees * nlumberyards

def run(inp, n=1000000000):
    forest = parse(inp)
    prev = {petrify(forest): 0}
    i = 0
    while i < n:
        i += 1
        forest = magic(forest)
        pf = petrify(forest)
        if pf in prev:
            h = prev[pf]
            period = i - h
            njumps = (n - i) // period
            i += period * njumps
        else:
            prev[pf] = i
    return resource_value(forest)

with open('inputs/day18.input.txt') as f:
    real_input = f.read()

print(run(real_input)) # => 107912
