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

    def play(self, goal):
        goal = [int(c) for c in f'{goal:05}']
        while True:
            r = sum(self.recipes[i] for i in self.players)
            ext = [int(c) for c in str(r)]
            for d in ext:
                self.recipes.append(d)
                if self.recipes[-len(goal):] == goal:
                    return len(self.recipes)-len(goal)
            for i in range(len(self.players)):
                self.players[i] += self.recipes[self.players[i]] + 1
                self.players[i] %= len(self.recipes)

assert (got := Kitchen().play(51589)) == 9, got
assert (got := Kitchen().play('01245')) == 5, got
assert (got := Kitchen().play('92510')) == 18, got
assert (got := Kitchen().play('59414')) == 2018, got

with open('inputs/day14.input.txt') as f:
    real_input = int(f.read())

print(Kitchen().play(real_input)) # => 20310465
