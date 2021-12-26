# https://adventofcode.com/2021/day/17
import sys


input = [line.strip() for line in sys.stdin]

# part 1
_, _, xr, yr = input[0].split(' ')
x1, x2 = [int(x) for x in xr[2:-1].split('..')]
y1, y2 = [int(y) for y in yr[2:].split('..')]
x1, x2 = min(x1, x2), max(x1, x2)
y1, y2 = max(y1, y2), min(y1, y2)

print(sum(range(1, -y2)))

# part 2
def sim(dx, dy):
    x, y = (0, 0)
    while x <= x2 and y >= y2:
        if x1 <= x <= x2 and y2 <= y <= y1:
            return True
        x += max(dx, 0)
        y += dy
        dx -= 1
        dy -= 1
    return False

print(sum(sim(x, y) for x in range(x2+1) for y in range(y2, -y2)))
