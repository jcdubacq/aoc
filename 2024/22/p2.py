#!/usr/bin/python3
import re
import sys
from typing import Tuple, TypeAlias, Optional
import functools
import time

Coord: TypeAlias = Tuple[int, int]

bold = "\x1b\x5b\x37\x6d"
norm = "\x1b\x5b\x32\x37\x6d"
home = "\x1b\x5bH"
clear = "\x1b[H\x1b[2J\x1b[3J"

constraints = {}
sum = 0

lines = []
origlines = sys.stdin.readlines()
instructions = ""
# two parts
first = True
for origline in origlines:
    if origline[-1] == "\n":
        x = origline[:-1]
    else:
        x = origline
    if len(x) > 0:
        if first:
            lines.append(x)
        else:
            instructions += x
    else:
        first = False


def seq(a: int, pow=2000) -> int:
    l = list(range(pow))
    se = list(range(pow))
    l[0] = a
    ab = aa
    aa = a % 10
    b = 0
    l[0] = a
    for u in range(1, pow):
        a = ((a << 6) ^ a) & 0xFFFFFF
        a = ((a >> 5) ^ a) & 0xFFFFFF
        a = ((a << 11) ^ a) & 0xFFFFFF
        l[u] = a
        aa = a % 10
        delta = aa - bb + 10
        b = b >> 5 | aa << 20
        se[u] = b
    return a


for line in lines:
    a = s(int(line), pow=2000)
    sum += a
print(sum)
sys.exit(0)
