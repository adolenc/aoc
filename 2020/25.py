# https://adventofcode.com/2020/day/25
import sys


input = [line.strip() for line in sys.stdin]


# part 1
card_pubkey, door_pubkey = map(int, input)
subject_number = 7
value = 1
loop_size = 0
while value != card_pubkey:
    value = (value * subject_number) % 20201227
    loop_size += 1

print(pow(door_pubkey, loop_size, 20201227))
