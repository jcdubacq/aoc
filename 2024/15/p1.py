#!/usr/bin/python3
import re
import sys

bold = "\x1b\x5b\x37\x6d"
norm = "\x1b\x5b\x32\x37\x6d"

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


class Bidule:
    dirs = {
        "^": (0, -1),
        "v": (0, 1),
        "<": (-1, 0),
        ">": (1, 0),
    }

    def __init__(self, terrain, x, y) -> None:
        self.x = x
        self.y = y
        self.t: Terrain = terrain
        return None

    def push(self, direction: str) -> bool:
        if direction not in Bidule.dirs:
            return False
        v = Bidule.dirs[direction]
        newx = self.x + v[0]
        newy = self.y + v[1]
        what = self.t.get(newx, newy)
        possible = True
        if what:
            possible = what.push(direction)
        if possible:
            self.t.set(newx, newy, self)
            self.t.set(self.x, self.y, None)
            self.x = newx
            self.y = newy
        return possible

    def score(self) -> int:
        return 0

    def __str__(self) -> str:
        return "?"


class Box(Bidule):
    def __str__(self) -> str:
        return "O"

    def score(self) -> int:
        return 100 * self.y + self.x


class Robot(Bidule):
    def __str__(self) -> str:
        return "@"


class Wall(Bidule):
    def push(self, direction):
        return False

    def __str__(self) -> str:
        return "#"


class Terrain:
    def __init__(self, lines) -> None:
        g = [[c for c in l] for l in lines]
        self.d = {}
        self.height = len(lines)
        self.width = len(lines[0])
        for y in range(self.height):
            for x in range(self.width):
                if lines[y][x] == "#":
                    self.set(x, y, Wall(self, x, y))
                elif lines[y][x] == "O":
                    self.set(x, y, Box(self, x, y))
                elif lines[y][x] == "@":
                    self.robot: Robot = Robot(self, x, y)
                    self.set(x, y, self.robot)
        assert self.robot is not None

    def set(self, x: int, y: int, v: Bidule | None):
        if x not in self.d:
            self.d[x] = {}
        self.d[x][y] = v

    def get(self, x: int, y: int):
        if x not in self.d:
            return None
        if y not in self.d[x]:
            return None
        return self.d[x][y]

    def execute(self, instructions: str):
        print(f"Execution {instructions}")
        for i in instructions:
            self.robot.push(i)
        print(str(self))

    def __str__(self) -> str:
        a = ""
        s = 0
        for y in range(self.height):
            for x in range(self.width):
                c = self.get(x, y)
                if c:
                    a += str(c)
                    s += c.score()
                else:
                    a += "."
            a += "\n"
        a += f"Score: {s}"
        return a


t = Terrain(lines)
t.execute(instructions)

sys.exit(0)
