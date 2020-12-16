# https://adventofcode.com/2020/day/6
import sys

input = sys.stdin


# part 1
groups = input.read().split('\n\n')
print(sum(map(len, [set(g) - set('\n') for g in groups]))) 

# part 2
groups = [[set(a) for a in g.split()] for g in groups]
print(sum(len(set.intersection(*g)) for g in groups))
