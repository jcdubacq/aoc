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
    cache = {}

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
        self.cacheshort = {}
        if link:
            self.link = link
            link.backlink = self

    def __str__(self) -> str:
        return "Keypad " + self.id

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
        cls = type(self)
        if k in cls.cache:
            return cls.cache[k]
        l: list[str] = []
        if self.keys[ppos[1]][ppos[0]] == "?":
            l = []
            cls.cache[k] = l
            return l
        if npos == ppos:
            l = ["A"]
            cls.cache[k] = l
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
        cls.cache[k] = l
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

    def highlevel(self) -> "Pad":
        if self.backlink:
            return self.backlink.highlevel()
        return self

    def shortest(self, dial: str) -> int:
        self.position = self.start
        whereA = dial.find("A") + 1
        if whereA < len(dial):
            print("BUG!")
            sys.exit(0)
        result = 0
        for x in dial:
            npos = self.coords[ord(x)]
            ways = self.possiblepaths(self.position, npos)
            self.position = npos
            if self.backlink is None:
                result += len(ways[0])  # they are all of the same length
                continue
            cost = None
            for way in ways:
                test = self.backlink.shortestnum(way)
                if cost == None or test < cost:
                    cost = test
            assert cost is not None
            result += cost
        return result

    def shortestnum(self, dial: str) -> int:
        self.position = self.start
        whereA = dial.find("A") + 1
        if dial in self.cacheshort:
            return self.cacheshort[dial]
        if whereA < len(dial):
            return self.shortestnum(dial[:whereA]) + self.shortestnum(dial[whereA:])
        result = self.shortest(dial)
        self.cacheshort[dial] = result
        return result


class NumKeypad(Pad):
    cache = {}


class DirectionalKeypad(Pad):
    cache = {}


d0 = ["789", "456", "123", "?0A"]
d1 = ["?^A", "<v>"]
nkp = NumKeypad("numeric", d0)
last = nkp
for d in range(1, 26):
    last = DirectionalKeypad("directional " + str(d), d1, last)


for line in lines:
    nkp.backreset()
    robot = nkp.highlevel()
    x = nkp.shortestnum(line)
    score = int(line[:-1]) * x
    print(int(line[:-1]), "*", x)
    # robot.beginsimulation(x)
    # if nkp.typed != line:
    #     print(f"Panic! MISMATCH {nkp.typed} is not {line}")
    #     sys.exit(0)
    sum += score
print(sum)
sys.exit(0)
