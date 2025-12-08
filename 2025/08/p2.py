#!/usr/bin/python3
from collections import defaultdict
import sys
import re
import math

lines = sys.stdin.readlines()


class Point:
    def __init__(self, x, y, z, n) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.num = n
        self.set = n

    def __str__(self) -> str:
        return f"({self.x},{self.y},{self.z})"

    def dst(self, p: "Point") -> float:
        return (p.x - self.x) ** 2 + (p.y - self.y) ** 2 + (p.z - self.z) ** 2

    def in_set(self, n):
        self.set = n


class Segment:
    def __init__(self, p: Point, q: Point) -> None:
        self.p = p
        self.q = q
        self.l = p.dst(q)

    def in_set(self, n):
        self.p.in_set(n)
        self.q.in_set(n)

    def __str__(self) -> str:
        return f"{str(self.p)}{self.p.num}=>{str(self.q)}{self.q.num}"

    def __lt__(self, other: "Segment"):
        return self.l < other.l

    def __gt__(self, other: "Segment"):
        return self.l > other.l

    def __le__(self, other: "Segment"):
        return self.l <= other.l

    def __ge__(self, other: "Segment"):
        return self.l >= other.l


points = []
for l in lines:
    x = re.match(r"^([0-9]+),([0-9]+),([0-9]+)$", l)
    assert x is not None
    points.append(Point(int(x.group(1)), int(x.group(2)), int(x.group(3)), len(points)))

segments: list[Segment] = []

for p in range(len(points)):
    for q in range(p + 1, len(points)):
        segments.append(Segment(points[p], points[q]))

segments.sort()

sets = []
for p in points:
    s = set()
    s.add(p)
    sets.append(s)
x = 0
lastsegment = None
while len(sets[points[0].set]) < len(points):
    s = segments[x]
    x += 1
    if s.q.set == s.p.set:
        print(f"Not merging {s.q.set} into {s.p.set}")
        continue
    print(f"Merging {s.q.set} into {s.p.set}")
    oldset_num = s.p.set
    dyingset_num = s.q.set
    for pp in sets[dyingset_num]:
        pp.in_set(oldset_num)
        sets[oldset_num].add(pp)
    sets[dyingset_num] = set()
print(segments[x - 1], segments[x - 1].p.x * segments[x - 1].q.x)
