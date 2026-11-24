"""Route L for (X):  w in G(s0) -2-> v_0 -1-> ... -1-> v_j (all level 2) -0-> p (central) -e-> u.
python3 routeL.py SMAX"""
import sys
from oh import *
SM = int(sys.argv[1]); setup(SM + 2)
level = lambda u: max(cls(u), 1 - cls(u))
L2 = functools.lru_cache(maxsize=None)(lambda s: frozenset(u for u in states(s) if level(u) == 2))
L2s = functools.lru_cache(maxsize=None)(lambda s: frozenset(u for u in L2(s) if not SC(u)))
def show(X, n=14): return " ".join(sorted(nm(u) for u in X)[:n])
print("step 1a: L2*(s) - step_1(L2*(s-1)):")
for s in range(3, SM + 1):
    m = L2s(s) - step(L2s(s - 1), 1)
    if m: print("   ", s, len(m), show(m))
print("step 1b: L2*(s) - step_2(G(s-2)), and L2(s) - step_2(G(s-2)):")
for s in range(2, SM + 1):
    m = L2s(s) - step(G(s - 2), 2); m2 = L2(s) - step(G(s - 2), 2)
    if m or m2: print("   ", s, len(m), show(m), "|", len(m2), show(m2))
P = functools.lru_cache(maxsize=None)(lambda s: step(L2s(s), 0) & Cen(s))
print("step 3: G(s+e) - step_e(P(s))  (G- for e = -1); |Cen - P|:")
for s in range(2, SM):
    out = []
    for e in (1, 0, -1):
        fam = Gm if e < 0 else G; m = fam(s + e) - step(P(s), e)
        out.append(f"e={e}: {len(m)} {show(m, 8)}")
    print("   ", s, len(Cen(s) - P(s)), "; ".join(out))
