# https://adventofcode.com/2021/day/12
import sys
from itertools import groupby


input = [line.strip() for line in sys.stdin]


# part 1
edges = [l.split('-') for l in input]
edges += [list(reversed(e)) for e in edges]
graph = {v1: {v[1] for v in v2} for v1, v2 in groupby(sorted(edges), lambda e: e[0])}

def flatten(lst):
    return [item for sublist in lst for item in sublist]

def dfs(start, G, current_path=None):
    if not current_path: current_path = []

    if start == 'end':
        return [current_path]

    return flatten(dfs(neigh, G, current_path + [neigh]) for neigh in G[start]
                   if neigh != 'start' and (neigh.isupper() or neigh not in current_path))

print(len(dfs('start', graph)))

# part 2
def dfs(start, G, current=None):
    if not current: current = []

    if start == 'end':
        return [current]

    solutions = []
    for neigh in G[start]:
        if neigh == 'start':
            continue

        if neigh.isupper() or neigh not in current:
            solutions += dfs(neigh, G, current + [neigh])
        else:
            smaller_visited = [v for v in current if v.islower()]
            if len(smaller_visited) == len(set(smaller_visited)):
                solutions += dfs(neigh, G, current + [neigh])
    return solutions

print(len(dfs('start', graph)))
