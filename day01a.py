#!/usr/bin/env python3

with open('inputs/day01.input.txt') as f:
    real_input = f.read()

def run(inp):
    return sum(int(x) for x in inp.strip().splitlines())

print(run(real_input)) # => 408
