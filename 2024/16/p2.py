#!/usr/bin/python3
import re
import sys
from typing import Tuple, TypeAlias
import time

Path: TypeAlias = list[int, int, int]

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


class Terrain:
    def __init__(self, lines) -> None:
        g = [[c for c in l] for l in lines]
        self.d = {}
        self.height = len(lines)
        self.width = len(lines[0])
        self.start: Tuple[int, int] = (-1, -1)
        self.end: Tuple[int, int] = (-1, -1)
        for y in range(self.height):
            for x in range(self.width):
                if lines[y][x] == "#":
                    self.set(x, y, "#")
                elif lines[y][x] == "S":
                    self.start = (x, y)
                elif lines[y][x] == "E":
                    self.end = (x, y)
        self.paths: list[Path] = [[(self.start[0], self.start[1], 0)]]
        self.scores: list[int] = [0]
        self.answer: Path = None
        self.score = 0

    def extend_paths(self) -> bool:
        arrows = ">^<v"
        dirs = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        minscore = min(self.scores)
        idx = self.scores.index(minscore)
        path = self.paths.pop(idx)
        self.scores.pop(idx)
        last = path[-1]
        # weed out bad paths:
        i = len(self.paths)
        while i > 0:
            if self.paths[i - 1][-1] in path:
                altpath = self.paths[i - 1]
                merge = False
                if self.scores[i - 1] == minscore and altpath[-1] == last:
                    merge = True
                if (
                    self.scores[i - 1] == minscore
                    and last[0] == self.end[0]
                    and altpath[-1][0] == self.end[0]
                    and last[1] == self.end[1]
                    and altpath[-1][1] == self.end[1]
                ):
                    merge = True  # the last merge can ignore the direction
                if merge:
                    path = list(set(path).union(altpath))
                del self.paths[i - 1]
                del self.scores[i - 1]
            i -= 1
        self.answer = path
        self.score = minscore
        # print("Pondering:\n"+str(self))
        if (last[0], last[1]) == self.end:
            return False
        for delta in range(len(dirs)):
            # print(f"{delta}:{arrows[delta]} ",end="")
            if (delta + 2) % 4 == last[2]:
                # print("No")
                continue  # No turning backward
            newx = last[0] + dirs[delta][0]
            newy = last[1] + dirs[delta][1]
            if (newx, newy) in path:
                # print("Looping")
                continue
            p = self.get(newx, newy)
            if p:
                # print("Wall")
                continue
            np = [x for x in path]
            np.append((newx, newy, delta))
            self.paths.append(np)
            self.scores.append(minscore + (1 if delta == last[2] else 1001))
            # print("New path")
        return True

    def set(self, x: int, y: int, v: str | None):
        if x not in self.d:
            self.d[x] = {}
        self.d[x][y] = v

    def get(self, x: int, y: int) -> str | None:
        if x not in self.d:
            return None
        if y not in self.d[x]:
            return None
        return self.d[x][y]

    def __str__(self) -> str:
        a = clear
        s = 0
        d = {}
        arrows = "OOOO"
        if self.answer:
            for u in self.answer:
                pl = (u[0], u[1])
                if pl not in d:
                    d[pl] = arrows[u[2]]
                    s += 1

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in d:
                    c = d[(x, y)]
                else:
                    c = self.get(x, y)
                if self.start == (x, y) or self.end == (x, y):
                    a += bold
                if c:
                    a += c
                elif self.start == (x, y):
                    a += "S"
                elif self.end == (x, y):
                    a += "E"
                else:
                    a += " "
                if self.start == (x, y) or self.end == (x, y):
                    a += norm
            a += "\n"
        a += f"Score: {self.score}"
        a += f"\nPlaces: {s}"
        return a

    def topgm(self) -> str:
        a = f"P2 {self.width} {self.height} 3\n"
        s = 0
        d = {}
        arrows = "OOOO"
        if self.answer:
            for u in self.answer:
                pl = (u[0], u[1])
                if pl not in d:
                    d[pl] = arrows[u[2]]
                    s += 1

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in d:
                    a += "0 "
                else:
                    c = self.get(x, y)
                    if c:
                        a += "2 "
                    else:
                        a += "3 "
            a += "\n"
        return a


t = Terrain(lines)
print(str(t))
while t.extend_paths():
    print(clear)
    print(t.score)
    print(len(t.paths))
print(clear + str(t))
print(t.score)
with open("result.pgm", "w") as f:
    print(t.topgm(), file=f)
sys.exit(0)
