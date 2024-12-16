#!/usr/bin/python3
import re
import sys
import math

bold = "\x1b\x5b\x37\x6d"
norm = "\x1b\x5b\x32\x37\x6d"

sum = 0

bre = re.compile("^Button ([A-Z]): X[+]([0-9]*), Y[+]([0-9]*)")
pre = re.compile("^Prize: X=([0-9]*), Y=([0-9]*)")

lines = []
origlines = sys.stdin.readlines()
for origline in origlines:
    if origline[-1] == "\n":
        x = origline[:-1]
    else:
        x = origline
    lines.append(x)


class Claw:
    def addbutton(self, a, b, c):
        if a == "A":
            self.a = int(b)
            self.b = int(c)
        else:
            self.c = int(b)
            self.d = int(c)

    def solve(self, a, b):
        self.e = int(a) + 10000000000000
        self.f = int(b) + 10000000000000
        # a*x+c*y=e
        # b*x+d*y=f
        # x=(e-cy)/a
        # (d-cb/a)y=f-eb/a
        o = self.b / self.a
        p = self.f - self.e * o
        q = self.d - o * self.c
        y = round(p / q)
        x = round((self.e - self.c * y) / self.a)
        if x * self.a + y * self.c == self.e and x * self.b + y * self.d == self.f:
            self.x = x
            self.y = y
            return 3 * x + y
        else:
            return None

    def __str__(self) -> str:
        return f"{self.a}*A+{self.b}*B={self.e} / {self.c}*A+{self.d}*B={self.f}"


acc = 0
claw = None
for line in lines:
    b = bre.match(line)
    if b:
        if claw is None:
            claw = Claw()
        claw.addbutton(b.group(1), b.group(2), b.group(3))
    else:
        p = pre.match(line)
        assert claw is not None
        if p:
            e = claw.solve(p.group(1), p.group(2))
            if e == None:
                print(str(claw) + " est insoluble")
            else:
                print(f"{claw} apporte +{e} ({claw.x} A+{claw.y} B)")
                acc += e
            claw = None

print(acc)
sys.exit(0)
