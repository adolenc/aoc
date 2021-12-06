# https://adventofcode.com/2021/day/4
import sys


input = [row.strip() for row in sys.stdin]
numbers = input[0].split(',')
boards = []
new_b = []
for l in input[2:] + ['']:
    if l == '':
        boards.append(new_b)
        new_b = []
    else:
        new_b.append(l.split())


# part 1
flatten = lambda lst: [item for sublist in lst for item in sublist]


def board_bingo(b, y, x):
    tr = [list(i) for i in zip(*b)]
    return ''.join(b[y]) == 'xxxxx' or ''.join(tr[x]) == 'xxxxx'

def score(b, n):
    s = sum(int(i) for i in flatten(b) if i.isdigit())
    return s * int(n)

def fill_in_board(b, n):
    for y, row in enumerate(b):
        for x, c in enumerate(row):
            if c == n:
                row[x] = 'x'
                if board_bingo(b, y, x):
                    return True
    return False

bingo_found = False
for n in numbers:
    for b in boards:
        if fill_in_board(b, n):
            print(score(b, n))
            bingo_found = True
            break
    if bingo_found:
        break


# part 2
for n in numbers:
    last_remaining_board = boards[0]
    boards = [b for b in boards if not fill_in_board(b, n)]
    if not boards:
        print(score(last_remaining_board, n))
        break
