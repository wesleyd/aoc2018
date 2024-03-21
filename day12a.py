#!/usr/bin/env python3

example_input = """
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
"""

class State:
    def __init__(self, s):
        self.s = s
        self.l = 0
    def step(self, rules):
        s = '.....' + self.s + '.....'
        l = self.l - 3
        t = []
        for i in range(2, len(s)-2):
            t.append('#' if s[i-2:i+3] in rules else '.')
        n = 0
        while t[n] == '.':
            l += 1
            n += 1
        self.l = l
        self.s = ''.join(t[n:]).rstrip('.')
    def score(self):
        n = 0
        for i, c in enumerate(self.s):
            if c == '#':
                n += i+self.l
        return n

def parse(inp):
    paras = inp.strip().split('\n\n')
    initial_state = State(paras[0].split(':')[1].strip())
    rules = set()
    for line in paras[1].strip().splitlines():
       if line.endswith('#'):
           rules.add(line[:5])
    return rules, initial_state

def run(inp, iters=20):
    rules, st = parse(inp)
    #print(f' 0: {st.s} {st.l}')
    for i in range(1,iters+1):
        st.step(rules)
        #print(f'{i:2}: {st.s} {st.l}')
    return st.score()

assert (got := run(example_input)) == 325, got

with open('inputs/day12.input.txt') as f:
    real_input = f.read()
print(run(real_input)) # => 4818

