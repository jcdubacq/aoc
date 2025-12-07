#!/usr/bin/python3
import sys
import re

lines = sys.stdin.readlines()
w = len(lines[0]) - 1
wbits = (1 << w) - 1

status = 0
splits = 0


def transform(l: str) -> int:
    r = 0
    for x in range(len(l)):
        if l[x] == "^":
            r |= 1 << x
    return r


def show(status, tl):
    a = ""
    for i in range(w):
        if tl & (1 << i):
            a += "^"
        elif status & (1 << i):
            a += "|"
        else:
            a += "."
    print(a)


for l in lines:
    if "S" in l:
        status |= 1 << l.find("S")
    else:
        tl = transform(l)
        chocks = tl & status
        status = (status ^ chocks) | (chocks << 1) | (chocks >> 1)
        while chocks:
            if chocks & 1:
                splits += 1
            chocks = chocks >> 1
        # show(status, tl)

print(splits)
