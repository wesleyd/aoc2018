#!/usr/bin/env python3

import re

example_input = """
Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]
"""


OPCODES = [
    'addr',
    'addi',
    'mulr',
    'muli',
    'banr',
    'bani',
    'borr',
    'bori',
    'setr',
    'seti',
    'gtir',
    'gtri',
    'gtrr',
    'eqir',
    'eqri',
    'eqrr',
]

def step(rr, instr):
    match instr:
        case ('addr', A, B, C):
            rr[C] = rr[A] + rr[B]
        case ('addi', A, B, C):
            rr[C] = rr[A] + B
        case ('mulr', A, B, C):
            rr[C] = rr[A] * rr[B]
        case ('muli', A, B, C):
            rr[C] = rr[A] * B
        case ('banr', A, B, C):
            rr[C] = rr[A] & rr[B]
        case ('bani', A, B, C):
            rr[C] = rr[A] & B
        case ('borr', A, B, C):
            rr[C] = rr[A] | rr[B]
        case ('bori', A, B, C):
            rr[C] = rr[A] | B
        case ('setr', A, B, C):
            rr[C] = rr[A]
        case ('seti', A, B, C):
            rr[C] = A
        case('gtir', A, B, C):
            rr[C] = 1 if A > rr[B] else 0
        case('gtri', A, B, C):
            rr[C] = 1 if rr[A] > B else 0
        case('gtrr', A, B, C):
            rr[C] = 1 if rr[A] > rr[B] else 0
        case('eqir', A, B, C):
            rr[C] = 1 if A == rr[B] else 0
        case('eqri', A, B, C):
            rr[C] = 1 if rr[A] == B else 0
        case('eqrr', A, B, C):
            rr[C] = 1 if rr[A] == rr[B] else 0
    return rr

def numbers(s):
    return [int(x) for x in re.findall(r'\d+', s)]

def match_opcodes(before, instr, after):
    """Yields any opcodes that could cause before -> after."""
    for opcode in OPCODES:
        instr = instr[:]
        instr[0] = opcode
        got = step(before[:], instr)
        if got == after:
            yield opcode

def run(inp):
    sections = inp.split('\n\n\n')
    paragraphs = sections[0].strip().split('\n\n')
    n3 = 0
    for para in paragraphs:
        lines = para.split('\n')
        assert lines[0].startswith('Before:')
        before = numbers(lines[0])
        instr = numbers(lines[1])
        assert lines[2].startswith('After:')
        want = numbers(lines[2])
        possibles = list(match_opcodes(before, instr, want))
        if len(possibles) >= 3:
            n3 += 1
    return n3

assert (got := run(example_input)) == 1, got

with open('inputs/day16.input.txt') as f:
    real_input = f.read()
run(real_input)  # => 560
