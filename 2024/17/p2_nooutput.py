#!/usr/bin/python3
import re
import sys
from typing import Tuple, TypeAlias
import time


bold = "\x1b\x5b\x37\x6d"
norm = "\x1b\x5b\x32\x37\x6d"
home = "\x1b\x5bH"
clear = "\x1b[H\x1b[2J\x1b[3J"

rre = re.compile(r"^Register ([ABC]): ([0-9]*)")
pre = re.compile(r"^Program: ([0-9,]*)")

lines = []
origlines = sys.stdin.readlines()
instructions = ""
# two parts
first = True
for origline in origlines:
    if origline[-1] == "\n":
        x = origline[:-1]
    else:
        x = origline
    if len(x) > 0:
        if first:
            lines.append(x)
        else:
            instructions += x
    else:
        first = False


class LifeError(Exception):
    pass


class MismatchError(Exception):
    pass


class Machine:
    trad = ["adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv", "ERR"]
    content = [0, 2, 1, 2, 3, 1, 0, 0]

    def __init__(self) -> None:
        self.life: int = 0
        self.a: int = 0
        self.b: int = 0
        self.c: int = 0
        self.program = list()
        self.pc = 0
        self.steps = 0
        self.out = []

    def setr(self, r: str, v: int):
        if r == "A":
            self.a = v
        elif r == "B":
            self.b = v
        else:
            self.c = v

    def godeep(self, a, life):
        # Returning value means : initial value has been found
        # Returning None means : abandon this branch, all possibilities have been explored
        self.reset(a, life)
        x = 0
        running = True
        mismatch = False
        outoflife = False
        while running:
            test = self.run()
            if test == 0:  # FINISHED
                running = False
            if test == 1:  # NORMAL
                if len(self.out) > x:
                    x += 1
                    if (
                        len(self.program) < len(self.out)
                        or self.out[x - 1] != self.program[x - 1]
                    ):
                        mismatch = True
                        running = False
            if test == 2:  # NO LIFE
                running = False
                outoflife = True
        if mismatch:
            return None
        if outoflife:
            d = 14
            for i in range(1 << d):
                newa = i << life | a
                u = self.godeep(newa, life + d)
                if u:
                    return u
            return None
        if len(self.out) == len(self.program):
            return a
        # Program ended, but not enough outputs. We need a higher value of a

    def run(self):
        self.steps += 1
        if self.pc > len(self.program) - 1:
            return 0
        opcode = self.program[self.pc]
        combo = self.program[self.pc + 1]
        litt = combo
        if combo == 4:
            combo = self.a
        elif combo == 5:
            combo = self.b
        elif combo == 6:
            combo = self.c
        self.pc += 2
        if opcode == 0:
            self.life -= combo
            if self.life < 0:
                return 2
            self.a = self.a >> combo
        elif opcode == 1:
            self.b = self.b ^ litt
        elif opcode == 2:
            if litt == 4 and self.life < 3:
                return 2
            self.b = combo % 8
        elif opcode == 3:
            if self.life < 8:
                return 2
            if self.a != 0:
                self.pc = litt
        elif opcode == 4:
            self.b = self.b ^ self.c
        elif opcode == 5:
            # out is only used with B
            self.out.append(combo % 8)
        elif opcode == 6:
            if self.life < combo:
                return 2
            self.b = self.a >> combo
        elif opcode == 7:
            if self.life < combo:
                return 2
            self.c = self.a >> combo
        return 1

    def reset(self, a, life):
        self.a = a
        self.life = life
        self.b = 0
        self.c = 0
        self.pc = 0
        self.out = []
        self.steps = 0

    def __str__(self) -> str:
        a = f"Register A: {bin(self.a)}={self.a}\nRegister B: {bin(self.b)}={self.b}\nRegister C: {bin(self.c)}={self.c}\nPC={self.pc}\n"
        for u in range(len(self.program)):
            if u == self.pc:
                a += bold + bin(8 + self.program[u])[3:] + norm + ","
            else:
                a += bin(8 + self.program[u])[3:] + ","
        a += f"\nSteps: {self.steps}\nOutput: " + ",".join([str(x) for x in self.out])
        return a


m = Machine()
for line in lines:
    r = rre.match(line)
    if r:
        m.setr(r.group(1), int(r.group(2)))
p = pre.match(instructions)
assert p is not None
m.program = list(map(int, p.group(1).split(",")))

print(m.godeep(0, 0))

sys.exit(0)
