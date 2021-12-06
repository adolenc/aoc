# https://adventofcode.com/2021/day/5
import sys
from collections import defaultdict


input = [line.strip() for line in sys.stdin]
lines = [l.replace('->', ',').split(',') for l in input]
lines = [tuple(map(int, coord)) for coord in lines]

# part 1
map = defaultdict(int)
for x1, y1, x2, y2 in lines:
    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            map[x1, y] += 1
    if y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            map[x, y1] += 1

print(sum(1 for v in map.values() if v >= 2))

# part 2
map = defaultdict(int)
for x1, y1, x2, y2 in lines:
    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            map[x1, y] += 1
    if y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            map[x, y1] += 1
    if abs(x1 - x2) == abs(y1 - y2):
        if x1 > x2:
            x1, y1, x2, y2 = x2, y2, x1, y1
        dy = 1 if y2 > y1 else -1
        for i in range(max(x1, x2) - min(x1, x2) + 1):
            map[x1 + i, y1 + dy * i] += 1

print(sum(1 for v in map.values() if v >= 2))
