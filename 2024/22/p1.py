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


def s(a: int, pow=1) -> int:
    for u in range(pow):
        a = ((a << 6) ^ a) & 0xFFFFFF
        a = ((a >> 5) ^ a) & 0xFFFFFF
        a = ((a << 11) ^ a) & 0xFFFFFF
    return a


for line in lines:
    a = s(int(line), pow=2000)
    sum += a
print(sum)
sys.exit(0)
