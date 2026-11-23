"""Staircase prefixes k, k-1, .., 1 (sums k+2 .. 2k+1) and k, .., 1, 0 (sums k+2 .. 2k+2): F against the plain LP and the
residue counts (agents/fshape/lp.py, counts.py), both necessary.   python3 stair.py K [MMAX]"""
import sys
sys.path.insert(0, "../fshape")
from ones0 import *
from lp import lp
from counts import count_ok
mask = lambda A: sum(1 << a for a in A)
if __name__ == "__main__":
    K = int(sys.argv[1]); MM = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    for k in range(int(sys.argv[3]) if len(sys.argv) > 3 else 2, K + 1):
        for z in (0, 1):
            w = tuple(range(k, 0, -1)) + (0,) * z; n = k + z; s = k * (k + 1) // 2; T = [2 * j + e for j, e in enumerate(w, 1)]
            f = F(w); S = [t for t in states(s) if len(t[0]) <= n and len(t[1]) <= n]
            S = [t for t in S if min(beta(t[0], n)) >= 1 and max(beta(t[0], n)) < T[-1] and max(beta(t[1], n)) < T[-1]]
            L = [t for t in S if lp(mask(beta(t[0], n)), mask(beta(t[1], n)), T)]
            C = [t for t in L if all(count_ok(mask(beta(t[0], n)), mask(beta(t[1], n)), T, m) for m in range(2, MM + 1))]
            assert f <= set(C)
            ex = sorted(nm2(t) for t in set(C) - f)
            print(f"{' '.join(map(str, w))}: |F| = {len(f)}, states with rows, columns < {T[-1]}: {len(S)}, LP-feasible {len(L)}, + residue counts mod 2..{MM}: {len(C)}"
                  + (f"; not reachable: {' '.join(ex[:8])}" if ex else ""), flush=True)
