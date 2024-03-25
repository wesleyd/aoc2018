#!/usr/bin/env python3

import math
import re

from collections import namedtuple

example_input = """
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
"""

Point = namedtuple('Point', ['x', 'y'])
up    = lambda p: Point(p.x,     p.y - 1)
down  = lambda p: Point(p.x,     p.y + 1)
left  = lambda p: Point(p.x - 1, p.y    )
right = lambda p: Point(p.x + 1, p.y    )

LINE_RE = re.compile(r'([xy])=(\d+), ([xy])=(\d+)\.\.(\d+)')

class Grid:
    def __init__(self, inp):
        self.g = {}
        for line in inp.strip().splitlines():
            m = LINE_RE.match(line)
            if m.group(1) == 'x':
                x = int(m.group(2))
                assert 'y' == m.group(3)
                for y in range(int(m.group(4)), int(m.group(5))+1):
                    self.g[Point(x,y)] = '#'
            elif m.group(1) == 'y':
                y = int(m.group(2))
                assert 'x' == m.group(3)
                for x in range(int(m.group(4)), int(m.group(5))+1):
                    self.g[Point(x,y)] = '#'
        self.miny, self.maxy = math.inf, -math.inf
        for p in self.g:
            if p.y < self.miny:
                self.miny = p.y
            if p.y > self.maxy:
                self.maxy = p.y

    def at(self, p):
        if p.y < self.miny or self.maxy < p.y:
            return ' '
        return self.g.get(p, '.')

    def draw(self):
        minx, maxx = math.inf, -math.inf
        for p in self.g:
            if p.x < minx:
                minx = p.x
            if p.x > maxx:
                maxx = p.x
        lines = []
        for y in range(self.miny, self.maxy+1):
            line = []
            for x in range(minx, maxx+1):
                line.append(self.at(Point(x,y)))
            lines.append(''.join(line))
        return '\n'.join(lines)

    def drain_left(self, p):
        """Returns watery point leftmost of p, and whether it drains."""
        while self.at(l := left(p)) in '.|':
            p = l
            if self.at(down(p)) in '.|':
                return p, True
        return p, False

    def drain_right(self, p):
        """Returns watery point rightmost of p, and whether it drains."""
        while self.at(r := right(p)) in '.|':
            p = r
            if self.at(down(p)) in '.|':
                return p, True
        return p, False

    def fill(self):
        spigots = [Point(500, self.miny)]
        while spigots:
            p = spigots.pop()
            if self.at(p) == '.':
                self.g[p] = '|'
            d = down(p)
            if self.at(d) == '.':
                spigots.append(d)
                continue
            elif self.at(d) in '#~':
                l, drains_left = self.drain_left(p)
                r, drains_right = self.drain_right(p)
                drains = drains_left or drains_right
                q = l
                while q.x <= r.x:
                    self.g[q] = '|' if drains else '~'
                    q = right(q)
                if drains_left:
                    spigots.append(l)
                if drains_right:
                    spigots.append(r)
                if not drains:
                    spigots.append(up(p))

    def count(self):
        return sum(1 for c in self.g.values() if c in '~')
           
        
g = Grid(example_input)
g.fill()
assert (got := g.count()) == 29, g

with open('inputs/day17.input.txt') as f:
    real_input = f.read()
g = Grid(real_input)
g.fill()
#print(g.draw())
print(g.count())  # => 27068

