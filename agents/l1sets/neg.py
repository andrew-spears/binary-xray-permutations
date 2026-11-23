"""Does the L1 family G(s) survive deeper negative letters?  Tests G(s - k) inside step_{-k}(G(s)) for k >= 2 (bound S),
and the same for the exact sets after a falling run:  G(s - k(k+1)/2) inside step_{-k} ... step_{-1}(G(s)).
  python3 neg.py S"""
import sys
sys.argv = [sys.argv[0], sys.argv[1]]
import fam
from fam import *
G = gfp()
def stepg(A, s, e):
    out = 0
    for i, t in enumerate(St[s]):
        if A >> i & 1:
            for u in set(Mo.succ(t, e)): out |= 1 << ix[s + e][u]
    return out
for k in range(2, 6):
    bad = [(s, bin(G[s - k] & ~stepg(G[s], s, -k)).count("1")) for s in range(k, S + 1)]
    print(f"single letter -{k} from G(s): missing states of G(s-{k}) by s:", [b for b in bad if b[1]] or "none")
for k in range(2, 6):
    res = []
    for s in range(k * (k + 1) // 2, S + 1):
        A = G[s]; t = s
        for j in range(1, k + 1): A = stepg(A, t, -j); t -= j
        m = bin(G[t] & ~A).count("1")
        if m: res.append((s, t, m))
    print(f"run -1 ... -{k} from G(s): (s, end slack, missing):", res or "none")
