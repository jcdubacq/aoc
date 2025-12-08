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
        self.set = -1

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
max = int(sys.argv[1])
print(f"Finding in {max} segments")
for x in range(max):
    s = segments[x]
    if s.p.set == -1 and s.q.set == -1:
        n = len(sets)
        print(f"New set {n}")
        newset = set()
        newset.add(s.p)
        newset.add(s.q)
        s.p.in_set(n)
        s.q.in_set(n)
        sets.append(newset)
    elif s.p.set == -1:
        n = s.q.set
        print(f"Adding to {n}")
        oldset = sets[n]
        oldset.add(s.p)
        s.p.in_set(n)
    elif s.q.set == -1:
        n = s.p.set
        print(f"Adding to {n}")
        oldset = sets[n]
        oldset.add(s.q)
        s.q.in_set(n)
    else:
        # merge two sets
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

a = [len(s) for s in sets if len(s) > 0]
a.sort(reverse=True)
print(math.prod(a[:3]))
