#!/usr/bin/python3
import re
import sys
import math
import time

bold = "\x1b\x5b\x37\x6d"
norm = "\x1b\x5b\x32\x37\x6d"
home = "\x1b\x5b\x48"

sum = 0

rre = re.compile(r"^p=([0-9]*),([0-9]*) v=([-0-9]*),([-0-9]*)")

w, h = 101, 103
delay = 100000
if len(sys.argv) > 1:
    delay = int(sys.argv[1])

final = []
speeds = []

suspect = []


def readit():
    global w, h
    lines = []
    origlines = sys.stdin.readlines()
    for origline in origlines:
        if origline[-1] == "\n":
            x = origline[:-1]
        else:
            x = origline
        lines.append(x)

    for line in lines:
        if len(line) == 0:
            continue
        r = rre.match(line)
        if not r:
            print("Incorrect line: ", line)
            sys.exit(0)
        x, y, vx, vy = (
            int(r.group(1)),
            int(r.group(2)),
            int(r.group(3)),
            int(r.group(4)),
        )
        final.append((x, y))
        speeds.append((vx, vy))
    if len(lines) < 30:
        w, h = 11, 7


readit()


def showit():
    isTree = False
    d = {}
    for u, v in final:
        if u not in d:
            d[u] = {}
        if v not in d[u]:
            d[u][v] = 1
        else:
            d[u][v] += 1
    for y in range(h):
        if isTree:
            break
        last = 0
        for x in range(w):
            if x in d and y in d[x]:
                last = (last << 1) | 0x1
            else:
                last = 0
            if (last & 0xFFF) == 0xFFF:
                isTree = True
                break
    print(f"{home}delay={when}/{delay}")
    if isTree:
        for y in range(h):
            for x in range(w):
                if x in d and y in d[x]:
                    print(chr(48 + d[x][y]), end="")
                else:
                    print(".", end="")
            print()
        suspect.append(when)
    print(suspect)
    return isTree


delay = 100000
for when in range(delay):
    for i, p in enumerate(final):
        nx = (p[0] + speeds[i][0]) % w
        ny = (p[1] + speeds[i][1]) % h
        final[i] = (nx, ny)
    if showit():
        print(when + 1)
        break

sys.exit(0)
