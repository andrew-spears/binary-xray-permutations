"""Print step table for one D: python3 diag.py n d1,d2,...  [order d,d,...]"""
import sys, math, itertools
from steplib import *
n = int(sys.argv[1]); D = [int(v) for v in sys.argv[2].split(',')]
P = poly(D, n); m = n
def lc(S):
    E, C, rem = restrict(P, set(S), m)
    if not rem: return math.log(C.sum()), {}
    return logcap(E, C), {D[k]: int(E[:, i].max()) for i, k in enumerate(rem)}
print('P =', {k: v for k, v in sorted(P.items())})
c0, d0 = lc([])
print('cap(P)=%.6f deg=%s W=%d' % (math.exp(c0), d0, sum(c for e, c in P.items() if all(x == 1 for x in e))))
for d in D:
    k = D.index(d); c1, _ = lc([k]); r = math.exp(c1 - c0)
    print(f' first step d={d}: k={d0[d]} ratio={r:.6f} g={g(d0[d]):.6f} ratio/g={r/g(d0[d]):.6f}')
if len(sys.argv) > 3:
    order = [int(v) for v in sys.argv[3].split(',')]
    S = []; cur, dg = c0, d0
    for d in order:
        S.append(D.index(d)); nc, nd = lc(S); r = math.exp(nc - cur)
        print(f' step d={d}: k={dg[d]} ratio={r:.6f} ratio/g={r/g(dg[d]):.6f}'); cur, dg = nc, nd
