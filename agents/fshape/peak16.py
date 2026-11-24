"""PEAK fails as a set inclusion at slack 16: x = (3, 4, 3, 3, 2, 1).  Independent check (no shared F code):
a placement of x 0 is exhibited, and the shifted state is shown unreachable for x 1 0 -1 by exhaustive search
and by an explicit weight certificate."""
from itertools import permutations
x = (3, 4, 3, 3, 2, 1)
def sums(w): return [2 * (j + 1) + e for j, e in enumerate(w)]
def reach(T):
    S = {(frozenset(), frozenset())}
    for t in T:
        S = {(A | {r}, B | {t - r}) for A, B in S for r in range(1, t) if r not in A and t - r not in B}
    return S
Tu, Tv = sums(x + (0,)), sums(x + (1, 0, -1))
Fu, Fv = reach(Tu), reach(Tv)
sh2 = lambda A: frozenset(a + 2 for a in A) | {1, 2}
bad = sorted((sorted(A), sorted(B)) for A, B in Fu if (sh2(A), sh2(B)) not in Fv)
print("sums of x 0     :", Tu); print("sums of x 1 0 -1:", Tv)
print(f"|F(x 0)| = {len(Fu)}, |F(x 1 0 -1)| = {len(Fv)}, states of F(x 0) missing from F(x 1 0 -1): {len(bad)}")
for A, B in bad:
    w = next(p for p in permutations(B) if sorted(a + b for a, b in zip(A, p)) == Tu)
    print("  rows", A, "cols", B, " placement of x 0:", list(zip(A, w)))
    print("     shifted target: rows", sorted(sh2(frozenset(A))), "cols", sorted(sh2(frozenset(B))))
# The missed states are alive: completing the first one to a permutation of size 13 gives the word w = x 0 y below.
# The longer word x 1 0 -1 y (size 15) is still solvable, through a different state at the cut.
def solve(T, n):
    def rec(i, R, C):
        if i == len(T): return []
        for r in range(max(1, T[i] - n), min(n, T[i] - 1) + 1):
            c = T[i] - r
            if r in R or c in C: continue
            got = rec(i + 1, R | {r}, C | {c})
            if got is not None: return [(r, c)] + got
        return None
    return rec(0, frozenset(), frozenset())
y = (-1, -2, -3, -4, -3, -3)
short = [(1, 4), (2, 11), (3, 8), (4, 5), (5, 3), (7, 7), (11, 1), (6, 10), (8, 9), (9, 12), (10, 13), (12, 6), (13, 2)]
assert sorted(a + b for a, b in short) == sums(x + (0,) + y) and len({a for a, b in short}) == len({b for a, b in short}) == 13
print("x 0 y      =", x + (0,) + y, "has the witness", short)
print("x 1 0 -1 y =", x + (1, 0, -1) + y, "has the witness", solve(sums(x + (1, 0, -1) + y), 15))
# Third check, with the window machine of ../interface/rewrite.py (the code behind run_rule.py), bound 17:
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "interface"))
from rewrite import machine, run
step, start = machine(17)
S = run(frozenset([start]), 0, None, x, 17, step, 1)
a, b = run(S, sum(x), x[-1], (0,), 17, step, 1), run(S, sum(x), x[-1], (1, 0, -1), 17, step, 1)
print(f"window machine: |F(x 0)| = {len(a)}, |F(x 1 0 -1)| = {len(b)}, missing {len(a - b)}")
