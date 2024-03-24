#!/usr/bin/env python3

import copy
import re

from collections import namedtuple

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
    #print(f'Before {instr}, {rr=}')
    match instr:
        case ('addr', A, B, C): rr[C] = rr[A] + rr[B]
        case ('addi', A, B, C): rr[C] = rr[A] + B
        case ('mulr', A, B, C): rr[C] = rr[A] * rr[B]
        case ('muli', A, B, C): rr[C] = rr[A] * B
        case ('banr', A, B, C): rr[C] = rr[A] & rr[B]
        case ('bani', A, B, C): rr[C] = rr[A] & B
        case ('borr', A, B, C): rr[C] = rr[A] | rr[B]
        case ('bori', A, B, C): rr[C] = rr[A] | B
        case ('setr', A, B, C): rr[C] = rr[A]
        case ('seti', A, B, C): rr[C] = A
        case ('gtir', A, B, C): rr[C] = 1 if A > rr[B] else 0
        case ('gtri', A, B, C): rr[C] = 1 if rr[A] > B else 0
        case ('gtrr', A, B, C): rr[C] = 1 if rr[A] > rr[B] else 0
        case ('eqir', A, B, C): rr[C] = 1 if A == rr[B] else 0
        case ('eqri', A, B, C): rr[C] = 1 if rr[A] == B else 0
        case ('eqrr', A, B, C): rr[C] = 1 if rr[A] == rr[B] else 0
        case _: assert False, instr
    #print(f'After {instr}, {rr=}')
    return rr

def numbers(s):
    return [int(x) for x in re.findall(r'\d+', s)]

Snippet = namedtuple('Snippet', ['before', 'instr', 'after'])

def parse(inp):
    sections = inp.split('\n\n\n')
    snippets = []
    paragraphs = sections[0].strip().split('\n\n')
    for para in paragraphs:
        lines = para.split('\n')
        assert lines[0].startswith('Before:')
        before = tuple(numbers(lines[0]))
        instr = tuple(numbers(lines[1]))
        assert lines[2].startswith('After:')
        want = tuple(numbers(lines[2]))
        snippets.append(Snippet(before, instr, want))
    instrs = []
    if len(sections) >= 2:
        for line in sections[1].strip().splitlines():
            instrs.append(tuple(numbers(line)))
    return snippets, instrs

def match_opcodes(snippet):
    """Yields any opcodes that could cause before -> after."""
    for opcode in OPCODES:
        instr = list(snippet.instr)
        instr[0] = opcode
        got = tuple(step(list(snippet.before), instr))
        if got == snippet.after:
            yield opcode

def reduce(candidates, depth=0):
    """Tries to find which opcodes match which names."""
    singletons = set()
    for opcode in range(len(OPCODES)):
        if len(candidates[opcode]) == 1:
            singletons.add(opcode)
    while singletons:
        singleton = singletons.pop()
        only = next(iter(candidates[singleton]))
        for opcode in candidates:
            if opcode == singleton:
                continue
            if only in candidates[opcode]:
                candidates[opcode].remove(only)
                if len(candidates[opcode]) == 1:
                    singletons.add(opcode)
    if all([len(v) == 1 for v in candidates.values()]):
        yield candidates
    for k, v in candidates.items():
        if len(v) < 1:
            return
    for opcode in range(len(OPCODES)):
        if len(candidates[opcode]) == 1:
            continue
        prev = set(candidates[opcode])
        for cand in prev:
            candidates[opcode] = set([cand])
            yield from reduce(candidates,depth+1)
        candidates[opcode] = prev

def solve(snippets):
    candidates = {}
    for snippet in snippets:
        opcode = snippet.instr[0]
        cands = match_opcodes(snippet)
        if opcode in candidates:
            candidates[opcode] &= set(cands)
        else:
            candidates[opcode] = set(cands)
    for opcode, cands in candidates.items():
        if len(cands) == 1:  # Can only be this
            for opcode2, cands2 in candidates.items():
                if opcode2 == opcode:
                    continue
                cands2 -= cands
    for c in reduce(candidates):
        return {k: v.pop() for k, v in c.items()}

def run(inp):
    snippets, instrs = parse(inp)
    solution = solve(snippets)
    rr = [0, 0, 0, 0]
    for instrt in instrs:
        instr = list(instrt)
        instr[0] = solution[instr[0]]
        rr = step(rr, instr)
    return rr[0]

with open('inputs/day16.input.txt') as f:
    real_input = f.read()
print(run(real_input))  # => 622
