# https://adventofcode.com/2021/day/13
import sys


input = [line.strip() for line in sys.stdin]


# part 1
split = input.index('')
points = [tuple(map(int, l.split(','))) for l in input[:split]]

folds = [l.split('=') for l in input[split+1:]]
folds = [(axis[-1], int(n)) for axis, n in folds]

res = set(points)
for i, (axis, line) in enumerate(folds):
    if axis == 'y':
        res = {(x, line-abs(y-line)) for x, y in res}
    if axis == 'x':
        res = {(line-abs(x-line), y) for x, y in res}

    is_first_fold = i == 0
    if is_first_fold:
        print(len(res))

# part 2
m = [[' '] * 39 for _ in range(6)]
for x, y in res:
    m[y][x] = 'x'
for mm in m:
    print(''.join(mm))
