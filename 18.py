# https://adventofcode.com/2020/day/18
import sys
import re
from math import prod


input = [line.strip() for line in sys.stdin]


# part 1
def tokenize(line):
    return re.findall(r'\d+|[()+*]', line)

def parse(tokens):
    i, result = 0, []
    while i < len(tokens):
        t = tokens[i]
        if t.isdigit(): result += [int(t)]
        elif t in '*+': result += [t]
        elif t == '(':
            parens, new_idx = parse(tokens[i + 1:])
            result += [parens]
            i += new_idx
        elif t == ')':
            return result, i + 1
        i += 1
    return result

def evl(exp):
    if isinstance(exp, int): return exp
    if len(exp) == 1: return evl(exp[0])
    if exp[1] == '+': return evl([evl(exp[0]) + evl(exp[2])] + exp[3:])
    if exp[1] == '*': return evl([evl(exp[0]) * evl(exp[2])] + exp[3:])


print(sum(evl(parse(tokenize(line))) for line in input))

# part 2
def evl(exp):
    exp = [evl(e) if isinstance(e, list) else e for e in exp]
    exp = ''.join(map(str, exp))
    sums = exp.split('*')
    prods = (sum(map(int, s.split('+'))) for s in sums)
    return prod(prods)

print(sum(evl(parse(tokenize(line))) for line in input))
