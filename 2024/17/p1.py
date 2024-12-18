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


class Machine:
    trad = ["adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv", "ERR"]
    content = [0, 2, 1, 2, 3, 1, 0, 0]

    def __init__(self) -> None:
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

    def run(self):
        self.steps += 1
        if self.pc > len(self.program) - 1:
            return False
        opcode = self.program[self.pc]
        combo = self.program[self.pc + 1]
        litt = combo
        if combo == 4:
            combo = self.a
        elif combo == 5:
            combo = self.b
        elif combo == 6:
            combo = self.c
        l = [combo, combo % 8, litt, "-"]
        uuu = str(l[self.content[opcode]])
        print(f"{Machine.trad[opcode]} {uuu}")
        self.pc += 2
        if opcode == 0:
            self.a = self.a >> combo
        elif opcode == 1:
            self.b = self.b ^ litt
        elif opcode == 2:
            self.b = combo % 8
        elif opcode == 3:
            if self.a != 0:
                self.pc = litt
        elif opcode == 4:
            self.b = self.b ^ self.c
        elif opcode == 5:
            self.out.append(str(combo % 8))
        elif opcode == 6:
            self.b = self.a >> combo
        elif opcode == 7:
            self.c = self.a >> combo
        return True

    def prog(self):
        ll = []
        for i in range(0, len(self.program), 2):
            opcode = self.program[i]
            combo = self.program[i + 1]
            litt = combo
            if combo == 4:
                combo = "A"
            elif combo == 5:
                combo = "B"
            elif combo == 6:
                combo = "C"
            l = [str(combo), str(combo) + "%8", bin(litt), "-"]
            ll.append(f"{Machine.trad[opcode]} {l[Machine.content[opcode]]}")
        return ll

    def __str__(self) -> str:
        a = f"Register A: {bin(self.a)}={self.a}\nRegister B: {bin(self.b)}={self.b}\nRegister C: {bin(self.c)}={self.c}\nPC={self.pc}\n"
        for u in range(len(self.program)):
            if u == self.pc:
                a += bold + bin(8 + self.program[u])[3:] + norm + ","
            else:
                a += bin(8 + self.program[u])[3:] + ","
        a += f"\nSteps: {self.steps}\nOutput: " + ",".join(self.out)
        return a


m = Machine()
for line in lines:
    r = rre.match(line)
    if r:
        m.setr(r.group(1), int(r.group(2)))
p = pre.match(instructions)
assert p is not None
print("-" * 72)
m.program = list(map(int, p.group(1).split(",")))
print("\n".join(m.prog()))
while m.run():
    print(str(m))
sys.exit(0)
