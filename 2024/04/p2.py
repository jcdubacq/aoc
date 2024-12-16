#!/usr/bin/python3
import re
import sys

bold = "\x1b\x5b\x37\x6d"
norm = "\x1b\x5b\x32\x37\x6d"

target = [i for i in "AMSMS"]


def find_vector(vec):
    ml = min(vec)
    mu = max(vec)
    found = []
    for i in range(-min(vec), len(all) - max(vec)):
        s = ""
        for k, j in enumerate(vec):
            if all[i + j] != target[k]:
                break
            if k == len(vec) - 1:
                found.append(i)
    pr(found, all, vec)
    return len(found)


def pr(places, al, vec):
    all = [x for x in al]
    u = sorted(places)
    adj = 0
    for aa in u:
        for v in vec:
            all[aa + v] = all[aa + v].lower()
    print(">" * ll)
    for c in all:
        if ord(c) > ord("Z"):
            print(bold + c.upper() + norm, end="")
        else:
            print(c, end="")
    print("\n" + ("<" * ll))


sum = 0
origlines = sys.stdin.readlines()
lines = []
for origline in origlines:
    if origline[-1] == "\n":
        lines.append(origline[:-1])
    elif len(origline) > 0:
        lines.append(origline)

ll = len(lines[0])
all = "\n".join(lines)

sum = 0

for vector in [
    [0, -ll - 2, ll + 2, -ll, ll],
    [0, -ll - 2, ll + 2, ll, -ll],
    [0, ll + 2, -ll - 2, -ll, ll],
    [0, ll + 2, -ll - 2, ll, -ll],
]:
    sum += find_vector(vector)
print(sum)
sys.exit(0)
