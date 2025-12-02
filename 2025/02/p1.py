#!/usr/bin/python3
from operator import inv
import sys

lines = sys.stdin.readlines()
ranges: list[str] = []
for line in lines:
    while line[-1] == "\n":
        line = line[:-1]
    ranges.extend(line.split(","))


def check_range(r):
    invalids: list[int] = []
    if r == "":
        return invalids
    low, high = map(lambda x: int(x), r.split("-"))
    for x in range(low, high + 1):
        xs = str(x)
        if len(xs) % 2 == 1:
            continue
        halfx = xs[: len(xs) // 2]
        if xs == halfx + halfx:
            invalids.append(x)
    # print(f"Range: {r} Invalids: {', '.join([str(x) for x in invalids])}")
    return invalids


invalids = []
for r in ranges:
    invalids.extend(check_range(r))


print(sum(invalids))
