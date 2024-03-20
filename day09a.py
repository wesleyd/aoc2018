#!/usr/bin/env python3

import re

example_input = """
9 players; last marble is worth 25 points
"""

def string_state(circle, curr):
    lst = []
    for i, n in enumerate(circle):
        if i == curr:
            lst.append(f'({n})')
        else:
            lst.append(f' {n} ')
    return ' '.join(lst)

def play(inp):
    num_players, last_marble = [int(x) for x in re.findall(r'\d+', inp.strip())]
    scores = [0] * num_players
    circle = [0, 1]
    curr = 1
    next_player = 2
    next_marble = 2
    #print(f'[{next_player-1}]', string_state(circle, curr))
    while next_marble <= last_marble:
        if next_marble % 23 == 0:
            scores[next_player] += next_marble
            seven = (curr - 7) % len(circle)
            scores[next_player] += circle.pop(seven)
            curr = seven % len(circle)
        else:
            at = (curr + 1) % len(circle)
            at += 1
            circle.insert(at, next_marble)
            if at <= curr:
                curr += 1
            curr += 2
            curr %= len(circle)
        next_marble += 1
        next_player += 1
        next_player %= num_players
        #print(f'[{next_player-1}]', string_state(circle, curr))
    return max(scores)

assert (got := play('9 players; last marble is worth 25 points')) == 32, got
assert (got := play('10 players; last marble is worth 1618 points')) == 8317, got
assert (got := play('13 players; last marble is worth 7999 points')) == 146373, got
assert (got := play('21 players; last marble is worth 6111 points')) == 54718, got
assert (got := play('30 players; last marble is worth 5807 points')) == 37305, got

with open('inputs/day09.input.txt') as f:
    real_input = f.read()
print(play(real_input)) # => 388844
