"""General boards: all R, C subsets of {1..N} with |R|=|C|=m (R up to translation: require 1 in R or 1 in C).
Counts sum-test holes, LP-feasible holes, and holes surviving the parity-refined LP.
Usage: python3 general.py N m"""
import sys, itertools
from brute import sumtest, placement
from lp import lp_feasible
from modlp import modlp

N, m = int(sys.argv[1]), int(sys.argv[2])
cnt = dict(holes=0, lp=0, mod2=0); ex = {}
for R in itertools.combinations(range(1, N + 1), m):
    for C in itertools.combinations(range(1, N + 1), m):
        if 1 not in R and 1 not in C: continue
        if N not in R and N not in C: continue
        lo, hi = min(C) - max(R), max(C) - min(R)
        for D in itertools.combinations(range(lo, hi + 1), m):
            if not sumtest(R, C, D): continue
            if placement(R, C, D) is not None: continue
            cnt['holes'] += 1; ex.setdefault('holes', (R, C, D))
            if not lp_feasible(R, C, D): continue
            cnt['lp'] += 1; ex.setdefault('lp', (R, C, D))
            if not modlp(R, C, D, 2): continue
            cnt['mod2'] += 1; ex.setdefault('mod2', (R, C, D))
print(N, m, cnt, ex)
