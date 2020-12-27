# https://adventofcode.com/2020/day/19
import sys


input = sys.stdin


# part 1
rules, messages = map(lambda l: l.strip().split('\n'), input.read().split('\n\n'))

def to_int_or_str(str): return str[1:-1] if str.startswith('"') else int(str)

grammar = {}
for rule in rules:
    a, b = rule.split(': ')
    grammar[int(a)] = [list(map(to_int_or_str, bi.split())) for bi in b.split(' | ')]

# part 1
def parse(msg, grammar, start):
    applicables = []
    for option in grammar[start]:
        restarts = [(0, msg)] # restarts is a list of (position within the option, evaluated msg) tuples
        while restarts:
            option_restart_idx, in_msg = restarts.pop()

            if option[option_restart_idx] in grammar: # another rule
                all_outcomes = parse(in_msg, grammar, option[option_restart_idx])
                for next_msg in [msg for satisfied, msg in all_outcomes if satisfied]:
                    if option_restart_idx + 1 >= len(option):
                        applicables += [(True, next_msg)]
                    else:
                        restarts += [(option_restart_idx + 1, next_msg)]
            else: # terminating character
                rule = option[option_restart_idx]
                if in_msg.startswith(rule):
                    applicables += [(True, in_msg[len(rule):])]
    if len(applicables) == 0:
        return [(False, '')]
    else:
        return applicables

print(sum(any(satisfied and leftover_msg == "" for satisfied, leftover_msg in possible_parsing)
          for possible_parsing in [parse(message, grammar, 0) for message in messages]))

# part 2
grammar = {**grammar,
           8:  [[42], [42, 8]],
           11: [[42, 31], [42, 11, 31]]}

print(sum(any(satisfied and leftover_msg == "" for satisfied, leftover_msg in possible_parsing)
          for possible_parsing in [parse(message, grammar, 0) for message in messages]))
