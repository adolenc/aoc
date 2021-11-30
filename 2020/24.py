# https://adventofcode.com/2020/day/24
import sys
import re
from collections import defaultdict
from copy import copy


input = [line.strip() for line in sys.stdin]


# part 1
moves = dict(       nw=(-0.5, -0.5),ne=(0.5, -0.5),
              w=(-1,  0),                     e=(1,  0),
                    sw=(-0.5,  0.5),se=(0.5,  0.5)
             )

def add(pos, delta): return (pos[0] + delta[0], pos[1] + delta[1])

black_tiles = set()
for tile in input:
    pos = (0, 0)
    for move in re.findall(r'se|sw|ne|nw|e|w', tile):
        pos = add(pos, moves[move])
    if pos in black_tiles:
        black_tiles.remove(pos)
    else:
        black_tiles.add(pos)

print(len(black_tiles))

# part 2
next_black_tiles = black_tiles
for i in range(100):
    black_tiles = copy(next_black_tiles)
    for black_tile in black_tiles:
        ngh = sum(1 for move in moves if add(black_tile, moves[move]) in black_tiles)
        if ngh == 0 or ngh > 2: next_black_tiles.discard(black_tile)
    for black_tile in black_tiles:
        for poss_white_tile in (add(black_tile, moves[move]) for move in moves):
            if poss_white_tile in black_tiles: continue
            ngh = sum(1 for move in moves if add(poss_white_tile, moves[move]) in black_tiles)
            if ngh == 2: next_black_tiles.add(poss_white_tile)

print(len(next_black_tiles))
