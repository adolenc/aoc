# https://adventofcode.com/2021/day/1

import sys

input = [int(line.strip()) for line in sys.stdin]

# part 1
print(sum(a < b for a, b in zip(input, input[1:])))


# part 2
print(sum(a + b + c < b + c + d for a, b, c, d in zip(input, input[1:], input[2:], input[3:])))
