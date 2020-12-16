# https://adventofcode.com/2020/day/15
import sys
from itertools import islice, count


input = list(map(int, sys.stdin.read().split(',')))


# part 1
def play():
    mem = {last: i for i, last in enumerate(input, 1)}
    for last in input:
        yield last
    last = input[-1]
    for i in count(len(input)):
        yield (current := 0 if last not in mem else i - mem[last])
        mem[last] = i
        last = current

print(next(islice(play(), 2020 - 1, None)))

# part 2
print(next(islice(play(), 30000000 - 1, None)))
