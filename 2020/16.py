# https://adventofcode.com/2020/day/16
import sys
import re
from math import prod


input = sys.stdin.read().split('\n\n')


# part 1
flatten = lambda lst: [e for slst in lst for e in slst]

rules = {}
for l in input[0].split('\n'):
    field, value_ranges = l.split(':')
    rules[field] = [tuple(map(int, range)) for range in re.findall(r'(\d+)-(\d+)', value_ranges)]

my_ticket = list(map(int, input[1].split('\n')[1].split(',')))
nearby_tickets = [list(map(int, line.split(','))) for line in input[2].split('\n')[1:-1]]

def satisfies(n, field):
    return any(a <= n <= b for a, b in rules[field])

print(sum(n for n in flatten(nearby_tickets) if not any(satisfies(n, field) for field in rules)))

# part 2
nearby_tickets = [ticket for ticket in nearby_tickets if all(any(satisfies(n, f) for f in rules) for n in ticket)]
possible_fields = [set(rules) for _ in rules]

# eliminate as many fields as possible based on ticket data
for ticket in nearby_tickets:
    for n, f in zip(ticket, possible_fields):
        for field in rules:
            if not satisfies(n, field):
                f -= set([field])

# propagate the constraints
while any(len(p) > 1 for p in possible_fields):
    for f1 in possible_fields:
        if len(f1) > 1: continue

        for f2 in possible_fields:
            if f1 != f2:
                f2 -= f1

print(prod(n for n, f in zip(my_ticket, flatten(possible_fields)) if f.startswith('departure')))
