#!/usr/bin/python3
import re
import sys
from typing import Tuple, TypeAlias, Optional
import functools
import time

Coord: TypeAlias = Tuple[int, int]

bold = "\x1b\x5b\x37\x6d"
norm = "\x1b\x5b\x32\x37\x6d"
home = "\x1b\x5bH"
clear = "\x1b[H\x1b[2J\x1b[3J"

constraints = {}
sum = 0

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


class Pad:
    def __init__(
        self, id: str, keyset: list[str], link: Optional["Pad"] = None
    ) -> None:
        self.keys = keyset
        self.width = len(keyset[0])
        self.height = len(keyset)
        self.coords: dict[int, Coord] = {}
        for x in range(self.width):
            for y in range(self.height):
                self.coords[ord(keyset[y][x])] = (x, y)
        self.start = self.coords[65]
        self.position = self.start
        self.id = id
        self.typed = ""
        self.backlink: Optional[Pad] = None
        self.link: Optional[Pad] = None
        if link:
            self.link = link
            link.backlink = self
        self.cache = {}

    def __str__(self) -> str:
        return (
            "Keypad "
            + self.id
            + (" linked to " + (str(self.link)) if self.link else "")
        )

    def reset(self):
        self.position = self.start
        self.typed = ""
        if self.link:
            self.link.reset()

    def backreset(self):
        self.position = self.start
        self.typed = ""
        if self.backlink:
            self.backlink.backreset()

    def beginsimulation(self, dial: str):
        self.reset()
        print(f"Simulating '{dial}' on {str(self)}")
        self.simulate(dial)

    def possiblepaths(self, ppos: Coord, npos: Coord) -> list[str]:
        k = ppos[0] << 9 | ppos[1] << 6 | npos[0] << 3 | npos[1]
        if k in self.cache:
            return self.cache[k]
        l: list[str] = []
        if self.keys[ppos[1]][ppos[0]] == "?":
            l = []
            self.cache[k] = l
            return []
        if npos == ppos:
            l = ["A"]
            self.cache[k] = l
            return l
        if ppos[0] < npos[0]:
            news = (ppos[0] + 1, ppos[1])
            lx = [">" + v for v in self.possiblepaths(news, npos)]
            l.extend(lx)
        if ppos[0] > npos[0]:
            news = (ppos[0] - 1, ppos[1])
            lx = ["<" + v for v in self.possiblepaths(news, npos)]
            l.extend(lx)
        if ppos[1] < npos[1]:
            news = (ppos[0], ppos[1] + 1)
            lx = ["v" + v for v in self.possiblepaths(news, npos)]
            l.extend(lx)
        if ppos[1] > npos[1]:
            news = (ppos[0], ppos[1] - 1)
            lx = ["^" + v for v in self.possiblepaths(news, npos)]
            l.extend(lx)
        self.cache[k] = l
        return l

    def simulate(self, dial: str):
        nkp = self.position
        for key in dial:
            if key == "<":
                nkp = (nkp[0] - 1, nkp[1])
            elif key == ">":
                nkp = (nkp[0] + 1, nkp[1])
            elif key == "v":
                nkp = (nkp[0], nkp[1] + 1)
            elif key == "^":
                nkp = (nkp[0], nkp[1] - 1)
            elif key != "A":
                print(f"Panic! Trying to press {key} for {str(self)}")
                sys.exit(0)
            self.position = nkp
            try:
                c = self.keys[nkp[1]][nkp[0]]
            except KeyError:
                c = "?"
            if c == "?":
                print(f"Panic!…{key} {str(self)} @ {nkp}")
                sys.exit(0)
            if key == "A":
                print(f"{self.id}…{key}: Pressing {c}")
                self.typed += c
                if self.link:
                    self.link.simulate(c)
            else:
                print(f"{self.id}…{key}: Hovering over {c}")

    def shortest(self, dial: str) -> Tuple[str, "Pad"]:
        self.position = self.start
        result = ""
        highlevel = self
        for x in dial:
            npos = self.coords[ord(x)]
            ways = self.possiblepaths(self.position, npos)
            self.position = npos
            if self.backlink is None:
                result += ways[0]
                continue
            cost = None
            best = None
            for way in ways:
                test = self.backlink.shortest(way)
                if cost == None or len(test[0]) < cost:
                    best = test[0]
                    highlevel = test[1]
                    cost = len(best)
            assert best is not None
            result += best

        return (result, highlevel)


class NumKeypad(Pad):
    pass


class DirectionalKeypad(Pad):
    pass


d0 = ["789", "456", "123", "?0A"]
d1 = ["?^A", "<v>"]
nkp = NumKeypad("numeric", d0)
dkp = DirectionalKeypad("directional 1", d1, nkp)
ddkp = DirectionalKeypad("directional 2", d1, dkp)

sols = []
for line in lines:
    nkp.backreset()
    x, robot = nkp.shortest(line)
    sols.append(x)
    score = int(line[:-1]) * len(x)
    print(int(line[:-1]), "*", len(x))
    robot.beginsimulation(x)
    if nkp.typed != line:
        print(f"Panic! MISMATCH {nkp.typed} is not {line}")
        sys.exit(0)
    sum += score
print(sols)
print(sum)
sys.exit(0)
