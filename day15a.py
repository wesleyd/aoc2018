#!/usr/bin/env python3

import heapq
import math

from collections import deque, namedtuple
from dataclasses import dataclass
from heapdict import heapdict

XY = namedtuple('XY', ['x', 'y'])
up    = lambda p: XY(p.x,   p.y - 1)
down  = lambda p: XY(p.x,   p.y + 1)
left  = lambda p: XY(p.x - 1, p.y)
right = lambda p: XY(p.x + 1, p.y)

@dataclass
class WeWon(Exception):
    us: str

@dataclass
class Unit:
    c: str # 'G' or 'E'
    p: XY # Current position
    i: int  # Order at start of round
    hp: int = 200
    ap: int = 3
    def alive(self):
        return self.hp > 0
    def __str__(self):
        return f'{self.c}@{self.p} {self.hp})'

class Game:
    def __init__(self, inp):
        i = 0
        self.grid = []  # a dot or a hash for [y][x]
        self.occupied = {}  # position => unit
        self.tn = 0
        for y, line in enumerate(inp.strip().splitlines()):
            row = []
            for x, c in enumerate(line):
                p = XY(x,y)
                if c in '#.':
                    row.append(c)
                elif c in 'EG':
                    row.append('.')
                    u = Unit(c,p,i)
                    i += 1
                    self.occupied[p] = u
                else:
                    assert False, (c, x, y)
            self.grid.append(''.join(row))

    def at(self, p):
        if (u := self.occupied.get(p)):
            return u.c
        if 0 <= p.y < len(self.grid) and 0 <= p.x < len(self.grid[p.y]):
            return self.grid[p.y][p.x]
        return '.'

    def __str__(self):
        lines = []
        for y, row in enumerate(self.grid):
            line = []
            line_units = []
            for x, c in enumerate(row):
                p = XY(x,y)
                line.append(self.at(p))
                if (u := self.occupied.get(p)):
                    line_units.append(f' ({u.hp})')
            lines.append(''.join(line) + ''.join(line_units))
        return '\n'.join(lines)

    def all_enemies(self, u):
        """Yields all the enemies of u."""
        n = 0
        for v in self.occupied.values():
            if v != u and u.c != v.c:
                yield v
                n += 1
        if not n:
            raise WeWon(us=u.c)

    def tastiest(self, u):
        """Returns the optimal enemy adjacent to p, if there is one."""
        candidates = []
        for q in [up(u.p), left(u.p), right(u.p), down(u.p)]:
            v = self.occupied.get(q)
            if not v:
                continue  # There is nothing there
            # There is *something* there...
            if u.c == v.c:
                continue  # It's one of ours
            # Sort by lowest hp, then start-of-round order
            heapq.heappush(candidates, (v.hp, v.i, v))
        if candidates:
            return candidates[0][2]
        return None
            
    def attack(self, u):
        """Returns True if u attacked somebody."""
        v = self.tastiest(u)
        if not v:  # Nobody to attack
            return False
        v.hp -= u.ap
        if v.hp <= 0:
            del self.occupied[v.p]
            v.p = None
        return True

    def moves_from(self, p):
        """Yields all the possible moves from p."""
        for d in [up(p), left(p), right(p), down(p)]:
            if self.at(d) == '.':
                yield d

    def best_enemy_adjacency(self, u):
        """Returns the optimal enemy adjacency to aim for, if there is one."""
        goals = set()  # All the empty spaces beside an enemy
        for e in self.all_enemies(u):
            for d in [up(e.p), down(e.p), left(e.p), right(e.p)]:
                if self.at(d) == '.':
                    goals.add(d)
        # Search goals for the closest and topleftiest
        prev = set()
        future = heapdict()
        future[u.p] = 0
        best_goals = []
        best_distance = math.inf  # distance to best_goals
        while future:
            p, d = future.popitem()
            prev.add(p)
            for q in [up(p), left(p), right(p), down(p)]:
                if q in prev or q in future or self.at(q) != '.':
                    continue
                future[q] = d+1
            if best_goals and d > best_distance:  # Rest are too far. Done.
                break
            if p in goals:
                heapq.heappush(best_goals, (p.y, p.x))
                assert d <= best_distance, (d, best_distance)
                best_distance = d
        if not best_goals:
            # There is nowhere to move to!
            return
        y, x = best_goals[0]
        return XY(x,y)

    def shortest_distance(self, a, z):
        """Returns the shortest distances from a to z."""
        prev = set()
        future = heapdict()
        future[a] = 0
        while future:
            p, d = future.popitem()
            if p == z:
                return d
            prev.add(p)
            for q in [up(p), down(p), left(p), right(p)]:
                if q in prev or q in future or self.at(q) != '.':
                    continue
                future[q] = d+1

    def best_move(self, u):
        """Returns the best move u can make."""
        goal = self.best_enemy_adjacency(u)
        if not goal:
            return None
        shortest_start = None
        shortest = math.inf
        # Which of u/l/r/d gives shortest path to goal? (Tie => first of ULRD)
        for p in [up(u.p), left(u.p), right(u.p), down(u.p)]:  # Note order!
            if self.at(p) != '.':
                continue
            d = self.shortest_distance(p, goal)
            if d is None:
                continue
            d += 1  # We started from one step away
            if d < shortest:
                shortest = d
                shortest_start = p
        return shortest_start

    def move(self, u):
        if self.attack(u):
            return True
        q = self.best_move(u)
        if q:
            assert u == self.occupied[u.p], (u, self.occupied[u.p])
            del self.occupied[u.p]
            u.p = q
            self.occupied[u.p] = u
        return self.attack(u)
            
    def turn(self):
        units = list(self.occupied.values())
        units.sort(key=lambda u: (u.p.y, u.p.x))
        for i, u in enumerate(units):
            u.i = i
        for u in units:
            if not u.alive():
                continue
            self.move(u)
        self.tn += 1
        #print(f'After {self.tn} round(s):')
        #print(self)
        #print()

    def play(self):
        while True:
            try:
                self.turn()
            except WeWon as e:
                hp_remaining = 0
                for u in self.occupied.values():
                    assert u.hp > 0, u
                    hp_remaining += u.hp
                return hp_remaining * self.tn

                
example_input_1 = """
#######
#E..G.#
#...#.#
#.G.#G#
#######
"""
#g = Game(example_input_1)
#print(g.play())
#print(g)

example_input_2 = """
#########
#G..G..G#
#.......#
#.......#
#G..E..G#
#.......#
#.......#
#G..G..G#
#########
"""
#g = Game(example_input_3)
#print(g.play())
#print(g)

g = Game("""
#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######   
""")
assert (got := g.play()) == 27730, got

g = Game("""
#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######
""")
assert (got := g.play()) == 36334, got

g = Game("""
#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######
""")
assert (got := g.play()) == 39514, got

g = Game("""
#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######
""")
assert (got := g.play()) == 27755, got

g = Game("""
#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######
""")
assert (got := g.play()) == 28944, got

g = Game("""
#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########
""")
assert (got := g.play()) == 18740, got

with open('inputs/day15.input.txt') as f:
    real_input = f.read()
print(Game(real_input).play()) # => 225096
