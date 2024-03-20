#!/usr/bin/env python3

import functools
import math

def power(serial, x, y):
    rack_id = x + 10
    power = rack_id * y
    power += serial
    power *= rack_id
    power = (power // 100) % 10
    power -= 5
    return power
assert (got := power(8, 3, 5)) == 4, got
assert (got := power(57, 122, 79)) == -5, got
assert (got := power(39, 217, 196)) == 0, got
assert (got := power(71, 101, 153)) == 4, got

class Grid:
    def __init__(self, serial):
        self.serial = serial

    @functools.lru_cache(maxsize=300*300*10)
    def power(self, x, y):
        if x < 0 or 300 <= x or y < 0 or 300 <= y:
            return 0
        return power(self.serial, x, y)

    @functools.lru_cache(maxsize=300*300*300*10)
    def powerSQ(self, tlx, tly, sq):
        #print(f'power3x3 {tlx=} {tly=} {sq=}')
        assert sq > 0, (tlx, tly, sq)
        if sq == 1:
            return self.power(tlx, tly)
        pwr = 0
        half = sq//2
        pwr += self.powerSQ(tlx,      tly,      half)
        pwr += self.powerSQ(tlx+half, tly,      half)
        pwr += self.powerSQ(tlx,      tly+half, half)
        pwr += self.powerSQ(tlx+half, tly+half, half)
        if sq % 2 == 1:
            for n in range(sq-1):
                pwr += self.power(tlx+n, tly+sq-1)
                pwr += self.power(tlx+sq-1, tly+n)
            pwr += self.power(tlx+sq-1, tly+sq-1)
        return pwr

    def max_power(self):
        mp = -math.inf
        mx, my, msq = None, None, None
        for x in range(300):
            for y in range(300):
                for sq in range(1, min(300-x+1, 300-y+1)):
                    p = self.powerSQ(x,y,sq)
                    if p > mp:
                        mp = p
                        mx, my = x, y
                        msq = sq
                        print(f'grid={self.serial},{mx,my,msq},{mp=}')
        return mx, my, msq

#assert (got := Grid(18).max_power()) == (90, 269, 16), got
#assert (got := Grid(42).max_power()) == (232, 251, 12), got

with open('inputs/day11.input.txt') as f:
    real_input = f.read()
print(Grid(int(real_input)).max_power())  # => 236,227,12
