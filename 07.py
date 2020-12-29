# https://adventofcode.com/2020/day/7
import sys
import re
from collections import defaultdict


input = [line.strip() for line in sys.stdin]


# part 1
flatten = lambda lst: [e for slst in lst for e in slst]

Gbwd = defaultdict(list) # unweighted directed graph Gbwd[from] = [to]
Gfwd = defaultdict(dict) # weighted directed graph Gfwd[from][to] = int(weight)
for line in input:
    container, containees = line.split(' bags contain ')
    if containees == 'no other bags.': continue

    for count, containee in re.findall(r'(\d+?) (.*?) bag', containees):
        Gbwd[containee] += [container]
        Gfwd[container][containee] = int(count)

def all_reachable_nodes_from(G, v):
    if v not in G: return set([v])
    return set([v] + flatten([all_reachable_nodes_from(G, neighbour) for neighbour in G[v]]))

print(len(all_reachable_nodes_from(Gbwd, 'shiny gold')) - 1)

# part 2
def count_bags_in(G, v):
    if v not in G: return 1
    return 1 + sum(G[v][neighbor] * count_bags_in(G, neighbor) for neighbor in G[v])

print(count_bags_in(Gfwd, 'shiny gold') - 1)
