"""Brute-force check of Lemma R: for a nonnegative word w (d_j = 2j + w_j) and every pair of partitions (lam, gam) with
lam + gam = the positive letters of w sorted, the number of bijections R -> C with sums {d_j} is odd,
R = {i + lam_i}, C = {i + gam_i} (parts in increasing order, padded with zeros).  Usage: python3 check_rows.py maxlen maxslack"""
import sys, itertools
from check_rows_lib import count
L, B = int(sys.argv[1]), int(sys.argv[2]); nw = ns = bad = 0
def gen(w, s):
    if w: yield tuple(w)
    if len(w) == L: return
    lo = max(w[-1] - 1, 0) if w else 0
    for e in range(lo, B - s + 1):
        w.append(e); yield from gen(w, s + e); w.pop()
for w in gen([], 0):
    m = len(w); D = [2 * (j + 1) + w[j] for j in range(m)]; pos = sorted([x for x in w if x > 0]); nw += 1; seen = set()
    def rec(i, lam, gam):
        if i == len(pos): yield list(lam), list(gam); return
        lo = lam[-1] if lam else 0; lo2 = gam[-1] if gam else 0
        for a in range(lo, pos[i] + 1):
            if pos[i] - a >= lo2: lam.append(a); gam.append(pos[i] - a); yield from rec(i + 1, lam, gam); lam.pop(); gam.pop()
    for lam, gam in rec(0, [], []):
        lam = [0] * (m - len(lam)) + lam; gam = [0] * (m - len(gam)) + gam
        R = [i + 1 + lam[i] for i in range(m)]; C = [i + 1 + gam[i] for i in range(m)]
        ns += 1
        if count(D, R, C) % 2 == 0: bad += 1
print(f"{nw} words (letters >= 0, length <= {L}, slack <= {B}), {ns} row-type states: even counts {bad}")
