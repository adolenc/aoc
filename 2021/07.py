# https://adventofcode.com/2021/day/7
import sys


input = [line.strip() for line in sys.stdin]
input = [int(i) for i in input[0].split(',')]


# part 1
fuel_per_pos = [sum([abs(i - pos) for i in input]) for pos in range(min(input), max(input)+1)]
print(min(fuel_per_pos))

# part 2
fuel_per_pos = [sum([(abs(i - pos)*(abs(i - pos)+1))//2 for i in input]) for pos in range(min(input), max(input)+1)]
print(min(fuel_per_pos))
