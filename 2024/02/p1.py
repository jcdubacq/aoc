#!/usr/bin/python3
import re
import sys

bold = "\x1b\x5b\x37\x6d"
norm = "\x1b\x5b\x32\x37\x6d"

safe = 0

origlines = sys.stdin.readlines()
lines = []
for origline in origlines:
    if origline[-1] == "\n":
        x = origline[:-1]
    else:
        x = origline
    if len(x) == 0:
        continue
    lines.append(x)

for line in lines:
    if line[-1] == "\n":
        line = line[:-1]
        print(line)
    if len(line) == 0:
        continue
    cols = [int(x) for x in line.split(" ")]
    if len(cols) == 0:
        continue
    if len(cols) == 1:
        safe += 1
        continue
    xsafe = True
    asc = 1 if cols[0] > cols[1] else -1
    for a, b in zip(cols[:-1], cols[1:]):
        c = (a - b) * asc
        if c > 3 or c < 1:
            xsafe = False
            break
    if xsafe:
        safe += 1

print(safe)
