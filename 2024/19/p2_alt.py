#!/usr/bin/python3
import re
import sys
from typing import Tuple, TypeAlias, Optional
import time
import functools

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

@functools.cache
def build(goal:str)->int:
    if len(goal)==0:
        return 1
    canbe = 0
    for design in d:
        if goal.startswith(design):
            newgoal = goal[len(design):]
            canbe+=build(newgoal)
    return canbe
                

for line in lines:
    sum+=build(line)
print(sum)