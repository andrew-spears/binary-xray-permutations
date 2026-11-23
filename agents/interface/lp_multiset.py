"""Repeated diagonals on the full square board: is 'a fractional placement exists' (LP: doubly
stochastic X with total weight m_x on each anti-diagonal r'+c = x) the same as 'a permutation
exists'?  Also compares with plain majorization.  Usage: python3 lp_multiset.py nmax"""
import sys, itertools
import numpy as np
from scipy.optimize import linprog
from collections import Counter
from nonstrict import sums, cands
def lp_ok(b, n):
    cnt = Counter(b)
    cells = [(r, c) for r in range(1, n+1) for c in range(1, n+1) if (r + c) in cnt]
    A = []; rhs = []
    for r in range(1, n+1): A.append([1.0 if cell[0] == r else 0.0 for cell in cells]); rhs.append(1.0)
    for c in range(1, n+1): A.append([1.0 if cell[1] == c else 0.0 for cell in cells]); rhs.append(1.0)
    for x, m in cnt.items(): A.append([1.0 if cell[0] + cell[1] == x else 0.0 for cell in cells]); rhs.append(float(m))
    res = linprog(np.zeros(len(cells)), A_eq=np.array(A), b_eq=np.array(rhs), bounds=(0, 1), method="highs")
    return res.status == 0
for n in (range(2, int(sys.argv[1]) + 1) if __name__ == "__main__" else []):
    S = sums(n); gap = []; nlp = 0; nbad = 0
    for b in cands(n):
        if b in S: continue
        nbad += 1
        if lp_ok(b, n): gap.append(b)
    print(n, "majorized multisets with no permutation:", nbad, "| of these LP-feasible:", len(gap), gap[:3], flush=True)
