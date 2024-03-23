#!/usr/bin/env python3

from dataclasses import dataclass, field

@dataclass
class Kitchen:
    recipes: list[int] = field(default_factory=lambda: [3, 7])
    players: list[int] = field(default_factory=lambda: [0, 1])

    def __str__(self):
        ret = []
        for i, d in enumerate(self.recipes):
            if i == self.players[0]:
                ret.append(f'[{d}]')
            elif i == self.players[1]:
                ret.append(f'({d})')
            else:
                ret.append(f' {d} ')
        return ''.join(ret)

    def play(self, n=1):
        while len(self.recipes) < n:
            r = sum(self.recipes[i] for i in self.players)
            self.recipes.extend(int(c) for c in str(r))
            for i in range(len(self.players)):
                self.players[i] += self.recipes[self.players[i]] + 1
                self.players[i] %= len(self.recipes)

    def last10(self, after=5):
        n = after+10
        self.play(after+10)
        return ''.join(str(d) for d in self.recipes[after:after+10])

assert (got := Kitchen().last10(after=9)) == '5158916779', got
assert (got := Kitchen().last10(after=5)) == '0124515891', got
assert (got := Kitchen().last10(after=18)) == '9251071085', got
assert (got := Kitchen().last10(after=2018)) == '5941429882', got

with open('inputs/day14.input.txt') as f:
    real_input = int(f.read())

print(Kitchen().last10(after=real_input)) # => 5115114101
