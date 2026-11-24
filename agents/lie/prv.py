"""Lie-theoretic form of the conjecture, and the same question for the other classical root systems.
Type A_{n-1}: D solvable  <=>  lambda + rho = w rho + w' rho for some permutations w, w', where rho = (n-1, ..., 0) and
lambda = (s_n, ..., s_1) is the score sequence read downwards; D valid <=> lambda dominant and lambda <= rho in the
root order (= majorisation).  So the conjecture reads: every REGULAR dominant weight mu <= 2 rho is W-conjugate to
rho + w rho (a 'generalised PRV weight' of V(rho) (x) V(rho)).
This script asks the same for types B, C, D: list regular dominant mu <= 2 rho (mu - 2 rho in the root lattice) that are
NOT conjugate to any rho + w rho.          Usage: python3 prv.py TYPE n      (TYPE in A B C D)"""
import sys, itertools
from fractions import Fraction as Fr
def setup(T, n):
    if T == 'A': rho = [Fr(n - 1 - i) for i in range(n)]
    if T == 'B': rho = [Fr(2 * (n - i) - 1, 2) for i in range(n)]
    if T == 'C': rho = [Fr(n - i) for i in range(n)]
    if T == 'D': rho = [Fr(n - 1 - i) for i in range(n)]
    return rho
def dom(T, v):
    """dominant representative of the orbit of v"""
    if T == 'A': return tuple(sorted(v, reverse=True))
    a = sorted((abs(x) for x in v), reverse=True)
    if T == 'D' and all(x != 0 for x in v) and sum(1 for x in v if x < 0) % 2: a[-1] = -a[-1]
    return tuple(a)
def group(T, n):
    for p in itertools.permutations(range(n)):
        if T == 'A': yield p, (1,) * n; continue
        for sg in itertools.product((1, -1), repeat=n):
            if T == 'D' and sg.count(-1) % 2: continue
            yield p, sg
def below(T, n, rho):
    """all dominant mu with 2 rho - mu a nonnegative integer combination of simple roots"""
    # 2rho - mu = sum a_i alpha_i.  In coordinates x = 2rho - mu: partial sums c_k = x_1 + ... + x_k.
    # A: c_k >= 0 integer, c_n = 0.  B: c_k >= 0 integer.  C: c_k >= 0 integer, c_n even.
    # D: a_i = c_i (i <= n-2), a_{n-1} - a_n = -x_n ... handled by direct solve below.
    out = []
    top = [2 * r for r in rho]
    def rec(i, mu, c):
        if i == n:
            x = [top[j] - mu[j] for j in range(n)]
            if T == 'A' and c != 0: return
            if T == 'C' and c % 2: return
            if T == 'D':
                # alpha_{n-1} = e_{n-1} - e_n, alpha_n = e_{n-1} + e_n : a_{n-1} = (c_{n-1} - x_n)/2... solve
                cn1 = sum(x[:n - 1]); an = (cn1 + x[n - 1]) / 2; an1 = (cn1 - x[n - 1]) / 2
                if an < 0 or an1 < 0 or an.denominator != 1 or an1.denominator != 1: return
            out.append(tuple(mu)); return
        hi = top[i] if i == 0 else min(mu[i - 1], top[i] + c)
        lo = 0 if T in 'BC' or (T == 'D' and i < n - 1) else None
        if T == 'A': lo = 0
        if T == 'D' and i == n - 1: lo = -mu[i - 1]
        m = hi
        while m >= lo:
            c2 = c + top[i] - m
            if c2 >= 0: rec(i + 1, mu + [m], c2)
            m -= 1
    rec(0, [], Fr(0))
    return out
def regular(T, mu):
    n = len(mu)
    if any(mu[i] == mu[j] for i in range(n) for j in range(i)): return False
    if T == 'A': return True
    if any(mu[i] == -mu[j] for i in range(n) for j in range(i)): return False
    if T in 'BC' and any(x == 0 for x in mu): return False
    return True
if __name__ == "__main__":
    T, n = sys.argv[1], int(sys.argv[2]); rho = setup(T, n)
    prv = {}
    for p, sg in group(T, n):
        v = dom(T, [rho[i] + sg[i] * rho[p[i]] for i in range(n)]); prv[v] = prv.get(v, 0) + 1
    B = [m for m in below(T, n, rho) if dom(T, m) == m]
    R = [m for m in B if regular(T, m)]
    assert all(v in set(B) for v in prv), "a PRV weight is not below 2 rho?"
    miss = [m for m in R if m not in prv]
    f = lambda m: "(" + ",".join(str(x) for x in m) + ")"
    print(f"type {T}{n if T != 'A' else n - 1}: dominant weights <= 2rho: {len(B)}, of the form rho + w rho: {len(prv)}, regular: {len(R)}, regular and not of that form: {len(miss)}")
    for m in miss[:6]: print("   mu =", f(m), "  mu - rho =", f([a - b for a, b in zip(m, rho)]))
