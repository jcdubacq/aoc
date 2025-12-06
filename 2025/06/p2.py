#!/usr/bin/python3
import sys
import re
from math import prod

lines = sys.stdin.readlines()

results = []
opline = len(lines) - 1
length = len(lines[0])
values = []
for x in range(length):
    value = 0
    if lines[0][length - x - 1] == "\n":
        continue
    for y in range(len(lines) - 1):
        c = lines[y][length - x - 1]
        if ord(c) >= 48 and ord(c) < 58:
            value = 10 * value + ord(c) - 48
            # print(f"{c} => value: {value}")
    if lines[opline][length - x - 1] == "*":
        # print("*".join([str(x) for x in values]))
        results.append(value * prod(values))
        values = []
    elif lines[opline][length - x - 1] == "+":
        # print("+".join([str(x) for x in values]))
        results.append(value + sum(values))
        values = []
    else:
        if value > 0:
            values.append(value)
        # print("Values: ", values)
print(sum(results))
