"""Hereditarily distinct lists: build the list by appending k (0 <= k <= t) and decrementing the first k entries,
keeping all entries distinct at every stage.  Which valid D arise?"""
import sys
from lib import valid_sets
N = int(sys.argv[1])
level = {()}
for t in range(0, N):
    nxt = set()
    for L in level:
        for k in range(0, t + 1):
            M = tuple(x - 1 for x in L[:k]) + L[k:] + (k,)
            if len(set(M)) == t + 1: nxt.add(M)
    level = nxt; n = t + 1
    got = {tuple(sorted(L)) for L in level}; V = valid_sets(n)
    miss = [D for D in V if D not in got]
    print(n, "HD lists", len(level), "valid", len(V), "missing", len(miss), miss[:4])
