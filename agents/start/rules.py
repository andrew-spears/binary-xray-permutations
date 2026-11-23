"""Item 2: test explicit parity rules a(d) on all Landau D, n = 1..N. Reports first failure
(smallest n, first D in lex order) per rule: 'cnt' = row/col parity counts wrong, 'lp' = restricted LP infeasible.
Usage: python3 rules.py N"""
import sys
import numpy as np
from common import landau_D, lp, counts_ok


def ranked(D):
    return list(enumerate(sorted(D), start=1))

def lin(al, be, ga):
    def f(n, D):
        return {d: (al * k + be * d + ga) % 2 for k, d in ranked(D)}
    f.__name__ = f"lin(k*{al}+d*{be}+{ga})"; return f

def rank_in_class(off, addd):
    # rank of d among elements of D with the same parity as d
    def f(n, D):
        a = {}
        for p in (0, 1):
            for j, d in enumerate([d for d in sorted(D) if d % 2 == p], start=1):
                a[d] = (j + off + addd * d) % 2
        return a
    f.__name__ = f"rank_in_parity_class+{off}{'+d' if addd else ''}"; return f

def abs_order(off):
    def f(n, D):
        Ds = sorted(D, key=lambda d: (abs(d), d))
        return {d: (j + off) % 2 for j, d in enumerate(Ds)}
    f.__name__ = f"alt_by_|d|+{off}"; return f

def pairs(off):
    def f(n, D):
        return {d: ((k + off) // 2) % 2 for k, d in ranked(D)}
    f.__name__ = f"floor((k+{off})/2)"; return f

def natural_row(rnd):
    # the "natural" row of d: centre the diagonal; d occupies rows max(1,1-d)..min(n,n-d)
    def f(n, D):
        a = {}
        for k, d in ranked(D):
            lo, hi = max(1, 1 - d), min(n, n - d)
            r = (lo + hi + rnd) // 2
            a[d] = r % 2
        return a
    f.__name__ = f"mid-row-of-diagonal(round{'+' if rnd else '-'})"; return f

def score_row(off):
    # row = rank k (diagonal d_k in row k, i.e. the 'sorted' identity witness): a = k parity is lin; use s_k-based row
    def f(n, D):
        return {d: ((d + n - k) // 2 + off) % 2 for k, d in ranked(D)}
    f.__name__ = f"floor(s_k/2)+{off}"; return f

def lp_bary(n, D):
    ok, (cells, x) = lp(n, D, None, ret=True)
    rho = {}
    for (r, c), v in zip(cells, x):
        rho.setdefault(c - r, 0.0); rho[c - r] += r * v
    return {d: int(np.floor(rho[d] + 0.5)) % 2 for d in D}
lp_bary.__name__ = "LP-vertex barycentric row, rounded"

def lp_argmax(n, D):
    ok, (cells, x) = lp(n, D, None, ret=True)
    best = {}
    for (r, c), v in zip(cells, x):
        d = c - r
        if d not in best or v > best[d][0] + 1e-9: best[d] = (v, r)
    return {d: best[d][1] % 2 for d in D}
lp_argmax.__name__ = "LP-vertex argmax row"

RULES = ([lin(a, b, g) for a in (0, 1) for b in (0, 1) for g in (0, 1)]
         + [rank_in_class(o, e) for o in (0, 1) for e in (0, 1)]
         + [abs_order(0), abs_order(1)] + [pairs(o) for o in range(4)]
         + [natural_row(0), natural_row(1), score_row(0), score_row(1), lp_bary, lp_argmax])

if __name__ == "__main__":
    N = int(sys.argv[1])
    fams = {n: landau_D(n) for n in range(1, N + 1)}
    VAR = []
    for rule in RULES:
        for c0 in (0, 1):
            def g(n, D, rule=rule, c0=c0):
                return {d: (v + c0 + n) % 2 for d, v in rule(n, D).items()}
            g.__name__ = rule.__name__ + f" +n+{c0}"; VAR.append(g)
    for rule in VAR:
        res = None
        for n in range(1, N + 1):
            for D in fams[n]:
                a = rule(n, D)
                if not counts_ok(n, D, a): res = (n, D, "cnt"); break
                if not lp(n, D, a): res = (n, D, "lp"); break
            if res: break
        print(f"{rule.__name__:45s}", f"first failure n={res[0]} D={list(res[1])} ({res[2]})" if res else f"PASSES all n<={N}", flush=True)
