#!/usr/bin/python3
import sys
lines = sys.stdin.readlines()

la=[]
lb=[]
for line in lines:
    c=line.split("  ")
    la.append(c[0])
    lb.append(c[1][:-1])
la.sort()
lb.sort()
s=0
for i,v in enumerate(la):
    s+=abs(int(lb[i])-int(v))
print(s)
