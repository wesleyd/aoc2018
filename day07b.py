#!/usr/bin/env python3

import re

from collections import defaultdict, deque
from heapdict import heapdict

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
    return dict(deps)

def work(inp, delay, num_elves):
    deps = parse(inp)
    # A given task is in exactly one of blocked, ready, working or done.
    blocked = set()
    ready = deque()
    working = heapdict()
    done = set()
    for after in deps:
        blocked.add(after)
    t = 0
    while True:
        #print(f'{t=} {blocked=} {ready=} working={list(working.items())} {done=}')
        happened = False
        for x in deps:
            if x not in blocked:
                continue
            undone = deps[x] - done
            #print(f'{x=}: {undone=}')
            if undone:
                continue
            blocked.remove(x)
            ready.append(x)
            happened = True
            #print(f'{x=} moved from blocked to ready')
        while ready and len(working) < num_elves:
            x = ready.popleft()
            assert x not in working, (x, working)
            w = t + ord(x) - ord('A') + 1 + delay
            working[x] = w
            #print(f'{x=} moved from ready to working, scheduled for {w=}')
            happened = True
        while working:
            x, w = working.peekitem()
            if w > t:
                break
            assert w == t, (w, t)
            working.popitem()
            done.add(x)
            #print(f'Done {x=} at {t=} ({w=})')
            happened = True
        if not blocked and not ready and not working:
            return t
        if not happened: 
            _, t = working.peekitem()

assert (got := work(example_input, 0, 2)) == 15, got


with open('inputs/day07.input.txt') as f:
    real_input = f.read()
print(work(real_input, 60, 5)) # => 1040
