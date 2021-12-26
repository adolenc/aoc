# https://adventofcode.com/2021/day/23
import sys
from copy import deepcopy
import heapq
from collections import defaultdict


input = [line for line in sys.stdin]

# part 1
end_state_p = """\
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
"""
valid_states = """\
#############
#oo.o.o.o.oo#
###o#o#o#o###
  #o#o#o#o#
  #########
"""

positions = [(y, x) for y, row in enumerate(valid_states.split('\n')) for x, c in enumerate(row) if c == 'o']
start_state = {(y, x): char for y, row in enumerate(input) for x, char in enumerate(row) if char in 'ABCD'}
end_state = {(y, x): char for y, row in enumerate(end_state_p.split('\n')) for x, char in enumerate(row) if char in 'ABCD'}
costs = dict(A=1, B=10, C=100, D=1000)


def has_unobstructed_walk(from_position, to_position, state):
    from_y, from_x = from_position
    to_y, to_x = to_position
    positions = []

    if from_y == 1:
        positions += [(y, to_x) for y in range(2, to_y+1)]
    else:
        positions += [(y, from_x) for y in range(1, from_y)]

    if from_x < to_x:
        positions += [(1, x) for x in range(from_x+1, to_x+1)]
    else:
        positions += [(1, x) for x in range(to_x, from_x)]
    return all(pos not in state for pos in positions)


def can_move(char, from_position, to_position, state):
    from_y, _ = from_position
    to_y, to_x = to_position
    if from_position == to_position: # cant move to the same position
        return False
    if to_position in state: # cant move somewhere thats already taken
        return False
    if to_y == from_y == 1: # cant just move within the top row
        return False
    if from_y == 1: # moving from top into end place
        if end_state[to_position] == char:
            other_y_in_room = range(to_y+1, len(input)-1)
            if to_position not in state and all(state.get((y, to_x), '.') == char for y in other_y_in_room):
                # check if anyone is on our way
                return has_unobstructed_walk(from_position, to_position, state)
            else:
                return False
        else:
            return False
    if from_y > 1 and to_y == 1:
        # moving from down under should only be possible if we are in incorrect column or column is not complete
        other_y_in_room = range(to_y+1, len(input)-1)
        if end_state[from_position] != char or not all(state.get((y, to_x), '.') == char for y in other_y_in_room):
            return has_unobstructed_walk(from_position, to_position, state)
        else:
            return False
    return False


def all_valid_moves(state):
    states = []
    for position, char in state.items():
        for target_position in positions:
            if can_move(char, position, target_position, state):
                s = deepcopy(state)
                del s[position]
                s[target_position] = char
                cost = manhattan(position, target_position) * costs[char]
                states.append((s, cost))
    return states

def is_final_position(state):
    return all(position in end_state and char == end_state[position] for position, char in state.items())

def state_to_str(state):
    lst = [['.' for _ in range(13)] for _ in range(7)]
    for (y, x), char in state.items():
        lst[y][x] = char
    return ''.join(''.join(z) for z in lst)

def str_to_state(state_str):
    state = {}
    for i in range(len(state_str)):
        if state_str[i] in 'ABCD':
            state[(i // 13, i % 13)] = state_str[i]
    return state

def dijkstra(start_state):
    visited = set()
    Q = []
    dist = defaultdict(lambda: float('inf'))
    dist[state_to_str(start_state)] = 0
    heapq.heappush(Q, (0, state_to_str(start_state)))

    while Q:
        _, u = heapq.heappop(Q)
        visited.add(u)
        u_state = str_to_state(u)
        # print(len(dist), len(Q))

        for v_state, length in all_valid_moves(u_state):
            v = state_to_str(v_state)
            if v in visited:
                continue

            alt = dist[u] + length
            if alt < dist[v]:
                dist[v] = alt
                heapq.heappush(Q, (alt, v))
    return dist

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

a = dijkstra(start_state)
print(a[state_to_str(end_state)])

# part 2
end_state_p = """\
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########
"""
valid_states = """\
#############
#oo.o.o.o.oo#
###o#o#o#o###
  #o#o#o#o#
  #o#o#o#o#
  #o#o#o#o#
  #########
"""
input = input[:3] + [
"  #D#C#B#A#",
"  #D#B#A#C#",
] + input[3:]

positions = [(y, x) for y, row in enumerate(valid_states.split('\n')) for x, c in enumerate(row) if c == 'o']
start_state = {(y, x): char for y, row in enumerate(input) for x, char in enumerate(row) if char in 'ABCD'}
end_state = {(y, x): char for y, row in enumerate(end_state_p.split('\n')) for x, char in enumerate(row) if char in 'ABCD'}


a = dijkstra(start_state)
print(a[state_to_str(end_state)])
