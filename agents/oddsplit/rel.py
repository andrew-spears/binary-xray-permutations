"""Relative splits ('mixed splits'): w = x m y, x = a prefix with letters <= 1, y = a suffix with letters >= -1.
A relative split = row/column sets for four parts X (stones of x), S, T (S u T = stones of m), Y with
  (R_X, C_X) a state of G(slack x)                      [Theorem 0 of ../l2sets: x reaches it]
  half-turn of (R_Y, C_Y) a state of G(slack y)         [the same for -reverse(y)]
  S and T chains: multiset {r_i + c_i - 2i} = multiset {d_i - 2i}, i = index inside the part   [Lemma R': odd count]
Usage: python3 rel.py "1 1 1 2 1 0 -1 -2 -3" [kmax] [all]   prints the relative splits with |S| <= kmax (default 1; S may be empty)
By default x and y are the LONGEST gentle ends, so an empty output only says there is no split with those ends; with `all` every
shorter pair of ends (p' <= p, r' <= r; the stones given up go to m) is searched too.
For |S| >= 2 the rows and columns of S are printed as sets: the chain condition gives an odd number of placements of S on them,
not the pairing in sorted order."""
import sys, itertools, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "l1sets"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "l2sets"))
import l1
from neg0 import in_G
def partitions(s, maxlen, maxpart):
    def rec(s, k, mx):
        if s == 0: yield (); return
        if k == 0: return
        for a in range(min(s, mx), 0, -1):
            for r in rec(s - a, k - 1, a): yield (a,) + r
    yield from rec(s, maxlen, maxpart)
def conj(p): return tuple(sum(1 for x in p if x > i) for i in range(p[0])) if p else ()
def states(s, p, n):
    """states (lam|gam) of slack s for a prefix of p stones on the n-board, in G(s); as (rows, cols, lam, gam)"""
    out = []
    for a in range(s + 1):
        for lam in partitions(a, p, n - p):
            for gam in partitions(s - a, p, n - p):
                if in_G((lam, conj(gam))):
                    R = tuple(sorted((lam[i] if i < len(lam) else 0) + p - i for i in range(p)))
                    C = tuple(sorted((gam[i] if i < len(gam) else 0) + p - i for i in range(p)))
                    out.append((R, C, lam, gam))
    return out
def cuts(e):
    n = len(e); p = 0
    while p < n and e[p] <= 1: p += 1
    r = 0
    while r < n - p and e[n - 1 - r] >= -1: r += 1
    return p, r
def chain(D, R, C):
    return sorted(d - 2 * i for i, d in enumerate(D)) == [r + c - 2 * i for i, (r, c) in enumerate(zip(R, C))]
def relsplits(e, kmax=1, p=None, r=None, first=False):
    n = len(e); d = [2 * (k + 1) + e[k] for k in range(n)]
    pp, rr = cuts(e)
    if p is None: p = pp
    if r is None: r = rr
    sx = sum(e[:p]); sy = -sum(e[n - r:]); q = n - p - r
    SX = states(sx, p, n) if p else [((), (), (), ())]
    SY = [(tuple(sorted(n + 1 - a for a in R)), tuple(sorted(n + 1 - a for a in C)), lam, gam) for R, C, lam, gam in states(sy, r, n)] if r else [((), (), (), ())]
    out = []
    for RX, CX, lx, gx in SX:
        for RY, CY, ly, gy in SY:
            if set(RX) & set(RY) or set(CX) & set(CY): continue
            Rm = [a for a in range(1, n + 1) if a not in RX and a not in RY]
            Cm = [a for a in range(1, n + 1) if a not in CX and a not in CY]
            for k in range(0, kmax + 1):
                for S in itertools.combinations(range(p, p + q), k):
                    DS = [d[i] for i in S]; DT = [d[i] for i in range(p, p + q) if i not in S]
                    us = sorted(x - 2 * i for i, x in enumerate(DS))
                    for RS in itertools.combinations(Rm, k):
                        CS = tuple(us[i] + 2 * i - RS[i] for i in range(k))
                        if any(c not in Cm for c in CS) or any(CS[i] >= CS[i + 1] for i in range(k - 1)): continue
                        RT = [a for a in Rm if a not in RS]; CT = [a for a in Cm if a not in CS]
                        if chain(DT, RT, CT):
                            out.append((tuple(i + 1 for i in S), RS, CS, (lx, gx), (ly, gy)))
                            if first: return out
    return out
if __name__ == "__main__":
    e = tuple(int(a) for a in sys.argv[1].split()); rest = sys.argv[2:]; every = "all" in rest
    kmax = next((int(a) for a in rest if a != "all"), 1)
    p, r = cuts(e)
    for p1, r1 in ([(a, b) for a in range(p, -1, -1) for b in range(r, -1, -1)] if every else [(p, r)]):
        print("x =", e[:p1], " m =", e[p1:len(e) - r1], " y =", e[len(e) - r1:])
        for S, RS, CS, tx, ty in relsplits(e, kmax, p1, r1):
            where = ("cell " + str((RS[0], CS[0]))) if len(S) == 1 else ("rows " + str(RS) + " columns " + str(CS))
            print("S =", S, where, " state of x (lam|gam):", tx, " state of -rev(y):", ty)
