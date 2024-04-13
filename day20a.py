#!/usr/bin/env python3

from collections import defaultdict, namedtuple
from heapdict import heapdict

Point = namedtuple('Point', ['x', 'y'])

def move1(p, c):
    match c:
        case 'N': return Point(p.x,     p.y + 1)
        case 'S': return Point(p.x,     p.y - 1)
        case 'E': return Point(p.x + 1, p.y    )
        case 'W': return Point(p.x - 1, p.y    )

def parMove1(pp, c):
    return [move1(p, c) for p in pp]

# class Walker:
#     def __init__(self, inp):
#         self.doors = defaultdict(set)
#         self.parse(inp.strip(), Point(0,0))
#     def parse(self, s, p):
#         start = p
#         ends = set()
#         for i, c in enumerate(s):
#             if c in 'NESW':
#                 q = move1(p, c)
#                 self.doors[p].add(q)
#                 self.doors[q].add(p)
#                 p = q
#                 continue
#             if c == '|':
#                 ends.add(p)
#                 p = start
#             elif c == '$':
#                 yield p
#             elif c == '(':
#                 for q in self.parse(s, p):
#             elif c == ')':
#                 ends.add(p)
#                 t = s[i+1:]
#                 for p in ends:
#                     yield self.parse(t, p)


def walk(inp):
    s = iter(inp.strip())
    doors = defaultdict(set)
    def alternate(pp=None):
        if not pp:
            pp = set([Point(0,0)])
        starts = set(pp)
        ends = set()
        while True:
            c = next(s)
            if c in 'NESW':
                qq = parMove1(pp, c)
                for p, q in zip(pp, qq):
                    doors[p].add(q)
                    # doors[q].add(p)
                pp = qq
            elif c == '(':
                pp = alternate(pp)
            elif c == '|':
                ends.update(pp)
                pp = set(starts)
            elif c in ')$':
                ends.update(pp)
                return ends
    alternate()
    return doors

def furthest(doors):
    future = heapdict()
    future[Point(0,0)] = 0
    dist = {}
    while future:
        p, d = future.popitem()
        dist[p] = d
        for q in doors[p]:
            if q in dist: 
                continue
            if q in future:
                continue
            future[q] = d+1
    return max(dist.values())

assert (got := furthest(walk('^WNE$'))) == 3, got
assert (got := furthest(walk('^ENWWW(NEEE|SSE(EE|N))$'))) == 10, got
assert (got := furthest(walk('^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'))) == 18, got
assert (got := furthest(walk('^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'))) == 23, got
assert (got := furthest(walk('^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'))) == 31, got

with open('inputs/day20.input.txt') as f:
    real_input = f.read()
print(furthest(walk(real_input)))
