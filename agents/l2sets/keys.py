"""How much of the prefix does F(x) depend on?  Letters in [-C, C], slacks <= S.  For several keys computed from the prefix, the number of keys
and the number of keys with more than one set F(x).  Gamma = set of classes on F(x); run = final non-increasing run.
  python3 keys.py C S"""
import sys
from fx2 import *
from collections import deque, defaultdict
W = 6
seen = {}; q = deque([(1, 0, ())])
while q:
    F, s, w = q.popleft()
    if (F, s, w) in seen: continue
    seen[F, s, w] = 1
    for e in LET:
        if not 0 <= s + e <= S or (w and e < w[-1] - 1): continue
        q.append((step(F, s, e), s + e, (w + (e,))[-W:]))
def run(w, k):
    r = [w[-1]] if w else []
    for a, b in zip(w[-2::-1], w[::-1]):
        if a >= b and len(r) < k: r.append(a)
        else: break
    return tuple(r)
gam = lambda F, s: tuple(sorted(c for c, m in clsmask[s].items() if F & m))
keys = {"slack, last letter": lambda F, s, w: (s, w[-1:]), "slack, Gamma, last letter": lambda F, s, w: (s, gam(F, s), w[-1:]),
        "slack, Gamma, run <= 3": lambda F, s, w: (s, gam(F, s), run(w, 3)), "slack, Gamma, run <= 5": lambda F, s, w: (s, gam(F, s), run(w, 5)),
        "slack, Gamma, last 3 letters": lambda F, s, w: (s, gam(F, s), w[-3:]), "slack, Gamma, last 4 letters": lambda F, s, w: (s, gam(F, s), w[-4:]),
        "slack, Gamma, last 5 letters": lambda F, s, w: (s, gam(F, s), w[-5:]), "slack, last 6 letters": lambda F, s, w: (s, w[-6:])}
print(f"letters [-{C}, {C}], slack <= {S}: {len({(F, s) for F, s, w in seen})} distinct (F, slack)")
for nm, f in keys.items():
    d = defaultdict(set)
    for F, s, w in seen:
        if len(w) >= W or True: d[f(F, s, w)].add(F)
    amb = [k for k, v in d.items() if len(v) > 1]
    print(f"  key ({nm}): {len(d)} keys, {len(amb)} with more than one set (largest number of sets {max(len(v) for v in d.values())}); least slack of an ambiguous key: {min((k[0] for k in amb), default='-')}")
