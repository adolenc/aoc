# https://adventofcode.com/2021/day/25
import sys
from copy import deepcopy
from itertools import product


input = [line.strip() for line in sys.stdin]


# part 1
map = [list(l) for l in input]
xmod = lambda x: x % len(map[0])
ymod = lambda y: y % len(map)
across = lambda map: product(range(len(map)), range(len(map[0])))

step = 0
x_move = y_move = True
while y_move or x_move:
    step += 1
    x_move = y_move = False
    next_map = deepcopy(map)
    for y, x in across(next_map):
        if map[y][x] == '>' and map[y][xmod(x+1)] == '.':
            next_map[y][x] = '.'
            next_map[y][xmod(x+1)] = '>'
            x_move = True
    map = deepcopy(next_map)
    for y, x in across(next_map):
        if map[y][x] == 'v' and map[ymod(y+1)][x] == '.':
            next_map[y][x] = '.'
            next_map[ymod(y+1)][x] = 'v'
            y_move = True
    map = next_map

print(step)
