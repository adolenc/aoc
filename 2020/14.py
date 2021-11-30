# https://adventofcode.com/2020/day/14
import sys
import re
from collections import defaultdict
from itertools import combinations


input = [line.strip() for line in sys.stdin]


# part 1
opcodes = [re.findall(r'(mask|mem)(?:\[(\d+)\])? = (.*)', instr)[0] for instr in input]
mask = ''
mem = defaultdict(int)
for opcode, loc, val in opcodes:
    if opcode == 'mask': mask = val
    if opcode == 'mem':
        val = '{:036b}'.format(int(val))
        mem[int(loc)] = int(''.join(v if m == 'X' else m for v, m in zip(val, mask)), 2)

print(sum(mem.values()))

# part 2
def powerset(iterable):
    items = list(iterable)
    for r in range(len(items)+1):
        for c in combinations(items, r):
            yield c

mask = ''
mem = defaultdict(int)
for opcode, loc, val in opcodes:
    if opcode == 'mask': mask = val
    if opcode == 'mem':
        loc = '{:036b}'.format(int(loc))
        masked_loc = [v if m == '0' else '1' if m == '1' else '0' for v, m in zip(loc, mask)]
        for swaps in powerset(i for i, m in enumerate(mask) if m == 'X'):
            for swap in swaps:
                masked_loc[swap] = '1'
            mem[int(''.join(masked_loc), 2)] = int(val)
            for swap in swaps:
                masked_loc[swap] = '0'

print(sum(mem.values()))
