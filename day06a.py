#!/usr/bin/env python3

import math
import re

from collections import defaultdict, namedtuple
from heapdict import heapdict

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
    return set([Point(*numbers(line)) for line in inp.strip().splitlines()])

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

def nearests(points, o):
    """Return the points in points that are closest to o."""
    nearest = []
    nearest_distance = math.inf
    for p in points:
        m = manhattan(o, p)
        if m < nearest_distance:
            nearest = [p]
            nearest_distance = m
        elif m == nearest_distance:
            nearest.append(p)
    return nearest

def infinity(pmin, pmax):
    """Yields a bounding box of points that are basically infinity away."""
    width = abs(pmax.x + 1 - pmin.x)
    height = abs(pmax.y + 1 - pmin.y)
    hw = max(width, height)
    qmin = Point(pmin.x - hw, pmin.y - hw)
    qmax = Point(pmax.x + hw, pmax.y + hw)
    for x in range(qmin.x, qmax.x):
        yield Point(x, qmin.y)
        yield Point(x, qmax.y)
    for y in range(qmin.y, qmax.y):
        yield Point(qmin.x, y)
        yield Point(qmax.x, y)


def infinites(points):
    """Returns any points in points that have infinite closest points."""
    ret = set()
    pmin, pmax = bounding_box(points)
    for p in infinity(pmin, pmax):
        nn = nearests(points, p)
        if len(nn) > 1:
            continue
        assert len(nn) == 1, (p, nn)
        ret.add(nn[0])
    return ret

def survey(points):
    closests = defaultdict(list)
    pmin, pmax = bounding_box(points)
    for x in range(pmin.x - 1, pmax.x + 2):
        for y in range(pmin.y - 1, pmax.y + 2):
            p = Point(x,y)
            nearest = nearests(points, p)
            if len(nearest) > 1:
                continue
            assert len(nearest) == 1, (p, nearest)
            closests[nearest[0]].append(p)
    for p in infinites(points):
        del closests[p]
    return closests

def run(inp):
    points = parse(inp)
    gardens = survey(points)
    loneliest = max(gardens, key=lambda g: len(gardens[g]))
    return len(gardens[loneliest])

assert (got := run(example_input)) == 17, got

with open('inputs/day06.input.txt') as f:
    real_input = f.read()
print(run(real_input)) # => 2342
