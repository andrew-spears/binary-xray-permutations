"""Candidate: fractional rainbow placement (LP) exists.
x_{r,c} >= 0 on cells with c-r in D; row sums 1, column sums 1, each diagonal d in D total 1.
Checks (a) LP feasible on every realizable case (necessity, sanity), (b) LP infeasible on holes.
Usage: python3 lp.py m h"""
import sys, itertools
import numpy as np
from scipy.optimize import linprog
from brute import sumtest, placement, boards

def lp_feasible(R, C, D):
    Dset = set(D)
    cells = [(r, c) for r in R for c in C if c - r in Dset]
    if not cells: return False
    Ri = {r: i for i, r in enumerate(R)}; Ci = {c: i for i, c in enumerate(C)}
    Di = {d: i for i, d in enumerate(sorted(D))}
    m = len(R)
    A = np.zeros((3 * m, len(cells)))
    for j, (r, c) in enumerate(cells):
        A[Ri[r], j] = 1; A[m + Ci[c], j] = 1; A[2 * m + Di[c - r], j] = 1
    res = linprog(np.zeros(len(cells)), A_eq=A, b_eq=np.ones(3 * m), bounds=(0, None), method="highs")
    return res.status == 0

if __name__ == "__main__":
    m, h = int(sys.argv[1]), int(sys.argv[2])
    holes_lp = []; bad_nec = 0; nholes = 0
    for R, C in boards(m, h):
        lo, hi = min(C) - max(R), max(C) - min(R)
        for D in itertools.combinations(range(lo, hi + 1), m):
            if not sumtest(R, C, D): continue
            real = placement(R, C, D) is not None
            f = lp_feasible(R, C, D)
            if real and not f: bad_nec += 1
            if not real:
                nholes += 1
                if f: holes_lp.append((C, D))
    print(m, h, "holes", nholes, "LP-feasible holes", len(holes_lp), "nec-violations", bad_nec)
    for x in holes_lp[:8]: print("  ", x)
