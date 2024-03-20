#!/usr/bin/env python3

import re

from dataclasses import dataclass

example_input = """
9 players; last marble is worth 25 points
"""

@dataclass
class Node:
    value: int
    next: 'Node' = None
    prev: 'Node' = None

def string_state(zero, curr):
    lst = []
    p = zero
    while True:
        if p == curr:
            lst.append(f'({p.value})')
        else:
            lst.append(f' {p.value} ')
        p = p.next
        if p == zero:
            break
    return ' '.join(lst)

def play(inp):
    num_players, last_marble = [int(x) for x in re.findall(r'\d+', inp.strip())]
    last_marble *= 100
    circle = Node(0)
    circle.prev = circle
    circle.next = circle
    zero = circle
    scores = [0] * num_players
    marble = 1
    while marble <= last_marble:
        player = marble % num_players
        #print(f'[{player}]', string_state(zero, circle))
        if marble % 23 == 0:
            scores[player] += marble
            for i in range(7):
                circle = circle.prev
            scores[player] += circle.value
            circle.next.prev, circle.prev.next = circle.prev, circle.next
            circle = circle.next
        else:
            circle = circle.next
            p = Node(marble)
            p.prev, p.next = circle, circle.next
            circle.next.prev, circle.next = p, p
            circle = p
        marble += 1
    #print(f'[{player}]', string_state(zero, circle))
    return max(scores)

with open('inputs/day09.input.txt') as f:
    real_input = f.read()
print(play(real_input)) # => 3212081616
