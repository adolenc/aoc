# https://adventofcode.com/2021/day/2
import sys


input = [line.strip().split() for line in sys.stdin]


# part 1
hor = 0
dep = 0
for dir, X in input:
    if dir == 'forward': hor += int(X)
    if dir == 'up': dep -= int(X)
    if dir == 'down': dep += int(X)

print(hor * dep)

# part 2
aim = 0
hor = 0
dep = 0
for dir, X in input:
    if dir == 'forward':
        hor += int(X)
        dep += aim * int(X)
    if dir == 'up':
        aim -= int(X)
    if dir == 'down':
        aim += int(X)

print(hor * dep)
