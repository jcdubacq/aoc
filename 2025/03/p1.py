#!/usr/bin/python3
from operator import inv
import sys

lines = sys.stdin.readlines()


def find_joltage(line):
    while len(line)>0 and line[-1] not in "0123456789":
        line=line[:-1]
    digit_one=max(set(int(x) for x in line[:-1]))
    where = line.find(str(digit_one))
    digit_two=max(set(int(x) for x in line[where+1:]))
    result = 10*digit_one+digit_two
    # print(f"{line} => {result}")
    return result
sum=0
for line in lines:
    sum+=find_joltage(line)
print(sum)