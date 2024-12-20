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
                self.path.append(pos)
                break

    def set(self, x: int, y: int, v: str | None):
        if x not in self.d:
            self.d[x] = {}
        self.d[x][y] = v


    def get(self, x: int, y: int) -> str | None:
        if x < 0 or y < 0 or x>=self.width or y >= self.height:
            return("#")
        if x not in self.d:
            return None
        if y not in self.d[x]:
            return None
        return self.d[x][y]
    
    def shortcut(self,threshold):
        bylength = {}
        for i in range(len(self.path)):
            x,y=self.path[i]
            for dir in [(-1,0),(0,1),(1,0),(0,-1)]:
                if self.get(x+dir[0],y+dir[1])!='#':
                    continue
                if self.get(x+2*dir[0],y+2*dir[1]):
                    continue
                n = (x+2*dir[0],y+2*dir[1])
                try:
                    z = self.path.index(n,i)
                except ValueError:
                    continue
                if z>i+2+threshold-1:
                    if z-i-2 not in bylength:
                        bylength[z-i-2]=[]
                    bylength[z-i-2].append((self.path[i],n))
        return bylength



        

    def __str__(self) -> str:
        a = clear
        s = 0
        d = {}
        for y in range(self.height):
            for x in range(self.width):
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
threshold=100
l=t.shortcut(threshold)
sum=0
for le in sorted(l.keys()):
    print(f"{le}:{len(l[le])}")
    if le>=threshold:
        sum+=len(l[le])
print(sum)
sys.exit(0)