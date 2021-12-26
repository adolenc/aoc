# https://adventofcode.com/2021/day/15
import sys
import heapq
from collections import defaultdict


input = [line.strip() for line in sys.stdin]
weights = [[int(i) for i in l] for l in input]


# part 1
def neighbors(node, G):
    move_deltas = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    y, x = node
    n = [(y+dy, x+dx) for dy, dx in move_deltas]
    n = [(y, x) for y, x in n if 0 <= y < len(G) and 0 <= x < len(G[0])]
    return (((y, x), G[y][x]) for y, x in n)


def dijkstra(G):
    visited = set()
    Q = []
    dist = defaultdict(lambda: float('inf'))
    start = (0, 0)
    dist[start] = 0
    heapq.heappush(Q, (0, start))
 
    while Q:
        _, u = heapq.heappop(Q)
        visited.add(u)
 
        for v, length in neighbors(u, G):
            if v in visited:
                continue

            alt = dist[u] + length
            if alt < dist[v]:
                dist[v] = alt
                heapq.heappush(Q, (alt, v))
    return dist

print(dijkstra(weights)[(len(weights)-1, len(weights[0])-1)])

# part 2
new_w = lambda y, x: (weights[y % len(weights)][x % len(weights[0])] + (y // len(weights)) + (x // len(weights[0])) - 1) % 9 + 1
w2 = [[new_w(y, x) for x in range(len(weights[0]) * 5)] for y in range(len(weights) * 5)]
print(dijkstra(w2)[(len(w2)-1, len(w2[0])-1)])
