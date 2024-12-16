#!/usr/bin/python3
import re
from functools import reduce

xx = re.compile("^([0-9]*) *([0-9]*).*$")
la = []
lb = []
with open("/tmp/input.txt") as f:
    lines = f.read().split("\n")
    for line in lines:
        x = xx.match(line)
        if x and x.group(1):
            la.append(int(x.group(1)))
            lb.append(int(x.group(2)))
    s = reduce(
        (lambda x, y: x + y),
        map((lambda x: abs(x[0] - x[1])), zip(sorted(la), sorted(lb))),
    )
    print(s)
