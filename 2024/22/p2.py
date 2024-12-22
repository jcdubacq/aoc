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


def seq(a: int, pow=2000) -> Tuple[list[int], list[int], list[int], set[int]]:
    l = list(range(pow))
    p = list(range(pow))
    se = list(range(pow))
    t: set[int] = set()
    ab = 0
    aa = a % 10
    b = 0
    l[0] = a
    p[0] = aa
    se[0] = b = (aa + 10) << 15
    for u in range(1, pow):
        ab = aa
        a = ((a << 6) ^ a) & 0xFFFFFF
        a = ((a >> 5) ^ a) & 0xFFFFFF
        a = ((a << 11) ^ a) & 0xFFFFFF
        l[u] = a
        aa = a % 10
        p[u] = aa
        delta = aa - ab + 10  # ranges from 1 to 19
        b = b >> 5 | delta << 15
        se[u] = b
        t.add(b)
    return l, p, se, t


def printse(a: int) -> str:
    r = ""
    b = (a >> 0 & 0x1F) - 10
    c = (a >> 5 & 0x1F) - 10
    d = (a >> 10 & 0x1F) - 10
    e = (a >> 15 & 0x1F) - 10
    return f"({b},{c},{d},{e})"


def printpr(a: int) -> str:
    return str(a % 10)


def sells(p: list[int], se: list[int], t: set[int], d: dict[int, int], line) -> None:
    for key in t:
        try:
            i = se.index(key)
        except ValueError:
            continue
        if key not in d:
            d[key] = p[i]
        else:
            d[key] += p[i]


d = {}
for line in lines:
    l, p, se, t = seq(int(line))
    sells(p, se, t, d, line)

bananas = max(d.values())
e = [printse(x) for x in d if d[x] == bananas]
print(e)
print(bananas)
sys.exit(0)
