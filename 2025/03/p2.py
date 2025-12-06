#!/usr/bin/python3
from operator import inv
import sys

lines = sys.stdin.readlines()


def find_joltage(line):
    digits = ""
    while len(line) > 0 and line[-1] not in "0123456789":
        line = line[:-1]
    if len(line) < 12:
        return 0  # empty line
    start = 0
    while len(digits) < 12:
        nosearch = 11 - len(digits)
        if nosearch > 0:
            subline = line[start:-nosearch]
        else:
            subline = line[start:]
        # print(f"{len(digits)}: Already got {digits}, Finding max in {subline}")
        current = str(max(set(int(x) for x in subline)))
        digits += current
        start = subline.find(current) + start + 1
    result = int(digits)
    # print(f"{line} => {result}")
    return result


sum = 0
for line in lines:
    sum += find_joltage(line)
print(sum)
