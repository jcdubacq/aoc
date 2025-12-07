#!/usr/bin/python3
import sys
import re
from collections import defaultdict

lines = sys.stdin.readlines()
w = len(lines[0]) - 1
wbits = (1 << w) - 1

hashtable = defaultdict(int)


def transform(l: str) -> int:
    r = 0
    for x in range(len(l)):
        if l[x] == "^":
            r |= 1 << x
    return r


for l in lines:
    if "S" in l:
        hashtable[l.find("S")] = 1
        continue
    newhashtable = defaultdict(int)
    for x in range(w):
        if l[x] == ".":
            newhashtable[x] += hashtable[x]
            continue
        # there is a split
        newhashtable[x - 1] += hashtable[x]
        newhashtable[x + 1] += hashtable[x]
    hashtable = newhashtable

print(sum(hashtable.values()))
