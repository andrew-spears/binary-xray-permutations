"""H-splits: S with sorted positive S-letters conjugate to sorted positive S^c-letters (state (rho|-), proved odd).
monotone = both part-words weakly increasing (then the placement is explicit).  Usage: python3 mono.py n [uni]"""
import sys
from ext import *
def hs(e):
    n = len(e); anyh = mono = False
    for S in range(1, (1 << n) - 1):
        w1, w2 = parts(e, S)
        if min(w1) < 0 or min(w2) < 0: continue
        r1 = tuple(sorted([x for x in w1 if x > 0], reverse=True)); r2 = tuple(sorted([x for x in w2 if x > 0], reverse=True))
        if conj(r1) == r2:
            anyh = True
            if w1 == sorted(w1) and w2 == sorted(w2): return True, True
    return anyh, False
if __name__ == "__main__":
    n = int(sys.argv[1]); uni = "uni" in sys.argv; tot = h = m = 0
    for e in words(n, uni):
        if not any(e): continue
        if any(sum(e[:k]) == 0 for k in range(1, n)): continue
        a, b = hs(e); tot += 1; h += a; m += b
        if not a and "v" in sys.argv: print("  no H-split:", e)
        if a and not b and "w" in sys.argv: print("  no monotone:", e)
    print(f"n = {n} {'unimodal' if uni else 'all'}, no tight cut: {tot} words; H-split: {h}; monotone H-split: {m}")
