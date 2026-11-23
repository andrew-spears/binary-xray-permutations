"""L_1 words (letters -1,0,+1, any order, prefix sums >= 0, total 0).  Restricted witnesses:
A: + stones only at (k+1,k) or (k,k+1), - stones only at (k,k-1) or (k-1,k), zeros free.
B: every stone within distance m of its home cell (k,k) in both coordinates.
Usage: python3 letters_ansatz.py nmax"""
import sys
from itertools import product
def solve(n, e, opts):
    def rec(k, R, C):
        if k > n: return True
        for r, c in opts(k, e[k - 1]):
            if 1 <= r <= n and 1 <= c <= n and not (R >> r & 1) and not (C >> c & 1) and rec(k + 1, R | 1 << r, C | 1 << c): return True
        return False
    return rec(1, 0, 0)
def optsA(n):
    def f(k, e):
        if e == 1: return [(k + 1, k), (k, k + 1)]
        if e == -1: return [(k, k - 1), (k - 1, k)]
        return [(k - m, k + m) for m in range(-n, n + 1)]
    return f
def optsB(n, m):
    return lambda k, e: [(k + u, k + e - u) for u in range(-m, m + 1) if abs(e - u) <= m]
for n in range(2, int(sys.argv[1]) + 1):
    tot = 0; failA = []; needB = {}
    for e in product((-1, 0, 1), repeat=n):
        s = 0; ok = True
        for x in e:
            s += x
            if s < 0: ok = False; break
        if not ok or s: continue
        tot += 1
        if not solve(n, e, optsA(n)): failA.append(e)
        m = 0
        while not solve(n, e, optsB(n, m)): m += 1
        needB[m] = needB.get(m, 0) + 1
    print(n, "words", tot, "| ansatz A fails:", len(failA), failA[:2], "| smallest displacement needed:", dict(sorted(needB.items())), flush=True)
