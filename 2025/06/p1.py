#!/usr/bin/python3
import sys
import re

lines = sys.stdin.readlines()


def trim(l: list[str]):
    start = 0
    stop = len(l)
    while len(l[start]) == 0:
        start += 1
    while len(l[stop - 1]) == 0 or l[stop - 1] == "\n":
        stop -= 1
    return l[start:stop]


operators = trim(re.split(r"[^*+]+", lines.pop()))

initial = [1 if x == "*" else 0 for x in operators]

for l in lines:
    ll = trim(re.split(r"\W+", l))
    print(ll)
    for i in range(len(initial)):
        print(i, ll[i])
        if operators[i] == "+":
            initial[i] += int(ll[i])
        else:
            initial[i] *= int(ll[i])

print(sum(initial))
