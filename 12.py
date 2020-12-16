# https://adventofcode.com/2020/day/12
import sys


input = [line.strip() for line in sys.stdin]



# part 1
input = [(l[0], int(l[1:])) for l in input]
moves = {'N': (0, 1),
         'E': (1, 0),
         'S': (0, -1),
         'W': (-1, 0)}
turns = {'L': -1,
         'R': 1}

def add(u, v): return (u[0] + v[0], u[1] + v[1])
def mul(u, c): return (u[0] * c, u[1] * c)
def manhattan(pos): return sum(map(abs, pos))

pos = (0, 0)
heading = 'E'
for op, n in input:
    if op == 'F': pos = add(pos, mul(moves[heading], n))
    if op in moves: pos = add(pos, mul(moves[op], n))
    if op in turns: heading = list(moves.keys())[(list(moves.keys()).index(heading) + n // 90 * turns[op]) % 4]

print(manhattan(pos))

# part 2
ship_pos = (0, 0)
waypoint_pos = (10, 1)
for op, n in input:
    if op == 'F': ship_pos = add(ship_pos, mul(waypoint_pos, n))
    if op in moves: waypoint_pos = add(waypoint_pos, mul(moves[op], n))
    if op in turns: 
        if op == 'L':
            while n > 0:
                waypoint_pos = (-waypoint_pos[1], waypoint_pos[0])
                n -= 90
        if op == 'R':
            while n > 0:
                waypoint_pos = (waypoint_pos[1], -waypoint_pos[0])
                n -= 90

print(manhattan(ship_pos))
