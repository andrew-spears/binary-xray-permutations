"""The prefix 1^s (sums 3, 5, ..., 2s+1, all odd) against the weights 'binom f f'.
Every stone joins an odd row to an even column or an even row to an odd column, so a state (R, C) in F(1^s) has
#odd(R) = #even(C) and #even(R) = #odd(C) (card paritycount with z = 0).  With R = {lam_i + s - i + 1}, i = 1..s, and
d(lam) = #odd(R) - #even(R) this reads d(lam) + d(mu) = 0: the 2-cores of lam and mu determine each other.
core2 (see weights.py) is a subset of the parity set.
Prints w(F(1^s)) and the weight P(s) of the states with d(lam) + d(mu) = 0, for w = dim = C(s,|lam|) f^lam f^mu.
Usage: python3 ones.py DATA      (compare with the data)
       python3 ones.py - N       (P(s) only, s <= N, by enumerating partitions)"""
import sys
from math import comb
from weights import *
def d(lam, k):
    R = [(lam[i] if i < len(lam) else 0) + k - i for i in range(k)]
    return sum(1 if r % 2 else -1 for r in R)
def partitions(n, m=None):
    if m is None: m = n
    if n == 0: yield (); return
    for a in range(min(n, m), 0, -1):
        for p in partitions(n - a, a): yield (a,) + p
if sys.argv[1] != "-":
    D = Data(sys.argv[1], False)
    for s in range(2, D.B + 1):
        L = D.lev[s]; w = np.array([float(comb(s, sum(a)) * flam(a) * flam(b)) for a, b in L]); w /= w.sum()
        ok = np.array([d(a, s) + d(b, s) == 0 for a, b in L]); M = D.sets(1, s, 1); words = D.F[(s, 1)][1]
        i = words.index((1,) * s); F = M[i].astype(bool); c2 = candidates(L, s)["core2 uniform"] > 0
        print(f"s {s:2d}: w(F(1^s)) = {w[F].sum():.4f}   P(s) = {w[ok].sum():.4f}   a(1) = {(M @ w).min():.4f}   F(1^s) inside / equal to the parity set: "
              f"{bool((F <= ok).all())} / {bool((F == ok).all())}   core2 inside F(1^s): {bool((c2 <= F).all())}   core2 = parity set: {bool((c2 == ok).all())}")
else:
    N = int(sys.argv[2]); g = []
    for n in range(N + 1):
        h = {}
        for lam in partitions(n): k = d(lam, 2 * N); h[k] = h.get(k, 0) + flam(lam)
        g.append(h)
    for s in range(2, N + 1):
        tot = sum(comb(s, a) * sum(g[a].values()) * sum(g[s - a].values()) for a in range(s + 1))
        # d was taken with 2N beads (even); with s beads it is d (s even) or 1 - d (s odd)
        good = sum(comb(s, a) * v * g[s - a].get(-k if s % 2 == 0 else 2 - k, 0) for a in range(s + 1) for k, v in g[a].items())
        print(f"s {s:2d}: P(s) = {good / tot:.4f}")
