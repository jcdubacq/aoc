#!/usr/bin/python3
import re
import sys

bold = "\x1b\x5b\x37\x6d"
norm = "\x1b\x5b\x32\x37\x6d"

constraints = {}
sum = 0

lines = []
origlines = sys.stdin.readlines()
for origline in origlines:
    if origline[-1] == "\n":
        x = origline[:-1]
    else:
        x = origline
    lines.append(x)


class Guard:
    delta = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}

    def __init__(self, x, y, d) -> None:
        self.xstart = x
        self.ystart = y
        self.sstate = d
        self.state = d
        self.x = x
        self.y = y
        self.visited = set()
        self.visiteddir = set()

    def update(self) -> bool:
        if self.state == "@":
            return False
        if (self.x, self.y, self.state) in self.visiteddir:
            return False
        self.visiteddir.add((self.x, self.y, self.state))
        self.visited.add((self.x, self.y))
        return True

    def speed(self):
        return Guard.delta[self.state]

    def move(self, terrain: "Terrain"):
        dx, dy = self.speed()
        print(
            f"x:{self.x}, y:{self.y}, v=({dx},{dy}), [{terrain.width}, {terrain.height}]"
        )
        if (
            self.x + dx >= terrain.width
            or self.x + dx < 0
            or self.y + dy >= terrain.height
            or self.y + dy < 0
        ):
            self.state = "@"
        else:
            if terrain.get(self.x + dx, self.y + dy) == ".":
                self.x += dx
                self.y += dy
            else:
                self.state = "><^v"["^v<>".find(self.state)]
                print(self.state)

    def __str__(self) -> str:
        return f"G{self.state}@{self.x},{self.y}"


class Terrain:
    def __init__(self, lines) -> None:
        self.g = [[c for c in l] for l in lines]
        self.height = len(lines)
        self.width = len(lines[0])
        for y in range(self.height):
            for x in range(self.width):
                if lines[y][x] != "." and lines[y][x] != "." and lines[y][x] in "<>^v":
                    d = lines[y][x]
                    self.guardian = Guard(x, y, d)
                    self.g[y][x] = "."
        assert self.guardian is not None

    def run(self):
        G = self.guardian
        while G.update():
            G.move(self)
        return G.visited

    def get(self, x, y):
        return self.g[y][x]

    def __str__(self) -> str:
        a = ""
        u = [l.copy() for l in self.g]
        n = self.guardian
        for v, w in n.visited:
            u[w][v] = "X"
        for y in range(self.height):
            a += "".join(u[y]) + "\n"
        return a


t = Terrain(lines)
visited = t.run()
print(str(t))
print(len(list(visited)))


sys.exit(0)
