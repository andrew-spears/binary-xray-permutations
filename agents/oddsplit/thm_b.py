"""Theorem B (REPORT2 section 2): a valid unimodal word x y with x in {0,1,2}* and y in {0,-1,-2,-3,-4}*, y not in {0,-1,-2}*.
T = sum over y of max(|e| - 2, 0), P(k) = e_1 + .. + e_k, t = last stone before the first negative letter.
Rule: k1 = first k with P(k) >= T;  k2 = t + 1 if P(k1) = T, else t + 2.   Claim: S = {k1, k2} is an RR-split with
lam = (N1, N3), gam = (N2, N4), N_i = #{k not in S: v_k >= i}, i.e. rows {N3 + 1, N1 + 2} and columns {N4 + 1, N2 + 2}.
Checks the arithmetic for every word of the class with n <= nmax, and for n <= nbrute counts the placements by brute force.
Usage: python3 thm_b.py nmax nbrute"""
import sys
from check_rows_lib import count
def cls(n):
    out = []
    def rec(w, s, down, deep):
        k = len(w)
        if k == n:
            if s == 0 and deep: out.append(tuple(w))
            return
        lo = (w[-1] - 1) if w else 0
        for e in range(max(lo, -s, -4), 3):
            if down and e > 0: continue
            if s + e > 4 * (n - k - 1): continue
            w.append(e); rec(w, s + e, down or e < 0, deep or e < -2); w.pop()
    rec([], 0, False, False); return out
nmax, nbrute = int(sys.argv[1]), int(sys.argv[2])
for n in range(6, nmax + 1):
    W = cls(n); bad = brute = even = 0
    for e in W:
        t = next(i for i in range(n) if e[i] < 0)                 # stones 1..t are x
        T = sum(max(-a - 2, 0) for a in e); P = 0
        for k1 in range(1, n + 1):
            P += e[k1 - 1]
            if P >= T: break
        k2 = t + 1 if P == T else t + 2
        S = (k1, k2)
        u = (e[k1 - 1] + 2 * (k1 - 1), e[k2 - 1] + 2 * (k2 - 2))
        v = [2 * sum(1 for j in S if j > k) - e[k - 1] for k in range(1, n + 1) if k not in S]
        N = [sum(1 for a in v if a >= i) for i in range(1, 5)]
        ok = k1 <= t and k2 <= n and min(v) >= 0 and max(v) <= 4 and u == (N[2] + N[3], N[0] + N[1])
        bad += not ok
        if ok and n <= nbrute:
            D = [2 * k + e[k - 1] for k in range(1, n + 1)]
            R = [N[2] + 1, N[0] + 2]; C = [N[3] + 1, N[1] + 2]
            a = count([D[k - 1] for k in S], R, C)
            b = count([D[k - 1] for k in range(1, n + 1) if k not in S], [r for r in range(1, n + 1) if r not in R], [c for c in range(1, n + 1) if c not in C])
            brute += 1; even += (a % 2 == 0 or b % 2 == 0)
    print(f"n = {n}: {len(W)} words in the class; rule fails: {bad}" + (f"; brute force: {brute} words, even counts: {even}" if n <= nbrute else ""))
