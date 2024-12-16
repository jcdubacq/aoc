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


def test_safe(cols):
    xsafe = True
    asc = 1 if cols[0] > cols[1] else -1
    for a, b in zip(cols[:-1], cols[1:]):
        c = (a - b) * asc
        if c > 3 or c < 1:
            xsafe = False
            break
    return xsafe


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
    xsafe = test_safe(cols)
    if not xsafe:
        for i in range(len(cols)):
            if i == 0:
                ncols = cols[1:]
            else:
                ncols = cols[0:i]
                if 1 + i < len(cols):
                    ncols.extend(cols[i + 1 :])
            print(f"{ncols},{i}?")
            if test_safe(ncols):
                print(f"{cols} is safe because {ncols} is safe")
                safe += 1
                break
    else:
        safe += 1

print(safe)
