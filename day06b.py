#!/usr/bin/env python3

import math
import re

from collections import namedtuple

example_input = """
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
"""

Point = namedtuple('Point', ['x', 'y'])

def manhattan(p, q):
    return abs(p.x - q.x) + abs(p.y - q.y)

def numbers(s):
    return [int(x) for x in re.findall(r'\d+', s)]

def parse(inp):
    return [Point(*numbers(line)) for line in inp.strip().splitlines()]

def bounding_box(points):
    xmin, ymin = math.inf, math.inf
    xmax, ymax = -math.inf, -math.inf
    for p in points:
        if p.x > xmax:
            xmax = p.x
        if p.x < xmin:
            xmin = p.x
        if p.y > ymax:
            ymax = p.y
        if p.y < ymin:
            ymin = p.y
    return (Point(xmin, ymin), Point(xmax,ymax))

def total_distance(points, p):
    """Returns the total distance of p to all of points."""
    return sum(manhattan(p, q) for q in points)
assert (got := total_distance(parse(example_input), Point(4,3))) == 30, got

def perimeter(pmin, pmax):
    """Yields every point in the perimeter of pmin/pmax."""
    for x in pmin.x, pmax.x:
        yield Point(x, pmin.y)
        yield Point(x, pmax.y)
    for y in pmin.y, pmax.y:
        yield Point(pmin.x, y)
        yield Point(pmax.x, y)

def widely_search(inp, max_distance):
    region_size = 0
    points = parse(inp)
    pmin, pmax = bounding_box(points)
    for x in range(pmin.x, pmax.x+1):
        for y in range(pmin.x, pmax.x+1):
            p = Point(x,y)
            if total_distance(points, p) < max_distance:
                region_size += 1
    while True:
        before = region_size
        pmin = Point(pmin.x-1, pmin.y-1)
        pmax = Point(pmax.x+1, pmax.y+1)
        for p in perimeter(pmin, pmax):
            if total_distance(points, p) < max_distance:
                region_size += 1
        if region_size == before:  # Limit hit
            return region_size

print(widely_search(example_input, 32))

with open('inputs/day06.input.txt') as f:
    real_input = f.read()
print(widely_search(real_input, 10000)) # => 43302
