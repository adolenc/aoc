# https://adventofcode.com/2020/day/3
import sys
from math import prod, ceil


input = [line.strip() for line in sys.stdin]


# part 1
TREE = '#'
H, W = len(input), len(input[0])

def count_trees(slope):
    dx, dy = slope
    steps = ceil(H / dy)
    return [input[s * dy][(s * dx) % W] for s in range(steps)].count(TREE)

print(count_trees((3, 1)))

# part 2
slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
print(prod(map(count_trees, slopes)))
