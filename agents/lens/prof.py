"""Profile of the reached set by the two imbalances.  python3 prof.py s1 "letters"
c = c0(lam) + c0(nu) (class), K = c0(lam) - c0(nu).  After each letter: reached / all, per (c, K)."""
import sys
sys.path.insert(0, "../l1sets"); sys.path.insert(0, "../l2sets")
import l1, neg0
from collections import Counter
s1 = int(sys.argv[1]); m = tuple(map(int, sys.argv[2].split()))
l1.depth = lambda u: len(u[0]) + len(u[1]) + 60
def parts(n, mx=None):
    mx = n if mx is None else mx
    if n == 0: yield (); return
    for a in range(min(n, mx), 0, -1):
        for p in parts(n - a, a): yield (a,) + p
def allst(s): return [(lam, nu) for k in range(s + 1) for lam in parts(k) for nu in parts(s - k)]
def key(u): return (l1.c0(u[0]) + l1.c0(u[1]), l1.c0(u[0]) - l1.c0(u[1]))
F = frozenset(u for u in allst(s1) if neg0.in_G(u)); s = s1
for e in m:
    F = frozenset(v for u in F for k, v in l1.succs(u, e)); s += e
    tot = Counter(key(u) for u in allst(s)); c = Counter(key(u) for u in F)
    print(f"{e:3d} s={s:3d}", " ".join(f"{k[0]},{k[1]}:{c[k]}/{tot[k]}" for k in sorted(tot)))
