#!/usr/bin/env python3

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
        self.power = [[0 for x in range(300)] for y in range(300)]
        for x in range(300):
            for y in range(300):
                self.power[x][y] = power(self.serial, x, y)
        self.area = [[0 for x in range(300)] for y in range(300)]
        self.area[0][0] = self.power[0][0]
        for n in range(1, 300):
            self.area[0][n] = self.area[0][n-1] + self.power[0][n]
            self.area[n][0] = self.area[n-1][0] + self.power[n][0]
        for x in range(1, 300):
            for y in range(1, 300):
                self.area[x][y] = (self.area[x-1][y]
                                +  self.area[x][y-1]
                                -  self.area[x-1][y-1]
                                +  self.power[x][y])
            
    def powerSQ(self, tlx, tly, sq):
        if sq == 1:
            return self.power[tlx][tly]
        return (self.area[tlx+sq-1][tly+sq-1]
              + self.area[tlx]     [tly]
              - self.area[tlx+sq-1][tly]
              - self.area[tlx]     [tly+sq-1])

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
        return mx+1, my+1, msq-1

assert (got := Grid(18).max_power()) == (90, 269, 16), got
assert (got := Grid(42).max_power()) == (232, 251, 12), got

with open('inputs/day11.input.txt') as f:
    real_input = f.read()
print(Grid(int(real_input)).max_power())  # => 236,227,12
