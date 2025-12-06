#!/usr/bin/python3
import sys

# Two part loading
firstpart = True
intervals = []
numbers = []
for l in sys.stdin.readlines():
    if len(l) < 2:
        firstpart = False
        continue
    if firstpart:
        intervals.append(l)
    else:
        numbers.append(int(l))


class Interval:
    def __init__(self, range_as_string) -> None:
        e = range_as_string.split("-")
        if len(e) < 2:
            self.start = None
            return
        self.start = int(e[0])
        self.stop = int(e[1])
        try:
            assert self.start <= self.stop
        except AssertionError:
            print(f"{range_as_string} is i515273536092893-515273536092893ncorrect")
            sys.exit(1)

    def inside(self, x: int):
        if x < self.start:
            return -1
        if x > self.stop:
            return 1
        return 0

    def defined(self) -> bool:
        if self.start is None:
            return False
        return True

    def __str__(self) -> str:
        if self.defined():
            return f"{self.start}-{self.stop}"
        return "Empty range"


class IntervalSet:
    def __init__(self) -> None:
        self.intervals = []

    def append(self, i: Interval):
        newlist = []
        highers = []
        build = True
        for x in self.intervals:
            left = i.inside(x.start)
            right = i.inside(x.stop)
            if right == -1:
                newlist.append(x)
            elif left == 1:
                highers.append(x)
            elif left == -1 and right == 1:  # i is contained in x
                lowers = self.intervals
                highers = []
                build = False
                break
            elif left == 1 and right == -1:  # x is contained in i:
                pass
            else:
                i.start = min(x.start, i.start)
                i.stop = max(x.stop, i.stop)
        if build:
            self.intervals = newlist + [i] + highers

    def inside(self, x: int):
        for i in self.intervals:
            if x > i.stop:
                continue
            if x < i.start:
                return False
            return True

    def __str__(self) -> str:
        return ",".join([str(x) for x in self.intervals])


iset = IntervalSet()
for i in intervals:
    ii = Interval(i)
    if ii.defined():
        iset.append(ii)

sum = 0
for n in numbers:
    if iset.inside(int(n)):
        sum += 1
print(sum)
