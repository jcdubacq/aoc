import re
import sys

bold = "\x1b\x5b\x37\x6d"
norm = "\x1b\x5b\x32\x37\x6d"

constraints = {}
sum = 0

lines = []
origlines = sys.stdin.readlines()
for origline in origlines:
    if origline[-1] == "\n":
        x = origline[:-1]
    else:
        x = origline
    lines.append(x)
line = lines[0]
acc = 0
line = " ".join(lines)
coeff = 1
x = re.compile(r"^.*?(mul\(([0-9][0-9]?[0-9]?),([0-9][0-9]?[0-9]?)\)|do(n't)?\(\))")
finished = False
while not finished:
    m = x.match(line)
    if m:
        line = line[len(m.group(0)) :]
        mm = m.group(1)[:3]
        if mm == "mul":
            acc += coeff * int(m.group(2)) * int(m.group(3))
        elif mm == "don":
            coeff = 0
        elif mm == "do(":
            coeff = 1
    else:
        finished = True
print(acc)
