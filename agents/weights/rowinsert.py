"""The step of the interface machine on pairs of partitions.  ins(lam, j, m) = (lam_1 - 1, .., lam_{j-1} - 1, m, lam_j, ..)
(needs lam_{j-1} - 1 >= m >= lam_j; size changes by m - j + 1): the shape of the Bernstein operator B_m without its sign.
Checks: the e-successors of (lam | mu) are exactly the pairs (ins(lam, j, m) | ins(mu, j', m')) with
(m - j + 1) + (m' - j' + 1) = e.     Usage: python3 rowinsert.py DATA(with transitions) [SMAX]"""
import sys
from load import *
def ins(lam):
    out = []
    for j in range(1, len(lam) + 2):
        hi = lam[j - 2] - 1 if j > 1 else 10 ** 9; lo = lam[j - 1] if j <= len(lam) else 0
        for m in range(lo, min(hi, len(lam) + 40) + 1):
            out.append((m - j + 1, tuple(a for a in tuple(x - 1 for x in lam[:j - 1]) + (m,) + tuple(lam[j - 1:]) if a)))
    return out
D = Data(sys.argv[1]); smax = int(sys.argv[2]) if len(sys.argv) > 2 else 10; n = 0
for s in range(0 if 0 in D.lev else 1, smax + 1):
    L = D.lev[s]
    for e in range(-s, smax - s + 1):
        if s + e < 1: continue
        T = D.T(s, e).tocsr(); L2 = D.lev[s + e]
        for i, (lam, mu) in enumerate(L):
            mine = {(a, b) for da, a in ins(tuple(lam)) for db, b in ins(tuple(mu)) if da + db == e}
            assert mine == {(tuple(L2[k][0]), tuple(L2[k][1])) for k in T[i].indices}, (lam, mu, e); n += 1
print(f"row insertion = machine step for all states of slack <= {smax}, all letters, slacks <= {smax}: {n} cases")
