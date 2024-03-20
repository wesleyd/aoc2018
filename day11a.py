#!/usr/bin/env python3

import functools
import math

def power(serial, x, y):
    rack_id = x + 10
    power = rack_id * y
    power += serial
    power *= rack_id
    power = int(str(power)[-3:-2])
    power -= 5
    return power
assert (got := power(8, 3, 5)) == 4, got
assert (got := power(57, 122, 79)) == -5, got
assert (got := power(39, 217, 196)) == 0, got
assert (got := power(71, 101, 153)) == 4, got

class Grid:
    def __init__(self, serial):
        self.serial = serial

    @functools.lru_cache
    def power(self, x, y):
        if x < 0 or 300 <= x or y < 0 or 300 <= y:
            return 0
        return power(self.serial, x, y)

    def power3x3(self, tlx, tly):
        pwr = 0
        for x in range(tlx, tlx+3):
            for y in range(tly, tly+3):
                pwr += self.power(x, y)
        return pwr

    def max_power3x3(self):
        mp = -math.inf
        mx, my = None, None
        for x in range(300):
            for y in range(300):
                p = self.power3x3(x,y)
                if p > mp:
                    mp = p
                    mx, my = x, y
        return mx, my, mp

assert (got := Grid(18).max_power3x3()) == (33, 45, 29), got
assert (got := Grid(42).max_power3x3()) == (21, 61, 30), got

with open('inputs/day11.input.txt') as f:
    real_input = f.read()
x, y, _ = Grid(int(real_input)).max_power3x3()
print(x,y) # => 235,18
