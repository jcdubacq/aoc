#!/usr/bin/python3
import re
import sys
import math

bold = "\x1b\x5b\x37\x6d"
norm = "\x1b\x5b\x32\x37\x6d"

sum = 0

rre = re.compile(r"^p=([0-9]*),([0-9]*) v=([-0-9]*),([-0-9]*)")

w, h = 101, 103
delay = 100
if len(sys.argv) > 1:
    delay = int(sys.argv[1])
lines = []
origlines = sys.stdin.readlines()
for origline in origlines:
    if origline[-1] == "\n":
        x = origline[:-1]
    else:
        x = origline
    lines.append(x)

if len(lines) < 30:
    w, h = 11, 7

final = []

for line in lines:
    if len(line) == 0:
        continue
    r = rre.match(line)
    if not r:
        print("Incorrect line: ", line)
        sys.exit(0)
    x, y, vx, vy = int(r.group(1)), int(r.group(2)), int(r.group(3)), int(r.group(4))
    fx = (x + delay * vx) % w
    fy = (y + delay * vy) % h
    final.append((fx, fy))

d = {}
for u, v in final:
    if u not in d:
        d[u] = {}
    if v not in d[u]:
        d[u][v] = 1
    else:
        d[u][v] += 1

print(f"delay={delay}")
sums = [0, 0, 0, 0]
for y in range(h):
    for x in range(w):
        if x in d and y in d[x]:
            s = False
            if x < w // 2:
                if y < h // 2:
                    sums[0] += d[x][y]
                elif y > h // 2:
                    sums[2] += d[x][y]
                else:
                    s = True
            elif x > w // 2:
                if y < h // 2:
                    sums[1] += d[x][y]
                elif y > h // 2:
                    sums[3] += d[x][y]
                else:
                    s = True
            else:
                s = True
            if s:
                print(bold + chr(48 + d[x][y]) + norm, end="")
            else:
                print(chr(48 + d[x][y]), end="")
        else:
            print(".", end="")
    print()

print(sums)
print(sums[0] * sums[1] * sums[2] * sums[3])
sys.exit(0)
