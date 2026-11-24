"""Class profile along a middle.  python3 cls.py s1 "m" : after each letter, how many reached states have each class c = c0(lam) + c0(mu)."""
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
F = frozenset(u for u in allst(s1) if neg0.in_G(u)); s = s1
print("start", s, dict(Counter(l1.cls(u) for u in F)))
for e in m:
    F = frozenset(v for u in F for k, v in l1.succs(u, e)); s += e
    tot = Counter(l1.cls(u) for u in allst(s)) if s <= 16 else {}
    c = Counter(l1.cls(u) for u in F)
    print(f"{e:3d} s={s:3d}", " ".join(f"c={k}:{c[k]}" + (f"/{tot[k]}" if tot else "") for k in sorted(c)))
