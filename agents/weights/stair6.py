"""The LP-feasible, unreachable states of the staircases k = 6: which pass the residue counts mod 2..MM?   python3 stair6.py [MM]"""
import sys
sys.path.insert(0, "../fshape")
from stair import *
MM = int(sys.argv[1]) if len(sys.argv) > 1 else 9
for z in (0, 1):
    k = 6; w = tuple(range(k, 0, -1)) + (0,) * z; n = k + z; s = 21; T = [2 * j + e for j, e in enumerate(w, 1)]
    f = F(w); S = [t for t in states(s) if len(t[0]) <= n and len(t[1]) <= n and max(beta(t[0], n)) < T[-1] and max(beta(t[1], n)) < T[-1]]
    ex = [t for t in S if t not in f and lp(mask(beta(t[0], n)), mask(beta(t[1], n)), T)]
    bad = {}
    for t in ex:
        m = next((m for m in range(2, MM + 1) if not count_ok(mask(beta(t[0], n)), mask(beta(t[1], n)), T, m)), None); bad[m] = bad.get(m, 0) + 1
    print(" ".join(map(str, w)), f": {len(ex)} LP-feasible states not in F; first modulus whose residue counts fail (None = all pass up to {MM}):", bad)
