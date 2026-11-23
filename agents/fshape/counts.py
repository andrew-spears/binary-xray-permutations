"""Residue counts modulo m (the parity counts of card `paritycount` are m = 2).
A stone in row r, column c has sum r + c, so the numbers n(i, j) of stones with (row, column) = (i, j) mod m satisfy
   sum_j n(i, j) = #rows = i,   sum_i n(i, j) = #columns = j,   sum_{i+j = s} n(i, j) = #sums = s   (all mod m).
count_ok(A, B, T, m): such non-negative integers exist (necessary for (A, B) in F(T); proved, it is just counting).
count_frac(A, B, T, m): the same with real numbers (weaker; implied by the plain LP)."""
import numpy as np
from scipy.optimize import milp, linprog, LinearConstraint, Bounds
from core import bits
def system(A, B, T, m):
    M = np.zeros((3 * m, m * m)); b = np.zeros(3 * m)
    for i in range(m):
        for j in range(m): M[i, i * m + j] = M[m + j, i * m + j] = M[2 * m + (i + j) % m, i * m + j] = 1
    for r in bits(A): b[r % m] += 1
    for c in bits(B): b[m + c % m] += 1
    for t in T: b[2 * m + t % m] += 1
    return M, b
def count_ok(A, B, T, m):
    M, b = system(A, B, T, m)
    res = milp(np.zeros(m * m), constraints=[LinearConstraint(M, b, b)], integrality=np.ones(m * m), bounds=Bounds(0, np.inf))
    return res.status == 0
def count_frac(A, B, T, m):
    M, b = system(A, B, T, m)
    return linprog(np.zeros(m * m), A_eq=M, b_eq=b, bounds=(0, None), method="highs").status == 0
def first_bad(A, B, T, mmax):
    for m in range(2, mmax + 1):
        if not count_ok(A, B, T, m): return m
    return None
FAILS = [  # (rule, x, shifted target rows, columns) : states of F(x u) missing from F(x v), found by find_fail.py / peak_short.py
    ("ZERO", (2, 3, 3, 2, 2, 1, 1, 0), (0, -1), (1, 2, 3, 4, 5, 6, 7, 8, 10, 13), (1, 2, 3, 4, 5, 7, 8, 10, 11, 13)),
    ("RUN(2,1)", (4, 3, 2, 1), (2, 1, 0, -1), (1, 2, 3, 4, 6, 7, 8, 9), (1, 2, 3, 4, 7, 8, 9, 10)),
    ("RUN(2,1)", (4, 3, 2, 1, 0), (2, 1, 0, -1), (1, 2, 3, 4, 5, 8, 9, 10, 11), (1, 2, 3, 4, 5, 7, 8, 9, 10)),
    ("PEAK", (3, 4, 3, 3, 2, 1), (1, 0, -1), (1, 2, 3, 4, 5, 6, 9, 10, 13), (1, 2, 3, 4, 5, 6, 9, 10, 13)),
    ("PEAK", (3, 4, 3, 3, 2, 1), (1, 0, -1), (1, 2, 3, 4, 5, 6, 7, 9, 13), (1, 2, 3, 5, 6, 7, 9, 10, 13)),
    ("PEAK", (3, 4, 3, 2, 3, 2, 1), (1, 0, -1), (1, 2, 3, 4, 5, 6, 7, 10, 11, 15), (1, 2, 3, 4, 5, 6, 7, 10, 11, 15))]
if __name__ == "__main__":
    from core import mask, sums
    from collections import Counter
    for name, x, v, A, B in FAILS:
        T = sums(x + v); bad = [m for m in range(2, 11) if not count_ok(mask(A), mask(B), T, m)]
        assert bad == [m for m in range(2, 11) if not count_frac(mask(A), mask(B), T, m)]
        m = bad[0]; f = lambda S: " ".join(f"{i}:{Counter(v % m for v in S)[i]}" for i in range(m))
        print(f"{name} after x = {x}: target rows {A}, columns {B}, sums {T}")
        print(f"    residue counts impossible mod {bad};  mod {m}: rows {f(A)} | columns {f(B)} | sums {f(T)}")
