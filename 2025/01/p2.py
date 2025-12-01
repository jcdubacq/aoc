#!/usr/bin/python3
import sys
import math
lines = sys.stdin.readlines()


class Lock:
    def __init__(self,pos=50,size=100) -> None:
        self.zero:int=0
        self.value:int=pos
        self.size:int=size
        # print(f" - The dial starts by pointing at {self.value}.")
    def processline(self,line):
        val=int(line[1:])
        if line[0]=='L':
            old=self.value-1
            new=self.value-val
        else:
            old=self.value+1
            new=self.value+val
        low=min(old,new)
        high=max(old,new)
        clicks=((high-low)+((low-1)%100+1))//100
        # print(low,high,clicks)
        self.value=new%self.size
        self.zero+=clicks
        # print(f" - The dial is rotated {line[:-1]} to point at {self.value} ; it clicked to zero {clicks} time.")

    def processlines(self,lines):
        for i in lines:
            self.processline(i)


lock=Lock()

lock.processlines(lines)

print(lock.zero)
