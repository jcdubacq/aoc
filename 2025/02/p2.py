#!/usr/bin/python3
from operator import inv
import sys

lines = sys.stdin.readlines()
ranges: list[str] = []
for line in lines:
    while line[-1] == "\n":
        line = line[:-1]
    ranges.extend(line.split(","))


def check_int(x: int) -> bool:
    xs = str(x)
    xl = len(xs)
    for l in range(1, 1 + (len(xs) // 2)):
        if xl % l != 0:
            continue
        pieceofx = xs[:l] * (xl // l)
        if pieceofx == xs:
            return True
    return False


def check_range(r):
    invalids: list[int] = []
    if r == "":
        return invalids
    low, high = map(lambda x: int(x), r.split("-"))
    for x in range(low, high + 1):
        if check_int(x):
            invalids.append(x)
    # print(f"Range: {r} Invalids: {', '.join([str(x) for x in invalids])}")
    return invalids


invalids = []
for r in ranges:
    invalids.extend(check_range(r))


print(sum(invalids))
