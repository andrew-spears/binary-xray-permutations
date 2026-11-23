"""Shared helpers for the COUNT experiments: all solutions of every word of length <= n by brute force.
A solution of w = (e_1..e_n) is a permutation whose stones, sorted by diagonal r + c, have r + c = 2k + e_k
(rows and columns 1..n).  stones(sigma) lists them in this 'time' order."""
import sys
from itertools import permutations
from collections import defaultdict
def stones(sig):
    return sorted(((i + 1, s + 1) for i, s in enumerate(sig)), key=lambda p: p[0] + p[1])
def solutions(nmax):
    """dict word -> list of stone lists, for all binary words of length 1..nmax"""
    sol = defaultdict(list)
    for n in range(1, nmax + 1):
        for sig in permutations(range(n)):
            d = sorted(i + s + 2 for i, s in enumerate(sig))
            if any(d[k] == d[k + 1] for k in range(n - 1)): continue
            sol[tuple(d[k] - 2 * (k + 1) for k in range(n))].append(stones(sig))
    return sol
def canon(w):
    """canonical shortening step of a valid nonzero word: (name, lo, u, v) with w = x v y, x = w[:lo]; shorter = x u y"""
    j = next(i for i, e in enumerate(w) if e < 0)
    if w[j - 2] == 0: return "ZERO", j - 1, (-1,), (0, -1)
    lo = j - 2
    while lo > 0 and w[lo - 1] == w[lo] + 1: lo -= 1
    hi = j
    while hi + 1 < len(w) and w[hi + 1] == w[hi] - 1: hi += 1
    a, b = w[lo], -w[hi]; v = tuple(range(a, -b - 1, -1))
    if (a, b) == (1, 1): return "PEAK", lo, (0,), v
    u = []
    for t in range(a - 1, -b, -1):
        u.append(t)
        if t == a - b: u.append(t)
    return f"RUN({a},{b})", lo, tuple(u), v
def state(st, m):
    """interface state after the first m stones, in coordinates relative to m:
    (row extras > 0, row holes <= 0, column extras, column holes)"""
    R = {r for r, c in st[:m]}; C = {c for r, c in st[:m]}
    f = lambda S: (tuple(sorted(x - m for x in S if x > m)), tuple(sorted(x - m for x in range(1, m + 1) if x not in S)))
    return f(R) + f(C)
