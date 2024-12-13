#!/usr/bin/python3
import sys

lines=sys.stdin.readlines()
la=[]
lb=[]
for line in lines:
    c=line.split("  ")
    la.append(c[0])
    lb.append(c[1][:-1])
la.sort()
lb.sort()
s=0
i=0
j=0
print(la,lb)
ss=0
x=int(la[i])
y=int(lb[j])
while i<len(la) and j<len(lb):
    x=int(la[i])
    y=int(lb[j])
    while i<len(la) and x<y:
        i+=1
        if i<len(la):
            x=int(la[i])
    while j<len(lb) and int(lb[j])<x:
        j+=1
        if j<len(lb):
            y=int(lb[j])
    while j<len(lb) and int(lb[j])==x:
        ss+=x
        print(f"i={i},j={j},ss={ss}")
        j+=1
    while i<len(la) and int(la[i])==y: 
        s+=ss
        print(f"i={i},j={j},s={s}")
        i+=1
    ss=0
print(s)
