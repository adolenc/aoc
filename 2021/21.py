# https://adventofcode.com/2021/day/21
import sys
from functools import lru_cache
from itertools import product


input = [line.strip() for line in sys.stdin]


# part 1
positions = [int(player.split(':')[1]) for player in input]
scores = [0, 0]
die = list(range(1, 100+1)) + list(range(1, 100+1))

def clock_mod(i, m):
    return (i % m) or m

i = 0
total_rolls = 0
player = 0
while True:
    positions[player] = clock_mod(positions[player] + sum(die[i:i+3]), 10)
    scores[player] += positions[player]
    i = (i + 3) % 100
    total_rolls += 3
    if scores[player] >= 1000:
        break
    player = 1 - player

print(min(scores) * total_rolls)

# part 2
positions = tuple([int(player.split(':')[1]) for player in input])
scores = tuple([0, 0])

@lru_cache(None)
def play(positions, scores, player):
    wins = [0, 0]
    for rolls in product(*[[1, 2, 3]] * 3):
        new_position = clock_mod(positions[player] + sum(rolls), 10)
        positions2 = (new_position if player == 0 else positions[0],
                      new_position if player == 1 else positions[1])
        scores2 = (scores[0] + (new_position if player == 0 else 0),
                   scores[1] + (new_position if player == 1 else 0))
        if scores2[player] >= 21:
            wins[player] += 1
        else:
            new_wins = play(positions2, scores2, 1 - player)
            wins[0] += new_wins[0]
            wins[1] += new_wins[1]
    return wins

print(max(play(positions, scores, 0)))
