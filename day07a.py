#!/usr/bin/env python3

import re

from collections import defaultdict

example_input = """
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
"""

line_re = r'Step ([A-Z]) must be finished before step ([A-Z]) can begin\.'

def parse(inp):
    all_steps = set()
    deps = defaultdict(set)
    for line in inp.strip().splitlines():
        m = re.match(line_re, line)
        before, after = m.group(1), m.group(2)
        deps[after].add(before)
        all_steps.add(before)
        all_steps.add(after)
    for step in all_steps:
        if step not in deps:
            deps[step] = set()
    return deps

def readies(deps):
    steps = []
    for after, befores in deps.items():
        if not befores:
            steps.append(after)
    steps.sort()
    return steps

def run(inp):
    order = []
    deps = parse(inp)
    while deps:
        c = readies(deps)[0]
        for after, before in deps.items():
            before.discard(c)
        del deps[c]
        order.append(c)
    return ''.join(order)

assert (got := run(example_input)) == 'CABDFE', got

with open('inputs/day07.input.txt') as f:
    real_input = f.read()
print(run(real_input)) # => BKCJMSDVGHQRXFYZOAULPIEWTN
