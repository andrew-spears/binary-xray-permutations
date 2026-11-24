"""Partition machine = interval orders whose unfinished stones are listed by right endpoint with labels increasing.
State: a partition lam of the slack (labels of the unfinished stones).  Letter e: choose m in {0} or a corner of lam
(lam_m > lam_{m+1}, m = len(lam) allowed), take one box from each of the m largest parts, add a part y = e + m, where
y >= lam_{m+1} is required (y = 0 only with m = len(lam)).
usage: python3 pm.py n"""
import sys
from iv import words
def succ(lam, e):
    t = len(lam); out = []
    for m in range(max(0, -e), t + 1):
        if 0 < m < t and lam[m - 1] == lam[m]: continue
        y = e + m; nxt = lam[m] if m < t else 0
        if y < nxt or (y == 0 and m < t): continue
        new = [p - 1 for p in lam[:m]] + list(lam[m:]) + ([y] if y else [])
        out.append(tuple(sorted((p for p in new if p), reverse=True)))
    return out
def reach(w):
    F = {()}; sizes = []
    for e in w:
        F = {v for u in F for v in succ(u, e)}; sizes.append(len(F))
        if not F: return None
    return sizes
if __name__ == "__main__":
    for n in range(2, int(sys.argv[1]) + 1):
        W = words(n); bad = [w for w in W if reach(w) is None]
        print(f"n = {n}: {len(W)} words; partition machine stuck on {len(bad)}", bad[:3])
