"""Fractional tests for a state (A, B) against a set of sums T.
lp(A,B,T): plain LP (rows, columns, sums each carry weight 1).
plp(A,B,T,m): exists an assignment of each sum to a residue class (row mod m) so that the LP restricted to cells
              whose row has the assigned residue is feasible (m = 2: the 'parity test' of card `parity`)."""
import numpy as np
from itertools import product
from scipy.optimize import linprog
from core import bits
def lp(A, B, T, allowed=None):
    R, C = bits(A), bits(B); T = list(T); ti = {t: i for i, t in enumerate(T)}
    cells = [(r, c) for r in R for c in C if r + c in ti and (allowed is None or allowed(r, c))]
    if not cells: return not T
    n = len(T); M = np.zeros((3 * n, len(cells)))
    ri = {r: i for i, r in enumerate(R)}; ci = {c: i for i, c in enumerate(C)}
    for j, (r, c) in enumerate(cells): M[ri[r], j] = M[n + ci[c], j] = M[2 * n + ti[r + c], j] = 1
    res = linprog(np.zeros(len(cells)), A_eq=M, b_eq=np.ones(3 * n), bounds=(0, 1), method="highs")
    return res.status == 0
def plp(A, B, T, m=2):
    T = list(T)
    Rc = [sum(1 for r in bits(A) if r % m == i) for i in range(m)]
    Cc = [sum(1 for c in bits(B) if c % m == i) for i in range(m)]
    def rec(j, asg, rc, cc):
        if j == len(T):
            return lp(A, B, T, lambda r, c: asg[r + c] == r % m)
        for i in range(m):
            ci_ = (T[j] - i) % m
            if rc[i] and cc[ci_]:
                rc[i] -= 1; cc[ci_] -= 1; asg[T[j]] = i
                if rec(j + 1, asg, rc, cc): return True
                rc[i] += 1; cc[ci_] += 1
        return False
    return rec(0, {}, Rc, Cc)
