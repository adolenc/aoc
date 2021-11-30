# https://adventofcode.com/2020/day/1
import sys


input = set(map(int, sys.stdin))


# part 1
print(next(a * b
           for a in input
           if (b := 2020 - a) in input))

# part 2
print(next(a * b * c
           for a in input
           for b in input
           if (c := 2020 - a - b) in input))
