# For each arrangement: over all solutions of width <= 3, the smallest possible size of the third chain
# (n minus the largest union of two increasing subsequences = third row of the RSK shape).
import sys, bisect
from collections import Counter
from show import sols
def words(n):
    out = []
    def rec(w, s):
        if len(w) == n:
            if s == 0: out.append(tuple(w))
            return
        lo = w[-1] - 1 if w else 0
        for e in range(max(lo, -s), n - len(w)): rec(w + [e], s + e)
    rec([], 0); return out
def shape(pi):
    rows = []
    for x in pi:
        for r in rows:
            j = bisect.bisect_left(r, x)
            if j == len(r): r.append(x); x = None; break
            r[j], x = x, r[j]
        if x is not None: rows.append([x])
    return [len(r) for r in rows] + [0] * 3
for n in range(4, int(sys.argv[1]) + 1):
    C = Counter(); ex = {}
    for e in words(n):
        m = min(shape(p)[2] for p in sols(list(e)))
        C[m] += 1; ex.setdefault(m, e)
    print(n, dict(sorted(C.items())), "first word needing the largest third chain:", ex[max(C)])
