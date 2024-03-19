#!/usr/bin/env python3

def react(polymer):
    i = 0
    while i < len(polymer)-1:
        a, b = polymer[i], polymer[i+1]
        if a != b and a.lower() == b.lower():
            polymer = polymer[:i] + polymer[i+2:]
            i = i-1 if i > 0 else i
        else:
            i += 1
    return polymer

assert (got := react('aA')) == '', got
assert (got := react('abBA')) == '', got
assert (got := react('abAB')) == 'abAB', got
assert (got := react('aabAAB')) == 'aabAAB', got
assert (got := react('dabAcCaCBAcCcaDA')) == 'dabCBAcaDA', got

with open('inputs/day05.input.txt') as f:
    real_input = f.read().strip()
print(len(react(real_input)))  # 11476
