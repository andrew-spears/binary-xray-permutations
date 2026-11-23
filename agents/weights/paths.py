"""Path-counting weights (need the transitions: ./dump B DATA 1), tested at the cuts with last letter 0 and 1.
  N(t)      = number of (prefix x with all letters >= 1, legal; placement of x) ending in t
  N N*      = N(t) N(t*), t* the mirror (conjugate both diagrams): a 'number of solutions through t' for words that
              rise with letters >= 1 and fall with letters <= -1
  u, u u*   = left Perron vector of the letter 0 at slack s (the limit of placements of x 0 0 0 ...), and u(t) u(t*)
  reach     = number of minimal reachable sets at (s, 0) and (s, 1) containing t
Usage: python3 paths.py DATA"""
import sys
from weights import *
D = Data(sys.argv[1]); B = D.B
N = {(0, None): np.ones(1)}; tot = [np.zeros(len(L)) for L in D.lev]; todo = [(0, None)]
for s in range(B):
    for l in [None] + list(range(1, B + 1)):
        if (s, l) not in N: continue
        for e in range(1 if l is None else max(1, l - 1), B - s + 1):
            v = D.T(s, e).T @ N[(s, l)]; N[(s + e, e)] = N.get((s + e, e), 0) + v; tot[s + e] += v
print(f"bound {B}: a(0), a(1) and their sum (needs > 1) for mirror-symmetric path weights")
names = ["N N*", "sqrt(N N*)", "u u*", "sqrt(u u*)", "reach", "reach^4"]
print("  s " + " ".join(f"{n:>20s}" for n in names))
for s in range(2, B + 1):
    p = D.sigma(s, lambda t: (conj(t[0]), conj(t[1]))); n = tot[s]; T0 = D.T(s, 0).T; u = np.ones(len(n))
    for _ in range(400): u = T0 @ u; u /= u.sum()
    M0 = D.sets(1, s, 0); M1 = D.sets(1, s, 1); r = (M0.sum(0) + M1.sum(0)) / (len(M0) + len(M1)); r = r * r[p]
    C = {"N N*": n * n[p], "sqrt(N N*)": np.sqrt(n * n[p]), "u u*": u * u[p], "sqrt(u u*)": np.sqrt(u * u[p]), "reach": r, "reach^4": r ** 4}
    row = []
    for nm in names:
        w = C[nm] / C[nm].sum(); a0 = (M0 @ w).min(); a1 = (M1 @ w).min(); row.append(f"{a0:.3f} {a1:.3f} {a0 + a1:6.3f} ")
    print(f"{s:3d} " + " ".join(row), flush=True)
