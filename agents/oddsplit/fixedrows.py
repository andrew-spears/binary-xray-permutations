"""Item 4: RR-splits whose stones of S sit in a fixed, word-independent row set R (lam_j = r_j - j).
For every valid word without a tight cut: is there S with |S| = |R| and gam such that sort(u) = lam + gam and conj(sort v) = lam u gam?
Usage: python3 fixedrows.py n pattern     pattern = e.g. 100 (rows = 1 mod 3), 010, 001, 10, 110"""
import sys
from ext import words, parts, conj
n = int(sys.argv[1]); pat = sys.argv[2]; R = [r for r in range(1, n + 1) if pat[(r - 1) % len(pat)] == "1"]; m = len(R)
lam = [R[j] - (j + 1) for j in range(m)]          # increasing
tot = ok = 0; ex = []
for e in words(n, False):
    if not any(e) or any(sum(e[:k]) == 0 for k in range(1, n)): continue
    tot += 1; good = False
    for S in range(1, 1 << n):
        if bin(S).count("1") != m: continue
        w1, w2 = parts(e, S)
        if min(w1) < 0 or (w2 and min(w2) < 0): continue
        u = sorted(w1); gam = [u[j] - lam[j] for j in range(m)]
        if gam[0] < 0 or any(gam[j] > gam[j + 1] for j in range(m - 1)): continue
        N = conj(tuple(sorted([x for x in w2 if x > 0], reverse=True)))
        if tuple(sorted([x for x in lam + gam if x > 0], reverse=True)) == N: good = True; break
    ok += good
    if not good and len(ex) < 3: ex.append(e)
print(f"n = {n}, rows {R}: {tot} words without a tight cut; with an RR-split in these rows: {ok}; first without: {ex}")
