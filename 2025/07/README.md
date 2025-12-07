# Day 1

[The challenge description](https://adventofcode.com/2025/day/7)

```sh
python3 p1.py < input.txt # last line is the answer
python3 p2.py < input.txt # last line is the answer
```

**Status:** Complete

## Remarks

The first exponential explosion! In the first part, one can compute all paths simultaneously (I dabbled with a bitfield representation of the data). In the second part, one has just to remember how many paths were necessary to reach some position, and duplicate on the two possible outcomes. Works great.
