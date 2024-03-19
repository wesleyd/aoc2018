#!/usr/bin/env python3

def react_without(polymer, without):
    polymer = polymer.replace(without.upper(), '')
    polymer = polymer.replace(without.lower(), '')
    i = 0
    while i < len(polymer)-1:
        a, b = polymer[i], polymer[i+1]
        if a != b and a.lower() == b.lower():
            polymer = polymer[:i] + polymer[i+2:]
            i = i-1 if i > 0 else i
        else:
            i += 1
    return polymer

def react(polymer):
    polymers = [react_without(polymer, c) for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    return min(polymers, key=lambda p: len(p))
assert (got := react('dabAcCaCBAcCcaDA')) == 'daDA', got

with open('inputs/day05.input.txt') as f:
    real_input = f.read().strip()
print(len(react(real_input)))  #  => 5446

