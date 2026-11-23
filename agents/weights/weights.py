"""Explicit weights for the majority property.  For weights w >= 0 on the states of slack s (total 1) let
    a(l) = min of w(F(x)) over legal prefixes x ending at slack s with last letter l   (all slacks of x <= B),
    b(f) = min of w(A(y)) over suffixes y starting at slack s with first letter f.
If a(l) + b(f) > 1 for all f >= l - 1 then every F(x) meets every compatible A(y) at this cut.  The mirror is
(lam | mu) -> (lam' | mu') (mirror.py), it exchanges F-sets with last letter l and A-sets with first letter -l, so
for w invariant under conjugation b(f) = a(-f) and the test is  a(l) + a(l') > 1  for all l + l' <= 1.
Usage: python3 weights.py DATA [SMIN]      (DATA = output prefix of ./dump B DATA 0)"""
import sys
from math import comb
from load import *
def d2(lam):
    """#odd - #even among the beads lam_i + k - i + 1 (i = 1..k) for an even k >= len(lam): 0 for an empty 2-core,
    2 for the 2-core (1), -2 for (2,1), 4 for (3,2,1), ..."""
    k = len(lam) + len(lam) % 2
    return sum(1 if ((lam[i] if i < len(lam) else 0) + k - i) % 2 else -1 for i in range(k))
def candidates(L, s):
    """dim = C(s,|lam|) f^lam f^mu: number of standard fillings of the pair = dimension of the irreducible representation
             (lam, mu) of the hyperoctahedral group B_s; dim^2 / (2^s s!) is its Plancherel measure
       core2 = both 2-cores empty (s even), one empty and one a single box (s odd)
       box   = lam and mu inside the k x k square, k minimal with k(k+1)/2 >= s (the square of the steepest prefix)
       balanced = | |lam| - |mu| | <= 1"""
    f = np.array([float(flam(a) * flam(b)) for a, b in L]); dim = f * np.array([float(comb(s, sum(a))) for a, b in L])
    bal = np.array([abs(sum(a) - sum(b)) <= 1 for a, b in L]) * 1.0
    c2 = np.array([sorted((d2(a), d2(b))) == [0, 2 * (s % 2)] for a, b in L]) * 1.0
    k = 1
    while k * (k + 1) // 2 < s: k += 1
    box = np.array([all(len(p) <= k and (not p or p[0] <= k) for p in t) for t in L]) * 1.0
    return {"uniform": np.ones(len(L)), "f f": f, "balanced f f": bal * f, "dim": dim, "dim^2": dim ** 2, "core2 uniform": c2,
            "core2 dim": c2 * dim, "core2 dim^2": c2 * dim ** 2, "core2 dim^3": c2 * dim ** 3, "core2 box dim^2": c2 * box * dim ** 2}
def mins(D, d, s, w):
    return {l: float((D.sets(d, s, l) @ w).min()) for l in D.letters(d, s)}
def worst(a, b):
    return min((a[l] + b[f], l, f) for l in a for f in b if f >= l - 1)
if __name__ == "__main__":
    D = Data(sys.argv[1], False); smin = int(sys.argv[2]) if len(sys.argv) > 2 else 1; names = None
    for s in range(smin, D.B + 1):
        C = candidates(D.lev[s], s)
        if names is None:
            names = list(C); print(f"bound {D.B}.  min over cuts of a(l) + b(f), f >= l - 1 (needs > 1), and the (l, f) attaining it")
            print("  s  states " + " ".join(f"{n:>17s}" for n in names))
        row = []
        for n in names:
            w = C[n] / C[n].sum(); v, l, f = worst(mins(D, 1, s, w), mins(D, -1, s, w)); row.append(f"{v:8.3f} ({l:2d},{f:2d})")
        print(f"{s:3d} {len(D.lev[s]):6d} " + " ".join(row), flush=True)
