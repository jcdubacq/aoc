#!/usr/bin/python3
import re
import sys
from typing import Tuple, TypeAlias, Optional
import time

Path: TypeAlias = list[Tuple[int, int]]

bold = "\x1b\x5b\x37\x6d"
norm = "\x1b\x5b\x32\x37\x6d"
home = "\x1b\x5bH"
clear = "\x1b[H\x1b[2J\x1b[3J"

constraints = {}
sum = 0

lines = []
origlines = sys.stdin.readlines()
instructions = ""
# two parts but swapped
first = False
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
        first = True

d=instructions.split(', ')

def build(goal:str):
    if len(goal)==0:
        return True
    for design in d:
        if goal.startswith(design):
            canbe=build(goal[len(design):])
            if canbe:
                return True
    return False
                

for line in lines:
    if build(line):
        sum+=1
        print(f"OK: {line}")
    else:
        print(f"KO: {line}")
print(sum)