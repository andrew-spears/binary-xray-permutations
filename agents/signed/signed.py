"""Signed counts of witnesses.  A witness of D = {d_1 < ... < d_n} puts stone k on (row r_k, column c_k), c_k - r_k = d_k.
With rho: k -> r_k and kappa: k -> c_k (both permutations) the three signed counts are
  A = sum sgn(rho)   B = sum sgn(kappa)   P = sum sgn(rho) sgn(kappa) = sum of the signs of the permutation matrices.
A is an inverse Kostka number, P a coefficient of the discriminant prod (z_i - z_j)^2 (see NOTES.md).
Usage: python3 signed.py n      (all valid D of size n)"""
import sys
from itertools import combinations

def sgn(p):
    s, seen = 1, [False] * len(p)
    for i in range(len(p)):
        if not seen[i]:
            j, L = i, 0
            while not seen[j]: seen[j] = True; j = p[j]; L += 1
            if L % 2 == 0: s = -s
    return s

def counts(D):
    n = len(D); tot = A = B = P = 0
    rho = [0] * n; kap = [0] * n; ur = [False] * n; uc = [False] * n
    def rec(k):
        nonlocal tot, A, B, P
        if k == n:
            a, b = sgn(rho), sgn(kap); tot += 1; A += a; B += b; P += a * b; return
        for r in range(n):
            c = r + D[k]
            if not ur[r] and 0 <= c < n and not uc[c]:
                ur[r] = uc[c] = True; rho[k] = r; kap[k] = c; rec(k + 1); ur[r] = uc[c] = False
    rec(0); return tot, A, B, P

def valid(D):
    n = len(D); s = 0
    for k, d in enumerate(D, 1):
        s += d + n - k
        if s < k * (k - 1) // 2: return False
    return s == n * (n - 1) // 2

if __name__ == "__main__":
    n = int(sys.argv[1]); N = zA = zB = zP = zAB = zall = 0; ex = []
    for D in combinations(range(-(n - 1), n), n):
        if not valid(D): continue
        t, A, B, P = counts(D); N += 1
        assert t > 0
        zA += A == 0; zB += B == 0; zP += P == 0; zAB += (A == 0 and B == 0); zall += (A == 0 and B == 0 and P == 0)
        if A == 0 and B == 0 and P == 0 and len(ex) < 3: ex.append((D, t))
    print(f"n={n}: {N} valid D; A=0: {zA}, B=0: {zB}, P=0: {zP}, A=B=0: {zAB}, all three 0: {zall}", ex)
