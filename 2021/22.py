# https://adventofcode.com/2021/day/22
import sys
from collections import defaultdict
from itertools import product


input = [line.strip() for line in sys.stdin]


# part 1
def line_to_cube(line):
    on, spans = line.split(' ')
    parse_span = lambda span: tuple([int(s) for s in span.split('=')[1:][0].split('..')])
    spans = spans.split(',')
    return on == 'on', tuple(parse_span(span) for span in spans)

regions = [line_to_cube(line) for line in input]

map = defaultdict(lambda: 0)
for on, ((x1, x2), (y1, y2), (z1, z2)) in regions:
    for x in range(max(x1, -50), min(x2, 50) + 1):
        for y in range(max(y1, -50), min(y2, 50) + 1):
            for z in range(max(z1, -50), min(z2, 50) + 1):
                map[(x, y, z)] = on
print(sum(map.values()))

# part 2
flatten = lambda lst: [item for sublist in lst for item in sublist]

def breakup1d(a, b):
    (a1, a2), (b1, b2) = a, b

    if a1 <= b1 <= a2 and a1 <= b2 <= a2: # --|---|--
        return [(a1, b1-1), (b1, b2), (b2+1, a2)]
    elif a1 <= b2 <= a2: # |  ---|----
        return [(a1, b2), (b2+1, a2)]
    elif a1 <= b1 <= a2: # ----|---  |
        return [(a1, b1-1), (b1, a2)]
    else: # | ---- |
        return [(a1, a2)]

def minus(cube1, cube2):
    if not intersects(cube1, cube2):
        return [cube1]

    (c1x, c1y, c1z) = cube1
    (c2x, c2y, c2z) = cube2

    xs = breakup1d(c1x, c2x)
    ys = breakup1d(c1y, c2y)
    zs = breakup1d(c1z, c2z)
    cubelets = product(xs, ys, zs)
    return [c for c in cubelets if not intersects(c, cube2)]

def intersects1d(a, b):
    (a1, a2), (b1, b2) = a, b
    return a1 <= b1 <= a2 \
        or a1 <= b2 <= a2 \
        or (b1 <= a1 and b2 >= a2)

def intersects(cube1, cube2):
    (c1x, c1y, c1z) = cube1
    (c2x, c2y, c2z) = cube2
    return intersects1d(c1x, c2x) and intersects1d(c1y, c2y) and intersects1d(c1z, c2z)

def area(cube):
    ((x1, x2), (y1, y2), (z1, z2)) = cube
    return (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)

on_regions = []
for on, cube in regions:
    on_regions = flatten([minus(region, cube) for region in on_regions]) + ([cube] if on else [])
print(sum(area(cube) for cube in on_regions))
