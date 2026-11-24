"""One-sided signed count.  For D = {d_1 < ... < d_n} (sums mu_k = r_k + c_k, rows and columns numbered 0..n-1):
   S(D) = sum over solutions of sign(k -> c_k)     (the sign of the column order, stones listed by diagonal)
        = coefficient of z^mu in m_rho * a_rho = inverse Kostka number K^{-1}(rho, lambda),  lambda = mu - rho reversed
(m_rho = sum_w z^{w rho} is the permanent of the Vandermonde matrix, a_rho its determinant, a_rho s_lambda = a_{lambda+rho}).
S(D) != 0 would give a solution.   Usage: python3 ik.py n"""
import sys, itertools
from collections import defaultdict
n = int(sys.argv[1])
def sign(p):
    s = 1; seen = [False] * len(p)
    for i in range(len(p)):
        if not seen[i]:
            j = i; L = 0
            while not seen[j]: seen[j] = True; j = p[j]; L += 1
            if L % 2 == 0: s = -s
    return s
S = defaultdict(int); N = defaultdict(int)
for p in itertools.permutations(range(n)):          # p[r] = column of the stone in row r
    sums = [r + p[r] for r in range(n)]
    if len(set(sums)) < n: continue
    order = sorted(range(n), key=lambda r: sums[r]); cols = tuple(p[r] for r in order)
    D = tuple(sorted(sums)); S[D] += sign(cols); N[D] += 1
zero = [D for D in N if S[D] == 0]
print(f"n = {n}: {len(N)} solvable D; one-sided signed count is 0 for {len(zero)}")
for D in sorted(zero)[:8]: print("   D =", D, " solutions", N[D])
vals = sorted(set(S.values())); print("   values of S:", vals[:12], "..." if len(vals) > 12 else "")
