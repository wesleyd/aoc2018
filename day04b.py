#!/usr/bin/env python3

import math
import re

from dataclasses import dataclass

example_input = """
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
"""

def numbers(s):
    return [int(x) for x in re.findall(r'\d+', s)]

def total_asleep(sleeps):
    n = 0
    for zzz in sleeps:
        n += zzz[1] - zzz[0]
    return n

def parse(inp):
    g = None
    asleep = None
    guards = defaultdict(list)
    lines = inp.strip().splitlines()
    lines.sort()
    for line in lines:
        nn = numbers(line)
        t = tuple(nn[:5])
        if len(nn) == 6:
            g = nn.pop()
        elif 'falls' in line:
            asleep = int(t[4])
        elif 'wakes' in line:
            assert asleep is not None, line
            guards[g].append((asleep, int(t[4])))
            asleep = None
        else:
            assert False, f'bad line {line}, {nn}, {g}, {asleep}'
    return guards

def sleepiest_minute(sleeps):
    """Returns the minute most slept."""
    minutes = defaultdict(int)
    for sleep in sleeps:
        for t in range(sleep[0], sleep[1]):
            minutes[t] += 1
    sleepiest = None
    most_hits = -math.inf
    for t, hits in minutes.items():
        if hits > most_hits:
            most_hits = hits
            sleepiest = t
    return sleepiest, most_hits

def best_minute(guards):
    """Which minute is likeliest to find a guard asleep?"""
    sleepiest_guard = None
    sleepiest_t = None
    most_sleeps = -math.inf
    for g, sleeps in guards.items():
        t, hits = sleepiest_minute(sleeps)
        if hits > most_sleeps:
            most_sleeps = hits
            sleepiest_t = t
            sleepiest_guard = g
    return sleepiest_guard * sleepiest_t
assert (got := best_minute(parse(example_input))) == 4455, got

with open('inputs/day04.input.txt') as f:
    real_input = f.read()
print(best_minute(parse(real_input))) # => 128617
