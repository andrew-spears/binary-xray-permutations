"""Candidate: mod-q refined LP. Exists an assignment of each d in D to a row residue class mod q
such that the LP (restricted to cells whose row has the assigned residue), together with
row-class counts, is feasible. q=1 is plain LP. Relaxation of placement => necessary.
Usage: python3 modlp.py m h q   (runs on sum-test-passing holes only, plus LP filter)"""
import sys, itertools
import numpy as np
from scipy.optimize import linprog
from brute import sumtest, placement, boards
from lp import lp_feasible

def lp_cells(R, C, D, allowed):
    Ri = {r: i for i, r in enumerate(R)}; Ci = {c: i for i, c in enumerate(C)}
    Ds = sorted(D); Di = {d: i for i, d in enumerate(Ds)}
    Cset = set(C)
    cells = [(r, r + d) for d in Ds for r in R if r + d in Cset and allowed(r, d)]
    m = len(R)
    if not cells: return False
    A = np.zeros((3 * m, len(cells)))
    for j, (r, c) in enumerate(cells):
        A[Ri[r], j] = 1; A[m + Ci[c], j] = 1; A[2 * m + Di[c - r], j] = 1
    if np.any(A.sum(axis=1) == 0): return False
    res = linprog(np.zeros(len(cells)), A_eq=A, b_eq=np.ones(3 * m), bounds=(0, None), method="highs")
    return res.status == 0

def modlp(R, C, D, q):
    Ds = sorted(D); Cset = set(C)
    choices = [sorted({r % q for r in R if r + d in Cset}) for d in Ds]
    if any(not ch for ch in choices): return False
    rowcnt = {a: sum(1 for r in R if r % q == a) for a in range(q)}
    colcnt = {a: sum(1 for c in C if c % q == a) for a in range(q)}
    for assign in itertools.product(*choices):
        # quick integral class-count check
        rc = {a: 0 for a in range(q)}; cc = {a: 0 for a in range(q)}
        for d, a in zip(Ds, assign): rc[a] += 1; cc[(a + d) % q] += 1
        if rc != rowcnt or cc != colcnt: continue
        amap = dict(zip(Ds, assign))
        if lp_cells(R, C, D, lambda r, d: r % q == amap[d]): return True
    return False

if __name__ == "__main__":
    m, h, q = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    survivors = []; n_lp_holes = 0
    for R, C in boards(m, h):
        lo, hi = min(C) - max(R), max(C) - min(R)
        for D in itertools.combinations(range(lo, hi + 1), m):
            if not sumtest(R, C, D): continue
            if placement(R, C, D) is not None: continue
            if not lp_feasible(R, C, D): continue
            n_lp_holes += 1
            if modlp(R, C, D, q): survivors.append((C, D))
    print(m, h, "q", q, "LP-feasible holes", n_lp_holes, "survive mod-q LP", len(survivors))
    for x in survivors[:6]: print("  ", x)
