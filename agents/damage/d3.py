"""Is the damage after W 0 the 'local' set: states of G(s) with no backward chain along 0 1 2^a from ANY state / any central state?
python3 d3.py SMAX"""
import sys, itertools
from oh import *
SM = int(sys.argv[1]); setup(SM + 2)
All = lambda s: frozenset(states(s))
def words(a, L):                                   # W in {1,2}* ending in 1 with a letters 2, length <= L
    for n in range(a + 1, L + 1):
        for w in itertools.product((1, 2), repeat=n - 1):
            if w.count(2) == a: yield w + (1,)
for a in (1, 2, 3, 4):
    for s in range(SM - 2, SM + 1):
        base = (2,) * a + (1, 0); s0 = s - sum(base)
        if s0 < 0: continue
        LocAll = G(s) - run(All(s0), base); LocCen = G(s) - run(Cen(s0), base); LocG = G(s) - run(G(s0), base)
        row = []
        for W in words(a, a + 3):
            t0 = s - sum(W)
            if t0 < 0: continue
            D = G(s) - run(G(t0), W + (0,)); DA = G(s) - run(All(t0), W + (0,))
            row.append((W, t0, len(D), len(DA), len(D - LocG), len(LocG - D)))
        print(f"a = {a}, slack {s}: local sets for 2^a 1 0 from All / Central / G: {len(LocAll)} {len(LocCen)} {len(LocG)};  (W, s0, |D|, |D from All|, |D - LocG|, |LocG - D|):")
        print("     ", "; ".join(f"{''.join(map(str, W))} s0={t0}: {d} {da} +{x} -{y}" for W, t0, d, da, x, y in row))
