#!/usr/bin/python3
import sys
import math

lines = sys.stdin.readlines()


class Lock:
    def __init__(self, pos=50, size=100) -> None:
        self.zero: int = 0
        self.clicks = 0
        self.value: int = pos
        self.size: int = size
        print(f" - The dial starts by pointing at {self.value}.")

    def processclick(self, direction):
        self.value += direction
        if self.value == 100:
            self.value = 0
        elif self.value < 0:
            self.value += 100
        if self.value == 0:
            self.clicks += 1

    def processline(self, line):
        val = int(line[1:])
        dir = 1
        if line[0] == "L":
            dir = -1
        for i in range(val):
            self.processclick(dir)
        self.zero += self.clicks
        print(
            f" - The dial is rotated {line[:-1]} to point at {self.value} ; it clicked to zero {self.clicks} time."
        )
        self.clicks = 0

    def processlines(self, lines):
        for i in lines:
            self.processline(i)


lock = Lock()

lock.processlines(lines)

print(lock.zero)
