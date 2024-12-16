#!/usr/bin/python3
from __future__ import annotations
import re
import sys
from typing import Tuple

bold = "\x1b\x5b\x37\x6d"
norm = "\x1b\x5b\x32\x37\x6d"
home = "\x1b\x5bH"

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
        self.attached: list[Bidule] = []
        return None

    def newp(self, v: Tuple[int, int]) -> Tuple[int, int]:
        return (self.x + v[0], self.y + v[1])

    def push(
        self, direction: str, already_moving: set[Bidule] = set(), why="?"
    ) -> Tuple[bool, set[Bidule]]:
        if self in already_moving:
            return (True, already_moving)
        if direction not in Bidule.dirs:
            return (False, set())
        v = Bidule.dirs[direction]
        what = self.t.get(*self.newp(v))
        if what is not None and what not in already_moving:
            possible, tomove = what.push(
                direction, set(already_moving), f"pushed by {self}{self.x},{self.y}"
            )
            if not possible:
                return (False, set())
            already_moving = tomove.union(already_moving)
        already_moving.add(self)
        for n in self.attached:
            attpossible, tomove = n.push(
                direction, already_moving, f"attached to {self}{self.x},{self.y}"
            )
            if not attpossible:
                return (False, set())
            already_moving = already_moving.union(tomove)
        return (True, already_moving)

    def score(self) -> int:
        return 0

    def __str__(self) -> str:
        return "?"


class BoxLeft(Bidule):
    def __init__(self, terrain, x, y) -> None:
        super().__init__(terrain, x, y)
        self.attached = [BoxRight(terrain, x + 1, y, self)]
        terrain.set(x + 1, y, self.attached[0])

    def __str__(self) -> str:
        return "["

    def score(self) -> int:
        return 100 * self.y + self.x


class BoxRight(Bidule):
    def __init__(self, terrain, x, y, left: BoxLeft) -> None:
        super().__init__(terrain, x, y)
        self.attached = [left]

    def __str__(self) -> str:
        return "]"

    def score(self) -> int:
        return 0


class Robot(Bidule):
    def __str__(self) -> str:
        return "@"


class Wall(Bidule):
    def push(
        self, direction, already_moving: set[Bidule] = set(), why="?"
    ) -> Tuple[bool, set[Bidule]]:
        return (False, set())

    def __str__(self) -> str:
        return "#"


class Terrain:
    def __init__(self, lines) -> None:
        g = [[c for c in l] for l in lines]
        self.d = {}
        self.height = len(lines)
        self.width = 2 * len(lines[0])
        for y in range(self.height):
            for x in range(self.width // 2):
                if lines[y][x] == "#":
                    self.set(2 * x, y, Wall(self, 2 * x, y))
                    self.set(2 * x + 1, y, Wall(self, 2 * x + 1, y))
                elif lines[y][x] == "O":
                    self.set(2 * x, y, BoxLeft(self, 2 * x, y))
                elif lines[y][x] == "@":
                    self.robot: Robot = Robot(self, 2 * x, y)
                    self.set(2 * x, y, self.robot)
        assert self.robot is not None

    def set(self, x: int, y: int, v: Bidule | None):
        if x not in self.d:
            self.d[x] = {}
        self.d[x][y] = v

    def get(self, x: int, y: int) -> Bidule | None:
        if x not in self.d:
            return None
        if y not in self.d[x]:
            return None
        return self.d[x][y]

    def move(self, direction, movelist: set[Bidule]):
        for u in movelist:
            self.set(u.x, u.y, None)
        for u in movelist:
            u.x, u.y = u.newp(u.dirs[direction])
            self.set(u.x, u.y, u)

    def execute(self, instructions: str):
        print(f"Execution {instructions}")
        for i in instructions:
            move, what = self.robot.push(i, set())
            if move:
                self.move(i, what)
            print(home+str(self))
        print(str(self))

    def __str__(self) -> str:
        a = ""
        s = 0
        for y in range(self.height):
            x = 0
            while x < self.width:
                c = self.get(x, y)
                if c:
                    cc = str(c)
                    a += cc
                    x += len(cc)
                    s += c.score()
                else:
                    a += "."
                    x += 1
            a += "\n"
        a += f"Score: {s}"
        return a


t = Terrain(lines)
print(str(t))
t.execute(instructions)

sys.exit(0)
