# https://adventofcode.com/2020/day/22
import sys
from copy import copy


input = sys.stdin


# part 1
p1_in, p2_in = [list(map(int, x.split('\n')[1:])) for x in input.read().strip().split('\n\n')]

p1_cards, p2_cards = p1_in[:], p2_in[:]
while p1_cards and p2_cards:
    p1, p2 = p1_cards[0], p2_cards[0]
    round_winner = max(p1, p2)
    p1_cards = p1_cards[1:] + ([p1, p2] if round_winner == p1 else [])
    p2_cards = p2_cards[1:] + ([p2, p1] if round_winner == p2 else [])

winning_deck = p1_cards or p2_cards
print(sum([a * b for a, b in zip(winning_deck[::-1], range(1, len(winning_deck) + 1))]))

# part 2
def game(p1_cards, p2_cards):
    round_history = set()
    while p1_cards and p2_cards:
        if (tuple(p1_cards), tuple(p2_cards)) in round_history:
            return ('p1', p1_cards)
        round_history.add((tuple(p1_cards), tuple(p2_cards)))

        p1, p2 = p1_cards[0], p2_cards[0]
        if p1 <= len(p1_cards[1:]) and p2 <= len(p2_cards[1:]):
            round_winner = game(copy(p1_cards[1:p1+1]), copy(p2_cards[1:p2+1]))[0]
            p1_cards = p1_cards[1:] + ([p1, p2] if round_winner == 'p1' else [])
            p2_cards = p2_cards[1:] + ([p2, p1] if round_winner == 'p2' else [])
        else:
            round_winner = max(p1, p2)
            p1_cards = p1_cards[1:] + ([p1, p2] if round_winner == p1 else [])
            p2_cards = p2_cards[1:] + ([p2, p1] if round_winner == p2 else [])
    return ('p1', p1_cards) if p1_cards else ('p2', p2_cards)

winning_deck = game(p1_in[:], p2_in[:])[1]
print(sum((a * b) for a, b in zip(winning_deck[::-1], range(1, len(winning_deck) + 1))))
