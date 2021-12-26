# https://adventofcode.com/2021/day/14
import sys
from collections import Counter, defaultdict


input = [line.strip() for line in sys.stdin]
start = input[0]
rules = dict([l.split(' -> ') for l in input[2:]])

# part 1
result = start
for _ in range(10):
    result = ''.join(a + rules[a + b] for a, b in zip(result, result[1:])) + result[-1]
c = Counter(result)
print(max(c.values()) - min(c.values()))

# part 2
pair_count = Counter(a + b for a, b in zip(start, start[1:]))
element_count = Counter(start)
for _ in range(40):
    next_pair_count = defaultdict(int)
    for production, frequencies in pair_count.items():
        next_pair_count[production[0] + rules[production]] += frequencies
        next_pair_count[rules[production] + production[1]] += frequencies
        element_count[rules[production]] += frequencies
    pair_count = next_pair_count
print(max(element_count.values()) - min(element_count.values()))
