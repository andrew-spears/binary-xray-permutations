# Size of the class covered by the one-marked-stone theorem (REPORT.md): valid D (n marks in 0..2n-2, Landau) for which some
# stone k has c = 1, i.e. the other n - 1 stones can be matched to the segments [2h, 2h+2], h = 0..n-2.
# Compared with the proved family l1 (every stone within one mark of evenly spaced: |d_k - 2k| <= 1, 0-based).
# Usage: python3 class1.py n
import sys, itertools
n = int(sys.argv[1])
def c1(D, k):
    rest = sorted(set(D) - {D[k]})
    return all(2 * h <= m <= 2 * h + 2 for h, m in enumerate(rest))    # sorted matching; the graph is a forest of paths
tot = cov = l1 = new = notc = 0
def rec(k, lo, s, D):
    global tot, cov, l1, new, notc
    if k == n:
        if s != n * (n - 1): return
        tot += 1
        a = any(c1(D, j) for j in range(n)); b = all(abs(d - 2 * i) <= 1 for i, d in enumerate(D))
        cov += a; l1 += b; new += a and not b; notc += b and not a
        return
    for d in range(lo, 2 * n - 1):
        if s + d < (k + 1) * k: continue
        D.append(d); rec(k + 1, d + 1, s + d, D); D.pop()
rec(0, 0, 0, [])
print(f"n = {n}: valid D {tot}; some stone has c = 1: {cov}; in l1: {l1}; c = 1 and not in l1: {new}; in l1 without c = 1: {notc}")
