#!/usr/bin/python3
import sys

lines = sys.stdin.readlines()


class Lock:
    def __init__(self, pos=50, size=100) -> None:
        self.zero = 0
        self.value = pos
        self.size = size
        # print(f" - The dial starts by pointing at {self.value}.")

    def processline(self, line):
        val = int(line[1:])
        if line[0] == "L":
            val = -val
        self.value = (self.value + val) % self.size
        if self.value == 0:
            self.zero += 1
        # print(f" - The dial is rotated {line[:-1]} to point at {self.value}.")

    def processlines(self, lines):
        for i in lines:
            self.processline(i)


lock = Lock()

lock.processlines(lines)

print(lock.zero)
