"""T-splits: S with theta(S^c-word) = transpose of theta(S-word) as multisets of connected components up to translation
and half-turn (then s_theta agree, every term is common).  Usage: python3 tsplit.py n [uni] [v]"""
import sys
from ext import *
def comps(w, tr):
    cells = set()
    for i, x in enumerate(w):
        for j in range(i, i + x): cells.add((j, i) if tr else (i, j))
    out = []; seen = set()
    for c in sorted(cells):
        if c in seen: continue
        st = [c]; seen.add(c); comp = []
        while st:
            a, b = st.pop(); comp.append((a, b))
            for q in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                if q in cells and q not in seen: seen.add(q); st.append(q)
        def norm(cc):
            ma = min(a for a, b in cc); mb = min(b for a, b in cc); return tuple(sorted((a - ma, b - mb) for a, b in cc))
        out.append(min(norm(comp), norm([(-a, -b) for a, b in comp])))
    return sorted(out)
def tsp(e):
    n = len(e); res = []
    for S in range(1, (1 << n) - 1):
        w1, w2 = parts(e, S)
        if min(w1) < 0 or min(w2) < 0 or sum(w1) != sum(w2): continue
        if comps(w1, False) == comps(w2, True): res.append(S)
    return res
if __name__ == "__main__":
    n = int(sys.argv[1]); uni = "uni" in sys.argv; tot = h = 0
    for e in words(n, uni):
        if not any(e) or any(sum(e[:k]) == 0 for k in range(1, n)): continue
        r = tsp(e); tot += 1; h += bool(r)
        if not r and "v" in sys.argv: print("  no T-split:", e)
    print(f"n = {n} {'unimodal' if uni else 'all'}, no tight cut: {tot} words; with a T-split: {h}")
