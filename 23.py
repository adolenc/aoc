# https://adventofcode.com/2020/day/23
import sys
from math import prod


input = sys.stdin


# part 1
cups = list(map(int, input.read().strip()))

class Cup:
    def __init__(self, value):
        self.value = value

def to_cyclic_linkedlist(vals):
    head = cup = Cup(vals[0])
    for v in vals[1:]:
        cup.next = Cup(v)
        cup = cup.next
    cup.next = head
    return head

def to_list_of_cups(cups, length):
    def to_list_of_cups_helper(cup):
        for _ in range(length):
            yield cup
            cup = cup.next
    return list(to_list_of_cups_helper(cups))

def to_list(cups, length):
    return [c.value for c in to_list_of_cups(cups, length)]


def play(list_of_cups, move_count):
    current_cup = to_cyclic_linkedlist(list_of_cups)
    cup_map = {c.value: c for c in to_list_of_cups(current_cup, len(list_of_cups))}
    max_cup = max(list_of_cups)
    modulo_minus_one = lambda v: ((v - 1 - 1) % max_cup) + 1

    for _ in range(move_count):
        # extract three cups
        three_cups = current_cup.next
        current_cup.next = three_cups.next.next.next
        # find destination cup
        destination_cup_val = modulo_minus_one(current_cup.value)
        while destination_cup_val in to_list(three_cups, 3):
            destination_cup_val = modulo_minus_one(destination_cup_val)
        destination_cup = cup_map[destination_cup_val]
        # re-insert the three cups
        three_cups.next.next.next = destination_cup.next
        destination_cup.next = three_cups
        # move to the next cup
        current_cup = current_cup.next

    return cup_map

print(''.join(map(str, to_list(play(cups, 100)[1].next, 8))))

# part 2
cups += list(range(len(cups)+1, 1_000_000+1))
print(prod(to_list(play(cups, 10_000_000)[1].next, 2)))
