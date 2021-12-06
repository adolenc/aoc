# https://adventofcode.com/2021/day/3
import sys
from collections import Counter


input = [line.strip() for line in sys.stdin]


# part 1
count_bits_on_pos = lambda bytes, n: Counter([list(i) for i in zip(*bytes)][n])

counts = [count_bits_on_pos(input, n) for n in range(len(input[0]))]
gam = ''.join(['1' if cnt['1'] > cnt['0'] else '0' for cnt in counts])
eps = ''.join(['0' if cnt['1'] > cnt['0'] else '1' for cnt in counts])
print(int(gam, 2) * int(eps, 2))

# part 2
co = input[:]
ox = input[:]
for i in range(len(input[0])):
    if len(co) > 1:
        cocnt = count_bits_on_pos(co, i)
        co = [n for n in co if n[i] == ('1' if cocnt['0'] <= cocnt['1'] else '0')]
    if len(ox) > 1:
        oxcnt = count_bits_on_pos(ox, i)
        ox = [n for n in ox if n[i] == ('0' if oxcnt['0'] <= oxcnt['1'] else '1')]

print(int(co[0], 2) * int(ox[0], 2))
