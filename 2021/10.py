# https://adventofcode.com/2021/day/10
import sys
from functools import reduce


input = [line.strip() for line in sys.stdin]


# part 1
pairs = ['()', '{}', '<>', '[]']
opening = {p[0]: p[1] for p in pairs}
closing = {p[1]: p[0] for p in pairs}

points = {')': 3, ']': 57, '}': 1197, '>': 25137}
unfinished_lines = []
score = 0
for line in input:
    stack = []
    for c in line:
        if c in opening:
            stack.append(c)
        else: # if c in closing:
            if closing[c] == stack[-1]:
                stack.pop()
            else:
                score += points[c]
                break
    else:
        unfinished_lines.append(''.join(stack))
print(score)


# part 2
points = {')': 1, ']': 2, '}': 3, '>': 4}
scores = [reduce(lambda s, c: s * 5 + points[opening[c]], line[::-1], 0) for line in unfinished_lines]
print(sorted(scores)[len(scores)//2])
