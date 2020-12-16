# https://adventofcode.com/2020/day/10
import sys
from collections import Counter
from functools import lru_cache


input = [int(line) for line in sys.stdin]


# part 1
input = sorted(input + [0] + [max(input) + 3])
cumsums = [b - a for a, b in zip(input, input[1:])]

print(Counter(cumsums)[1] * (Counter(cumsums)[3]))

# part 2
@lru_cache
def dp(i):
    if i < 0: return 0
    if i == 0: return 1
    return sum(dp(i - prev)
               for prev in range(1, 4)
               if input[i - prev] + 3 >= input[i])

print(dp(len(input) - 1))
