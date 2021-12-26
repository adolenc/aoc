# https://adventofcode.com/2021/day/11
import sys
from itertools import product


input = [line.strip() for line in sys.stdin]


# part 1
map = [[10] + [int(j) for j in i] + [10] for i in input]
map = [[10] * len(map[0])] + map + [[10] * len(map[0])]

def energize(y, x):
    map[y][x] += 1
    if map[y][x] == 10:
        map[y][x] = -10000
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == dy == 0:
                    continue
                energize(y+dy, x+dx)

flashes = 0
for step in range(100):
    for y, x in product(range(1, len(map) - 1), range(1, len(map[0]) - 1)):
        energize(y, x)
    for y, x in product(range(1, len(map) - 1), range(1, len(map[0]) - 1)):
        if map[y][x] < 0:
            flashes += 1
            map[y][x] = 0
print(flashes)

# part 2
for step in range(10000):
    for y, x in product(range(1, len(map) - 1), range(1, len(map[0]) - 1)):
        energize(y, x)
    all_flash = True
    for y, x in product(range(1, len(map) - 1), range(1, len(map[0]) - 1)):
        if map[y][x] < 0:
            map[y][x] = 0
        else:
            all_flash = False
    if all_flash:
        print(step+1)
        break
