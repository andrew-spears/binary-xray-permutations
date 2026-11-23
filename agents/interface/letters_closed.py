"""Recursive class K of witnesses for L_1 words, built only by direct sums and the zigzag chain:
K(0) = {one stone}; K(uv) = direct sums when u, v both return to height 0; K(+ M -) = results of the alternating
chain (row-first or column-first) started from corner stones + a member of K(M).
Reports whether K(w) is non-empty for every word, and how the chain fails when it fails.
Usage: python3 letters_closed.py nmax"""
import sys
from itertools import product
from functools import lru_cache
def chain(n, cells, first):
    pos = list(cells); byrow = {p[0]: k for k, p in enumerate(pos)}; bycol = {p[1]: k for k, p in enumerate(pos)}
    cur = 0; mode = first; seen = set()
    while True:
        if (cur, mode) in seen: return None, "cycle"
        seen.add((cur, mode)); r, c = pos[cur]
        if mode == 0:
            if r == n: return None, "row n"
            o = byrow[r + 1]; pos[cur] = (r + 1, c); pos[o] = (r, pos[o][1]); byrow[r + 1] = cur; byrow[r] = o
        else:
            if c == n: return None, "col n"
            o = bycol[c + 1]; pos[cur] = (r, c + 1); pos[o] = (pos[o][0], c); bycol[c + 1] = cur; bycol[c] = o
        if o == n - 1: return tuple(pos), "ok"
        cur = o; mode ^= 1
stats = {}
@lru_cache(None)
def K(w):
    n = len(w)
    if n == 0: return frozenset([()])
    s = 0
    for i, x in enumerate(w):
        s += x
        if s == 0: break
    i += 1
    if i < n:
        return frozenset(a + tuple((r + i, c + i) for r, c in b) for a in K(w[:i]) for b in K(w[i:]))
    if n == 1: return frozenset([((1, 1),)])
    out = set()
    for a in K(w[1:-1]):
        for f in (0, 1):
            res, why = chain(n, ((1, 1),) + tuple((r + 1, c + 1) for r, c in a) + ((n, n),), f)
            stats[why] = stats.get(why, 0) + 1
            if res: out.add(res)
    return frozenset(out)
if __name__ == "__main__":
    for n in range(1, int(sys.argv[1]) + 1):
        tot = empty = 0; mn = None; first = None
        for e in product((-1, 0, 1), repeat=n):
            s = 0; ok = True
            for x in e:
                s += x
                if s < 0: ok = False; break
            if not ok or s: continue
            tot += 1; k = len(K(e))
            if k == 0:
                empty += 1
                if first is None: first = e
            mn = k if mn is None else min(mn, k)
        print(f"n={n}: {tot} words, K empty for {empty}, smallest |K| = {mn}, first empty: {first}, chain outcomes so far {stats}", flush=True)
