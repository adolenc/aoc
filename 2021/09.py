# https://adventofcode.com/2021/day/9
import sys
from math import prod
from itertools import product


input = [line.strip() for line in sys.stdin]
map = [[9] + [int(j) for j in i] + [9] for i in input]
map = [[9] * len(map[0])] + map + [[9] * len(map[0])]

# part 1
move_deltas = [(0, -1), (0, 1), (-1, 0), (1, 0)]

low_points = []
for y, x in product(range(1, len(map) - 1), range(1, len(map[0]) - 1)):
    if all(map[y][x] < map[y+dy][x+dx] for dy, dx in move_deltas):
        low_points += [(y, x)]

print(sum(map[y][x] + 1 for y, x in low_points))

# part 2
def basin_size(y, x, prev, visited=None):
    if not visited: visited = set()

    if (y, x) in visited or map[y][x] == 9 or map[y][x] < prev:
        return 0
    visited.add((y, x))
    return 1 + sum(basin_size(y+dy, x+dx, map[y][x], visited) for dy, dx in move_deltas)

basin_sizes = [basin_size(y, x, map[y][x]) for y, x in low_points]
print(prod(sorted(basin_sizes, reverse=True)[:3]))
