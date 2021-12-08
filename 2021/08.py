# https://adventofcode.com/2021/day/8
import sys
from itertools import permutations


input = [line.strip() for line in sys.stdin]
entries = [(line.split(' | ')[0].split(), line.split(' | ')[1].split()) for line in input]


# part 1
print(sum(sum(len(o) in [2, 4, 3, 7] for o in output_value) for _, output_value in entries))

# part 2
segments_to_digits = {
    'ooo.ooo': '0',
    '..o..o.': '1',
    'o.ooo.o': '2',
    'o.oo.oo': '3',
    '.ooo.o.': '4',
    'oo.o.oo': '5',
    'oo.oooo': '6',
    'o.o..o.': '7',
    'ooooooo': '8',
    'oooo.oo': '9'
}

toggle_segments = lambda mapping, input: ''.join('o' if c in input else '.' for c in mapping)

def segment_mapping_works_for(mapping, inputs):
    return all(toggle_segments(mapping, input) in segments_to_digits for input in inputs)

sum = 0
for signal_patterns, output_value in entries:
    for mapping in (''.join(p) for p in permutations('abcdefg')):
        if segment_mapping_works_for(mapping, set(signal_patterns + output_value)):
            sum += int(''.join(segments_to_digits[toggle_segments(mapping, c)] for c in output_value))
            break
print(sum)
