#!/usr/bin/python3
import re
import sys
from typing import Tuple, TypeAlias, Optional
import time

Path: TypeAlias = list[Tuple[int, int]]

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

size = 71
if len(sys.argv) > 1:
    size = int(sys.argv[1]) + 1

timelimit = 1024
if len(sys.argv) > 2:
    timelimit = int(sys.argv[2])


class Terrain:
    def __init__(self, size: int) -> None:
        g = [[c for c in l] for l in lines]
        self.d = {}
        self.height = size
        self.width = size
        self.start: Tuple[int, int] = (0, 0)
        self.end: Tuple[int, int] = (self.height - 1, self.width - 1)
        self.paths: list[Path] = [[(self.start[0], self.start[1])]]
        self.scores: list[int] = [0]
        self.answer: Optional[Path] = None
        self.score = 0

    def read_walls(self, lines, limit=None) -> None:
        lim = 0
        for line in lines:
            if limit is not None and lim == limit:
                break
            l = line.split(",")
            if len(l) == 2:
                x, y = int(l[0]), int(l[1])
                lim += 1
                self.set(x, y, "#")

    def extend_paths(self) -> bool:
        arrows = ">^<v"
        dirs = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        minscore = min(self.scores)
        idx = self.scores.index(minscore)
        path = self.paths.pop(idx)
        self.scores.pop(idx)
        last = path[-1]
        self.answer = path
        self.score = minscore
        # weed out bad paths:
        i = len(self.paths)
        while i > 0:
            if self.paths[i - 1][-1] in path:
                del self.paths[i - 1]
                del self.scores[i - 1]
            i -= 1

        # print("Pondering:\n"+str(self))
        if last == self.end:
            return False
        for delta in range(len(dirs)):
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
            np.append((newx, newy))
            self.paths.append(np)
            self.scores.append(minscore + 1)
            # print("New path")
        return True

    def set(self, x: int, y: int, v: str | None):
        if x not in self.d:
            self.d[x] = {}
        self.d[x][y] = v

    def get(self, x: int, y: int) -> str | None:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return "#"
        if x not in self.d:
            return None
        if y not in self.d[x]:
            return None
        return self.d[x][y]

    def __str__(self) -> str:
        a = ""
        s = 0
        d = {}
        if self.answer:
            for u in self.answer:
                d[(u[0], u[1])] = "O"
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
                    a += "."
                if self.start == (x, y) or self.end == (x, y):
                    a += norm
            a += "\n"
        a += f"Score: {self.score}"
        return a


t = Terrain(size)
t.read_walls(lines, timelimit)
print(str(t))
while t.extend_paths():
    # print(str(t))
    print(clear)
    print(t.score)
    print(len(t.paths))
print(clear + str(t))
print(t.score)
