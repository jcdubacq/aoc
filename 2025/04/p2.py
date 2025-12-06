#!/usr/bin/python3
import sys

lines = sys.stdin.readlines()


class StorageRoom:
    def __init__(self, lines):
        ref = lines[0]
        w = len(ref)
        self.map = {}
        while ref[w - 1] not in "@.":
            w -= 1
        self.w = w
        h = 0
        for l in lines:
            if len(l) >= w:
                self.map[h] = l[0:w]
                h += 1
        self.h = h

    def get(self, x, y):
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            return False
        return ord(self.map[y][x]) == 64  # "@"

    def remove(self, x, y):
        if not (x < 0 or x >= self.w or y < 0 or y >= self.h):
            self.map[y] = self.map[y][:x] + "." + self.map[y][x + 1 :]

    def neighborhood(self, x, y):
        a = 0
        for dx, dy in [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]:
            if self.get(x + dx, y + dy):
                a += 1
        return a

    def accessible(self):
        a = 0
        for y in range(self.h):
            for x in range(self.w):
                if self.get(x, y):
                    if self.neighborhood(x, y) < 4:
                        a += 1
        return a

    def accessible_and_remove(self):
        a = 0
        l = []
        for y in range(self.h):
            for x in range(self.w):
                if self.get(x, y):
                    if self.neighborhood(x, y) < 4:
                        a += 1
                        l.append((x, y))
        for x, y in l:
            self.remove(x, y)
        return a

    def __str__(self) -> str:
        a = ""
        for y in range(self.h):
            for x in range(self.w):
                if self.get(x, y):
                    if self.neighborhood(x, y) < 4:
                        a += "x"
                    else:
                        a += "@"
                else:
                    a += "."
            a += "\n"
        return a


room = StorageRoom(lines)
sum = 0

while True:
    removed = room.accessible_and_remove()
    if removed == 0:
        break
    sum += removed

print(sum)
