# https://adventofcode.com/2020/day/17
import sys
from itertools import product
from copy import copy


input = [line.strip() for line in sys.stdin]


# part 1
cubes = {(x, y, 0)
         for y, x in product(range(len(input)), range(len(input[0])))
         if input[y][x] == '#'}

def add(u, v): return tuple(map(sum, zip(u, v)))

def simulate(state):
    dims = len(list(state)[0])
    nh = [delta for delta in product((-1, 0, 1), repeat=dims) if any(delta)]
    for cycle in range(6):
        prev = copy(state)
        for cube in prev:
            for pos in [add(cube, delta) for delta in nh] + [cube]:
                s = sum((add(pos, delta) in prev) for delta in nh)
                if pos in prev and s not in [2, 3]: state.discard(pos)
                elif pos not in prev and s == 3: state.add(pos)
    return state

print(len(simulate(copy(cubes))))

# part 2
print(len(simulate({(*pos, 0) for pos in cubes})))
