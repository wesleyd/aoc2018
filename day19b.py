#!/usr/bin/env python3

example_input = """
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
"""

def parse1(s):
    instr = s.split()
    for i, s in enumerate(instr):
        try:
            instr[i] = int(s)
        except ValueError:
            instr[i] = s
    return tuple(instr)

class CPU:
    def __init__(self, inp):
        self.instrs = []
        self.rr = [0] * 6
        self.rr[0] = 1
        for line in inp.strip().splitlines():
            instr = parse1(line)
            if instr[0] == '#ip':
                self.ip = instr[1]
            else:
                self.instrs.append(instr)

    def pc(self):
        return self.rr[self.ip]

    def step(self):
        op, A, B, C = self.instrs[self.pc()]
        match op:
            case 'addr': self.rr[C] = self.rr[A] + self.rr[B]
            case 'addi': self.rr[C] = self.rr[A] + B
            case 'mulr': self.rr[C] = self.rr[A] * self.rr[B]
            case 'muli': self.rr[C] = self.rr[A] * B
            case 'banr': self.rr[C] = self.rr[A] & self.rr[B]
            case 'bani': self.rr[C] = self.rr[A] & B
            case 'borr': self.rr[C] = self.rr[A] | self.rr[B]
            case 'bori': self.rr[C] = self.rr[A] | B
            case 'setr': self.rr[C] = self.rr[A]
            case 'seti': self.rr[C] = A
            case 'gtir': self.rr[C] = 1 if A > self.rr[B] else 0
            case 'gtri': self.rr[C] = 1 if self.rr[A] > B else 0
            case 'gtrr': self.rr[C] = 1 if self.rr[A] > self.rr[B] else 0
            case 'eqir': self.rr[C] = 1 if A == self.rr[B] else 0
            case 'eqri': self.rr[C] = 1 if self.rr[A] == B else 0
            case 'eqrr': self.rr[C] = 1 if self.rr[A] == self.rr[B] else 0
            # remainder relative
            case 'remr':
                self.rr[C] = self.rr[A] % self.rr[B]
            case 'nop': pass
            case _: assert False, (op, self.rr)
        self.rr[self.ip] += 1

    def run(self):
        self.optimize()
        while 0 <= self.pc() < len(self.instrs):
            rr = self.rr[:]
            self.step()
        return self.rr

    def optimize(self):
        """Optimize out the 'is divisible by' function."""
        for i in range(len(self.instrs)-10):
            if self.instrs[i:i+10] == [
                    parse1('seti 1 7 5'),
                    parse1('mulr 1 5 4'),
                    parse1('eqrr 4 2 4'),
                    parse1('addr 4 3 3'),
                    parse1('addi 3 1 3'),
                    #
                    parse1('addr 1 0 0'),
                    parse1('addi 5 1 5'),
                    parse1('gtrr 5 2 4'),
                    parse1('addr 3 4 3'),
                    parse1('seti 2 2 3'),
                ]:
                self.instrs[i:i+10] = [
                    parse1('remr 2 1 5'),
                    parse1('gtri 5 0 4'),
                    parse1('addr 3 4 3'),
                    parse1('addr 0 1 0'),
                    parse1('nop 0 0 0'),
                    #
                    parse1('nop 0 0 0'),
                    parse1('nop 0 0 0'),
                    parse1('nop 0 0 0'),
                    parse1('nop 0 0 0'),
                    parse1('nop 0 0 0')]

with open('inputs/day19.input.txt') as f:
    real_input = f.read()
print(CPU(real_input).run()[0]) # => 2223
