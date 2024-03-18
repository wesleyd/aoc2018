#!/usr/bin/env python3

with open('inputs/day01.input.txt') as f:
    real_input = f.read()

def run(inp):
    return [int(x) for x in inp.strip().splitlines()]

real_input.strip().splitlines()

print(run(real_input))
