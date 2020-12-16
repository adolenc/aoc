# https://adventofcode.com/2020/day/5
import sys


input = [line.strip() for line in sys.stdin]


# part 1
seats = set((int(l[:-3].replace('B', '1').replace('F', '0'), 2),
             int(l[-3:].replace('R', '1').replace('L', '0'), 2))
            for l in input)

print(max(row * 8 + col for row, col in seats))

# part 2
print(next(row * 8 + col
           for row in range(128)
           for col in range(8)
           if (row, col) not in seats and (row - 1, col) in seats and (row + 1, col) in seats))
