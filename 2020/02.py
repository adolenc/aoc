# https://adventofcode.com/2020/day/2
import sys
from collections import Counter


input = [line.strip() for line in sys.stdin]


# part 1
def parse(line):
    lowest, highest, ch, _, password = line.replace(':', '-').replace('-', ' ').split(' ')
    return int(lowest), int(highest), ch, password

print(sum(a <= Counter(passw)[ch] <= b for a, b, ch, passw in map(parse, input)))

# part 2
print(sum((passw[a - 1] == ch) ^ (passw[b - 1] == ch) for a, b, ch, passw in map(parse, input)))
