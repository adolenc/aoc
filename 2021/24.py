# https://adventofcode.com/2021/day/24
import sys
from itertools import groupby


input = [line.strip() for line in sys.stdin]


# part 1
monad = [l.split(' ') for l in input]

def find_valid_input_zs(block, valid_end_zs, is_prefered_fn, max_possible_z):

    val = lambda v: state[v] if v in 'wxyz' else int(v)

    ops = {
        'inp': lambda a:    state.__setitem__(a, int(possible_input)),
        'add': lambda a, b: state.__setitem__(a, state[a] + val(b)),
        'mul': lambda a, b: state.__setitem__(a, state[a] * val(b)),
        'div': lambda a, b: state.__setitem__(a, state[a] // val(b)),
        'mod': lambda a, b: state.__setitem__(a, state[a] % val(b)),
        'eql': lambda a, b: state.__setitem__(a, 1 if val(a) == val(b) else 0)
    }

    valid_input_zs = {}
    for possible_input_z in range(max_possible_z):
        for possible_input in '123456789':
            state = dict(w=0, x=0, y=0, z=possible_input_z)
            for op, *args in block:
                ops[op](*args)
            if val('z') in valid_end_zs:
                valid_input = possible_input + valid_end_zs[val('z')]
                if possible_input_z not in valid_input_zs or is_prefered_fn(int(valid_input), int(valid_input_zs[possible_input_z])):
                    valid_input_zs[possible_input_z] = valid_input
    return valid_input_zs

def find_accepted_input(program, is_prefered_fn = int.__gt__):
    program_blocks = []
    for instruction in program:
        if instruction[0] == 'inp': program_blocks.append([])
        program_blocks[-1].append(instruction)

    max_possible_z = 10
    while True:
        valid_input_zs_for_next_block = {0: ''}
        for block in program_blocks[::-1]:
            valid_input_zs_for_next_block = find_valid_input_zs(block, valid_input_zs_for_next_block, is_prefered_fn, max_possible_z)

        if not valid_input_zs_for_next_block:
            max_possible_z *= 10
        else:
            return valid_input_zs_for_next_block

print(find_accepted_input(monad)[0])

# part 2
print(find_accepted_input(monad, int.__lt__)[0])
