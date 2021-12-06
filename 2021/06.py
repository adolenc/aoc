# https://adventofcode.com/2021/day/6
import sys
from collections import Counter


input = [line.strip() for line in sys.stdin]
ages_in = [int(s) for s in input[0].split(',')]


# part 1
def count_fish(final_day):
    fish = dict(Counter(ages_in))
    for _ in range(final_day):
        for age in range(0, 9):
            fish[age - 1] = fish.get(age, 0)
        fish[8] = fish[-1]
        fish[6] = fish[-1] + fish[6]
        del fish[-1]
    return sum(fish.values())

print(count_fish(80))

# part 2
print(count_fish(256))
