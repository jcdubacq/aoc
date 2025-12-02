# Day 1

[The challenge description](https://adventofcode.com/2025/day/1)

```sh
python3 p1.py < input.txt # last line is the answer
python3 p2.py < input.txt # last line is the answer
```

**Status:** Complete

## Remarks
The challenge of part1 is just parsing. The challenge of part2 is counting correctly the number of multiples of the lock size inside the list of clicks. This is easy if done one by one, but more challenging to find the right formula (which I had already found in the past for other uses, but apparently kept forgetting) : ((high-low)+((low-1)%100+1))//100
