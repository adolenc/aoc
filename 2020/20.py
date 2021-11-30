# https://adventofcode.com/2020/day/20
import sys
from collections import defaultdict
from math import prod
import re


input = sys.stdin


# part 1
def transpose(A): return [*map(lambda r: ''.join(r), zip(*A))]
def rotate(A): return [*map(lambda r: ''.join(r), zip(*A[::-1]))]

def record_tile_edges(id, tile, tile_ids_with_edge):
    for rotation in range(4):
        tile = rotate(tile)
        tile_ids_with_edge[tile[0]].append(id)
        tile_ids_with_edge[tile[-1]].append(id)

tiles = {}
tile_ids_with_edge = defaultdict(list)
for t in input.read().strip().split('\n\n'):
    id, *tile = t.split('\n')
    tiles[int(id[5:-1])] = tile
    record_tile_edges(int(id[5:-1]), tile, tile_ids_with_edge)

per_tile = defaultdict(int)
for edge in tile_ids_with_edge:
    if len(tile_ids_with_edge[edge]) >= 2:
        for tile_id in tile_ids_with_edge[edge]:
            per_tile[tile_id] += 1

print(prod(e for e, v in per_tile.items() if v == 4))

# part 2
def all_transformations(A):
    for flip in range(2):
        for rotation in range(4):
            yield A
            A = rotate(A)
        A = transpose(A)

flatten = lambda lst: [e for slst in lst for e in slst]
def add(u, v): return (u[0] + v[0], u[1] + v[1])

def top(tile): return tile[0]
def bottom(tile): return tile[-1]
def left(tile): return rotate(tile)[0]
def right(tile): return rotate(tile)[-1]

def propagate_map(coordinates, sea_map):
    tile_id_at_coordinates, tile_at_coordinates = sea_map[coordinates]

    for delta, edge_1_fn, edge_2_fn in [((0, -1), top, bottom),
                                        ((0,  1), bottom, top),
                                        ((-1, 0), left, right),
                                        (( 1, 0), right, left)]:
        if add(coordinates, delta) in sea_map:
            continue

        edge_to_match = edge_1_fn(tile_at_coordinates)
        if len(tile_ids_with_edge[edge_to_match]) <= 1:
            continue

        [matching_tile_id] = set(tile_ids_with_edge[edge_to_match]) - {tile_id_at_coordinates}
        for transformed_tile in all_transformations(tiles[matching_tile_id]):
            if edge_2_fn(transformed_tile) == edge_to_match:
                sea_map[add(coordinates, delta)] = (matching_tile_id, transformed_tile)
                break
        propagate_map(add(coordinates, delta), sea_map)

def concatenate_map(sea_map):
    def remove_edges(tile):
        return [t[1:-1] for t in tile[1:-1]]

    min_x, min_y = min(sea_map)
    max_x, max_y = max(sea_map)
    big_map = []
    for y in range(min_y, max_y+1):
        big_map += list(map(''.join, zip(*[remove_edges(sea_map[(x, y)][1])
                                           for x in range(min_x, max_x+1)])))
    return big_map


first_tile_id = next(iter(tiles.keys()))
sea_map = {(0, 0): (first_tile_id, tiles[first_tile_id])}
propagate_map((0, 0), sea_map)
sea_map = concatenate_map(sea_map)

MONSTER = """\
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""

monster_tiles = sum(m == '#' for m in MONSTER)
sea_map_tiles = sum(m == '#' for m in ''.join(flatten(sea_map)))
regex_monster = ['(?=(' + m + '))' for m in MONSTER.replace(' ', '.').split('\n')]

monsters_found = 0
for possible_map in all_transformations(sea_map):
    for i in range(len(possible_map) - 2):
        m0 = {m.start() for m in re.finditer(regex_monster[0], possible_map[i+0])}
        m1 = {m.start() for m in re.finditer(regex_monster[1], possible_map[i+1])}
        m2 = {m.start() for m in re.finditer(regex_monster[2], possible_map[i+2])}
        monsters_found += len(m0 & m1 & m2)

print(sea_map_tiles - monster_tiles * monsters_found)
