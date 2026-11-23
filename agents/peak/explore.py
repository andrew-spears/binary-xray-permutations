"""Exploration helpers (absolute coordinates): F(S) = set of (rows, cols) over placements of the sum set S."""
import sys, itertools
from functools import lru_cache
def step(F, s):
    out = set()
    for A, B in F:
        for a in range(1, s):
            b = s - a
            if a not in A and b not in B: out.add((A | {a}, B | {b}))
    return out
def Fset(S):
    F = {(frozenset(), frozenset())}
    for s in sorted(S): F = step(F, s)
    return F
def sh(X, j=1):
    return frozenset(x + j for x in X) | frozenset(range(1, j + 1))
def words(N, B):
    """legal prefixes of length <= N with slack <= B, as sum tuples"""
    def rec(w, s):
        yield tuple(w)
        if len(w) == N: return
        lo = 0 if not w else max(-s, w[-1] - 1)
        for e in range(lo, B - s + 1):
            w.append(e); yield from rec(w, s + e); w.pop()
    yield from rec([], 0)
def sums(w): return [2 * (i + 1) + e for i, e in enumerate(w)]
