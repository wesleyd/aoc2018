#!/usr/bin/env python3

import re
import sys

from dataclasses import dataclass

example_input = """
position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>
"""

@dataclass
class Particle:
    px: int
    py: int
    vx: int
    vy: int

def numbers(s):
    return [int(x) for x in re.findall(r'-?\d+', s)]

def parse(inp):
    return [Particle(*numbers(line)) for line in inp.strip().splitlines()]

def maybe_show(particles, n, max_height):
    minx = min(p.px for p in particles)
    miny = min(p.py for p in particles)
    maxx = max(p.px for p in particles)
    maxy = max(p.py for p in particles)
    width = maxx - minx + 1
    height = maxy - miny + 1
    if height > max_height:
        return False
    lines = [['.' for x in range(width)] for y in range(height)]
    for p in particles:
        lines[p.py-miny][p.px-minx] = '#'
    print('\n'.join(''.join(line) for line in lines))
    print(f'{n}')
    return True

def move1(particles):
    for p in particles:
        p.px += p.vx
        p.py += p.vy

def play(inp, max_height=12):
    particles = parse(inp)
    n = 0
    while True:
        if maybe_show(particles, n, max_height):
            break
        move1(particles)
        n += 1

#play(example_input, 8)

with open('inputs/day10.input.txt') as f:
    real_input = f.read()
play(real_input) # => 10117
