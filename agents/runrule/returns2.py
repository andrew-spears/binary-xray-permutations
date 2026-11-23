"""Return matrices at slack 2.  An excursion is a word e that starts at slack 2, stays at slack >= 3 strictly inside
and ends at slack 2.  It acts linearly on the symmetric count vectors (alpha, beta, gamma) of slack 2
(alpha = L(11|-) = L(-|11), beta = L(2|-) = L(-|2), gamma = L(1|1)).  In the basis
   U = (0,1,1), V = (1,0,1), W = (1,1,0)    (so (alpha, beta, gamma) = uU + vV + wW, u = (beta+gamma-alpha)/2, ...)
the matrix of e has columns e(U), e(V), e(W) written in (u, v, w).  Prints how many distinct matrices occur for
excursions of length <= N with slacks <= B, whether all entries are nonnegative integers, whether every column lies
in the pentagon of S2 (then every return maps the whole triangle cone into the pentagon), and the first matrices.
Usage: python3 returns2.py B N"""
import sys
from collections import Counter
from fractions import Fraction
sys.path.insert(0, "../interface")
from count_rule import cstep
from cone import part
Bd, N = int(sys.argv[1]), int(sys.argv[2]); B = Bd + 2; base = (1 << B) - 1
A, Bt, G = ((), (1, 1)), ((), (2,)), ((1,), (1,))
cls = lambda t: tuple(sorted((part(t[0], B), part(t[1], B))))
# the five states of slack 2
S2 = set()
C = Counter({(base, base): 1})
for w in ((2,), (1, 1)):
    D = C
    for e in w: D = cstep(D, e, B)
    S2 |= set(D)
assert len(S2) == 5
start = {k: Counter({t: 1 for t in S2 if cls(t) == k}) for k in (A, Bt, G)}
def abg(D):
    d = {}
    for t, c in D.items(): assert d.setdefault(cls(t), c) == c
    return (d.get(A, 0), d.get(Bt, 0), d.get(G, 0))
def uvw(z):
    al, be, ga = z; return (Fraction(be + ga - al, 2), Fraction(al + ga - be, 2), Fraction(al + be - ga, 2))
mats = {}
def rec(e, Ds, s, last):
    if s == 2 and e:
        img = {k: abg(Ds[k]) for k in Ds}                      # images of the class indicators
        col = lambda co: uvw(tuple(sum(co[i] * img[k][j] for i, k in enumerate((A, Bt, G))) for j in range(3)))
        M = tuple(zip(*(col(co) for co in ((0, 1, 1), (1, 0, 1), (1, 1, 0)))))      # rows of the matrix
        if M not in mats or len(e) < len(mats[M]): mats[M] = e
        return
    if len(e) == N: return
    for x in range(1 if not e else max(last - 1, 2 - s), Bd - s + 1):
        rec(e + (x,), {k: cstep(D, x, B) for k, D in Ds.items()}, s + x, x)
rec((), start, 2, None)
neg = [m for m in mats if any(x < 0 or x.denominator != 1 for r in m for x in r)]
print(f"excursions above slack 2, length <= {N}, slacks <= {Bd}: {len(mats)} distinct matrices; with a negative or non-integer entry: {len(neg)}")
for M, e in sorted(mats.items(), key=lambda z: (len(z[1]), z[1]))[:12]:
    print(f"   e = {str(e):28} M = {[[int(x) if x.denominator == 1 else str(x) for x in r] for r in M]}")
# columns in the pentagon of S2?   u <= 2v + w  (beta <= 2 alpha)   and   v <= 3u + 4w  (gamma <= 4 beta)
out = [(mats[M], j) for M in mats for j in range(3) if M[0][j] > 2 * M[1][j] + M[2][j] or M[1][j] > 3 * M[0][j] + 4 * M[2][j]]
tight = [(mats[M], j) for M in mats for j in range(3) if M[0][j] == 2 * M[1][j] + M[2][j] or M[1][j] == 3 * M[0][j] + 4 * M[2][j]]
print(f"columns (images of U, V, W) outside the pentagon u <= 2v + w, v <= 3u + 4w: {len(out)} of {3 * len(mats)} {out[:3]}; on its boundary: {len(tight)} {sorted(tight, key=lambda z: len(z[0]))[:3]}")
for M in neg[:8]: print(f"   NEGATIVE: e = {mats[M]}  M = {[[str(x) for x in r] for r in M]}")
