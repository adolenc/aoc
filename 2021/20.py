# https://adventofcode.com/2021/day/20
import sys


input = [line.strip() for line in sys.stdin]
alg = input[0]
image = input[2:]


# part 1
deltas = [(-1,-1), (0,-1), (1,-1),
          (-1, 0), (0, 0), (1, 0),
          (-1, 1), (0, 1), (1, 1)]

tr = lambda c: '1' if c == '#' else '0'
to_int = lambda neigh: int(''.join(neigh).replace('#', '1').replace('.', '0'), 2)

def expand(map, out_of_range_char):
    return {(x+dx,y+dy): map.get((x+dx, y+dy), out_of_range_char) for x, y in map for dx, dy in deltas}

def enhance(image, times):
    out_of_range_char = '.'
    map = {(x,y): char for y,row in enumerate(image) for x,char in enumerate(row)}
    map = expand(map, out_of_range_char)

    for _ in range(times):
        next_map = {}
        for x,y in {(xx+dx, yy+dy) for xx,yy in map for dx,dy in deltas}:
            neigh = [map.get((x+dx, y+dy), tr(out_of_range_char)) for dx,dy in deltas]
            next_map[(x, y)] = alg[to_int(neigh)]
        out_of_range_char = alg[to_int([tr(out_of_range_char)] * 9)]
        map = expand(next_map, out_of_range_char)
    return map

print(sum(v == '#' for v in enhance(image, 2).values()))

# part 2
print(sum(v == '#' for v in enhance(image, 50).values()))
