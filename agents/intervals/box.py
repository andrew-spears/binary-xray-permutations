"""Is the reachable set of the partition machine 'all partitions of the slack with partial sums between two bounds'?
usage: python3 box.py n"""
import sys
from iv import words
from pm import succ
def parts(s, mx=None):
    if mx is None: mx = s
    if s == 0: yield (); return
    for a in range(min(s, mx), 0, -1):
        for r in parts(s - a, a): yield (a,) + r
n = int(sys.argv[1]); seen = {}; 
for w in words(n):
    F = {()}
    for k, e in enumerate(w):
        if w[:k + 1] in seen: F = seen[w[:k + 1]]; continue
        F = frozenset(v for u in F for v in succ(u, e)); seen[w[:k + 1]] = F
tot = bad = badcol = 0; ex = []
for x, F in seen.items():
    s = sum(x); L = len(x)
    ps = lambda u, j: sum(u[:j])
    lo = [min(ps(u, j) for u in F) for j in range(L + 1)]; hi = [max(ps(u, j) for u in F) for j in range(L + 1)]
    cj = lambda u: tuple(sum(1 for p in u if p > i) for i in range(u[0] if u else 0))
    lo2 = [min(ps(cj(u), j) for u in F) for j in range(s + 1)]; hi2 = [max(ps(cj(u), j) for u in F) for j in range(s + 1)]
    B = [u for u in parts(s) if len(u) <= L and all(lo[j] <= ps(u, j) <= hi[j] for j in range(L + 1))]
    B2 = [u for u in B if all(lo2[j] <= ps(cj(u), j) <= hi2[j] for j in range(s + 1))]
    tot += 1
    if len(B) != len(F): bad += 1
    if len(B2) != len(F):
        badcol += 1
        if len(ex) < 4: ex.append((x, sorted(set(B2) - F)[:4], len(F)))
print(f"n = {n}: {tot} prefixes; reachable set != box of row partial sums: {bad}; != box of row and column partial sums: {badcol}")
for t in ex: print("  ", t)
