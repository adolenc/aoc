# https://adventofcode.com/2020/day/11
import sys
from copy import copy
import numpy as np
from scipy import signal
from itertools import product
from collections import defaultdict


input = [line.strip() for line in sys.stdin]


# part 1
seats = np.array([list(l.replace('.', '0').replace('L', '1')) for l in input], dtype=int)

def simulate(counts_fn, max_seats):
    prev = np.ones(np.shape(seats), dtype=bool)
    next = np.zeros(np.shape(seats), dtype=bool)
    while not (next == prev).all():
        prev = copy(next)
        counts = counts_fn(prev)
        next[(seats == 1) & (~prev & (counts == 0))] = True
        next[(seats == 1) & (prev & (counts >= max_seats))] = False
    return next

neighborhood = [[1, 1, 1],
                [1, 0, 1],
                [1, 1, 1]]
print(np.sum(simulate(lambda world: signal.convolve2d(world, neighborhood, 'same'), 4)))

# part 2
def neighbor_in_dir(pos, dir):
    pos = (pos[0] + dir[0], pos[1] + dir[1])
    while 0 <= pos[0] < len(seats) and 0 <= pos[1] < len(seats[0]):
        if seats[pos] == 1:
            return pos
        pos = (pos[0] + dir[0], pos[1] + dir[1])
    return None

neighborhood = defaultdict(list)
for pos in product(range(len(seats)), range(len(seats[0]))):
    for dy, dx in product((-1, 0, 1), (-1, 0, 1)):
        if dy == dx == 0: continue
        if (neighbor := neighbor_in_dir(pos, (dy, dx))):
            neighborhood[pos] += [neighbor]

def count_taken_seats(seating):
    cnts = np.zeros(np.shape(seating))
    for pos in product(range(len(seating)), range(len(seating[0]))):
        cnts[pos] = sum(seating[neighbor] for neighbor in neighborhood[pos])
    return cnts

print(np.sum(simulate(count_taken_seats, 5)))
