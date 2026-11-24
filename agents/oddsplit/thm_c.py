"""Theorem C (REPORT2 section 3): a valid unimodal word x y with x in {0,1}* and y <= 0 of any depth.
m = ceil(max|y| / 2), c_j = sum over y of max(|e| - 2(m - j), 0) for j = 1..m (c_m = slack).
Rule: S = the ones of x number c_1 < c_2 < .. < c_m.  Claim: S is an RR-split with lam = (N1, N3, ..), gam = (N2, N4, ..),
N_i = #{k not in S: v_k >= i}; the stones of S go to the cells (N_{2m-2j+1} + j, N_{2m-2j+2} + j), j = 1..m, in increasing order.
Checks the arithmetic for every word of the class with n <= nmax; for n <= nbrute counts the placements by brute force.
Usage: python3 thm_c.py nmax nbrute"""
import sys
from check_rows_lib import count
def cls(n):
    out = []
    def rec(w, s, down):
        k = len(w)
        if k == n:
            if s == 0 and any(w): out.append(tuple(w))
            return
        lo = (w[-1] - 1) if w else 0
        for e in range(max(lo, -s), 2):
            if down and e > 0: continue
            w.append(e); rec(w, s + e, down or e < 0); w.pop()
    rec([], 0, False); return out
nmax, nbrute = int(sys.argv[1]), int(sys.argv[2])
for n in range(3, nmax + 1):
    W = cls(n); bad = brute = even = 0; mm = 0
    for e in W:
        m = (max(-a for a in e) + 1) // 2; mm = max(mm, m)
        c = [sum(max(-a - 2 * (m - j), 0) for a in e) for j in range(1, m + 1)]
        ones = [k for k in range(1, n + 1) if e[k - 1] == 1]
        S = [ones[cj - 1] for cj in c]
        u = [e[k - 1] + 2 * (k - 1 - j) for j, k in enumerate(S)]
        v = [2 * sum(1 for j in S if j > k) - e[k - 1] for k in range(1, n + 1) if k not in S]
        N = [sum(1 for a in v if a >= i) for i in range(1, 2 * m + 1)]
        ok = len(set(S)) == m and min(v) >= 0 and max(v) <= 2 * m and u == sorted(u) and u[::-1] == [N[2 * i] + N[2 * i + 1] for i in range(m)]
        bad += not ok
        if ok and n <= nbrute:
            D = [2 * k + e[k - 1] for k in range(1, n + 1)]
            R = [N[2 * (m - j)] + j for j in range(1, m + 1)]; C = [N[2 * (m - j) + 1] + j for j in range(1, m + 1)]
            diag = [r + c_ for r, c_ in zip(R, C)] == [D[k - 1] for k in S]
            a = count([D[k - 1] for k in S], R, C)
            b = count([D[k - 1] for k in range(1, n + 1) if k not in S], [r for r in range(1, n + 1) if r not in R], [c_ for c_ in range(1, n + 1) if c_ not in C])
            brute += 1; even += (a % 2 == 0 or b % 2 == 0 or not diag)
    print(f"n = {n}: {len(W)} words in the class (largest m = {mm}); rule fails: {bad}" + (f"; brute force: {brute} words, even counts: {even}" if n <= nbrute else ""))
