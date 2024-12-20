#!/usr/bin/python3
import re
import sys
from typing import Tuple, TypeAlias
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
        self.path : Path = []
        self.get_path()
    
    def get_path(self)->None:
        pos=self.start
        self.path.append(pos)
        while (pos!=self.end):
            for dir in [(-1,0),(0,1),(1,0),(0,-1)]:
                if self.get(pos[0]+dir[0],pos[1]+dir[1]):
                    continue
                n=(pos[0]+dir[0],pos[1]+dir[1])
                if len(self.path)>2 and n == self.path[-2]:
                    continue
                if n in self.path:
                    continue # should not happen
                pos = n
                break



    def set(self, x: int, y: int, v: str | None):
        if x not in self.d:
            self.d[x] = {}
        self.d[x][y] = v

    def get(self, x: int, y: int) -> str | None:
        if x < 0 or y > 0 or x>=self.width or y >= self.height:
            return("#")
        if x not in self.d:
            return None
        if y not in self.d[x]:
            return None
        return self.d[x][y]

    def __str__(self) -> str:
        a = clear
        s = 0
        d = {}
        arrows = ">^<v"
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
        return a


t = Terrain(lines)
print(str(t))
sys.exit(0)
