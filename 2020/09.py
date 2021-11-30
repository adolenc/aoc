# https://adventofcode.com/2020/day/9
import sys


input = [int(line) for line in sys.stdin]


# part 1
def two_sums_to(sum, arr): return any(sum - n in arr for n in arr)

PREAMBLE = 25
invalid = next(n for i, n in enumerate(input[PREAMBLE:], PREAMBLE)
               if not two_sums_to(n, input[i - PREAMBLE:i]))
print(invalid)

# part 2
a, b, cumsum = 0, 0, 0
while cumsum != invalid:
    if cumsum > invalid:
        cumsum -= input[a]
        a += 1
    elif cumsum < invalid:
        cumsum += input[b]
        b += 1
# a, b = (next((a, b) for a in range(len(input)) for b in range(len(input)) if sum(input[a:b]) == invalid))
print(min(input[a:b]) + max(input[a:b]))
