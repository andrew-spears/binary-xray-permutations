"""Theorem A, the cell: for a valid word e and k with e_i in {0,1,2} (i < k), e_i in {0,-1,-2} (i > k), let
p = #{i < k: e_i = 0} + #{i > k: e_i = -2},  q = #{i < k: e_i = 1} + #{i > k: e_i = -1}.
Then the number of solutions with stone k on the cell (row p+q+1, column p+1) is odd, and likewise for (p+1, p+q+1).
Usage: python3 check_cell.py n     (all valid words of length <= n, brute force)"""
import sys
from ext import words
from check_rows_lib import count
N = int(sys.argv[1]); nw = nk = bad = 0
for n in range(2, N + 1):
    for e in words(n, False):
        hit = False
        for k in range(n):
            if not (all(0 <= x <= 2 for x in e[:k]) and all(-2 <= x <= 0 for x in e[k + 1:])): continue
            p = sum(x == 0 for x in e[:k]) + sum(x == -2 for x in e[k + 1:]); q = sum(x == 1 for x in e[:k]) + sum(x == -1 for x in e[k + 1:])
            D = [2 * (i + 1) + e[i] for i in range(n) if i != k]; hit = True
            for r, c in {(p + q + 1, p + 1), (p + 1, p + q + 1)}:
                nk += 1
                if r + c != 2 * (k + 1) + e[k] or count(D, [i for i in range(1, n + 1) if i != r], [i for i in range(1, n + 1) if i != c]) % 2 == 0: bad += 1; print("BAD", e, k, r, c)
        nw += hit
print(f"n <= {N}: {nw} valid words in the family, {nk} (word, k, cell) tested: number of solutions through the cell even or cell off the diagonal: {bad}")
