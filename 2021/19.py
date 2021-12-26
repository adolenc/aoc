# https://adventofcode.com/2021/day/19
import sys
from itertools import product, permutations
from collections import defaultdict


input = [line.strip() for line in sys.stdin]
scanners = []
for line in input:
    if line.startswith('---'):
        scanners.append(set())
    elif line != '':
        scanners[-1].add(tuple(int(p) for p in line.split(',')))

# part 1
def transform(beacons, s, i, d):
    return {(s[0] * b[i[0]] + d[0],
             s[1] * b[i[1]] + d[1],
             s[2] * b[i[2]] + d[2]) for b in beacons}

def overlaps(scanner1, scanner2):
    signs = product(*[[-1, 1]] * 3)
    indices = permutations(range(3))
    for s, i in product(signs, indices):
        # relative_positions = {(s[0] * b[i[0]], s[1] * b[i[1]], s[2] * b[i[2]]) for b in scanner2}
        relative_positions = transform(scanner2, s, i, (0, 0, 0))
        for b1 in scanner1:
            for b2 in relative_positions:
                d = (b1[0] - b2[0], b1[1] - b2[1], b1[2] - b2[2])
                # d = (b1[0] - b2[0], b1[1] - b2[1])
                new_positions = {(b[0] + d[0], b[1] + d[1], b[2] + d[2]) for b in relative_positions}
                # new_positions = {(b[0] + d[0], b[1] + d[1]) for b in relative_positions}
                if len(new_positions & scanner1) >= 12:
                # if len(new_positions & scanner1) >= 3:
                    return s, i, d
    return None


sc = defaultdict(list)
for i, scanner1 in enumerate(scanners):
    for j, scanner2 in enumerate(scanners):
        if i == j: continue
        if m := overlaps(scanner1, scanner2):
            sc[i] += [(j, m)]

accounted_for_scanners = [False] * len(scanners)
accounted_for_scanners[0] = True
map = scanners[0]
def account_for_scanner(scanner_id, transformations):
    global accounted_for_scanners, map
    for next_scanner, (s, i, d) in sc[scanner_id]:
        if accounted_for_scanners[next_scanner]:
            continue
        accounted_for_scanners[next_scanner] = True
        account_for_scanner(next_scanner, [(s,i,d)] + transformations)
        bc = scanners[next_scanner]
        for ss,ii,dd in [(s,i,d)] + transformations:
            bc = transform(bc, ss,ii,dd)
        map = map | bc

account_for_scanner(0, [((1,1,1), (0,1,2), (0,0,0))])
print(len(map))

# part 2
accounted_for_scanners = [None] * len(scanners)
accounted_for_scanners[0] = (0, 0, 0)
map = [(0, 0, 0)] * len(scanners)
def scanner_pos(scanner_id, transformations):
    global accounted_for_scanners, map
    for next_scanner, (s, i, d) in sc[scanner_id]:
        if accounted_for_scanners[next_scanner]:
            continue
        accounted_for_scanners[next_scanner] = True
        scanner_pos(next_scanner, [(s,i,d)] + transformations)
        bc = {(0, 0, 0)}
        for ss,ii,dd in [(s,i,d)] + transformations:
            bc = transform(bc, ss,ii,dd)
        map[next_scanner] = next(iter(bc))

def manhattan(a, b):
    x1,y1,z1 = a
    x2,y2,z2 = b
    return abs(x2-x1) + abs(y2-y1) + abs(z2-z1)

scanner_pos(0, [((1,1,1), (0,1,2), (0,0,0))])
print(max(manhattan(a, b) for a in map for b in map))
