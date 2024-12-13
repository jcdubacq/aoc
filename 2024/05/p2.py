#!/usr/bin/python
import re
import sys

bold = "\x1b\x5b\x37\x6d"
norm = "\x1b\x5b\x32\x37\x6d"

constraints = {}
sum = 0
sumtwo = 0

origlines = sys.stdin.readlines()
clines = []
tlines = []
firstpart = True
for origline in origlines:
    if origline[-1] == "\n":
        x = origline[:-1]
    else:
        x = origline
    if len(x) == 0:
        firstpart = False
        continue
    if firstpart:
        clines.append(x)
    else:
        tlines.append(x)

for cc in clines:
    c = cc.split("|")
    if c[0] not in constraints:
        constraints[c[0]] = set()
    constraints[c[0]].add(c[1])

for tt in tlines:
    t = tt.split(",")
    print(t)
    ok = True
    incorrect = False
    for u in range(len(t) - 1, -1, -1):
        if not ok:
            break
        for v in range(u - 1, -1, -1):
            if t[u] in constraints and t[v] in constraints[t[u]]:
                print(f"{tt} est incorrect because of {t[u]}|{t[v]}")
                ok = False
                incorrect = True
                # rebuild
                print(f"----------------------- Rebuilding {t}")
                newt = []
                while len(t):
                    mem = len(t)
                    print(f"Now looking at {t} / {newt}")
                    lic = set()
                    lc = [constraints[x] for x in t if x in constraints]
                    print(lc)
                    for c in lc:
                        if c not in newt:
                            lic = lic.union(c)
                    print(f"{lic} is forbidden")
                    for uu in t:
                        if uu not in lic:
                            newt.append(uu)
                            t.remove(uu)
                            print(f"Next looking at {t} / {newt}")
                            break
                        else:
                            print(f"{uu} is forbidden...")
                    if mem == len(t):
                        print("Loop?")
                        sys.exit(0)
                print(newt)
                a = int(newt[len(newt) // 2])
                print(
                    f"{bold}{tt} est incorrect, utilisation de {newt}, {sumtwo}+{a}{norm}"
                )
                sumtwo += a
                break

    if ok:
        a = int(t[len(t) // 2])
        # print(f"{tt} est correct, +{a}")
        sum += a


print(sumtwo)
sys.exit(0)
