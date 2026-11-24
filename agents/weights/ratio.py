"""Step by step: does a letter e lose weight?  For every minimal reachable set F(x) at (s, l), l in {-1, 0, 1}, and
every legal next letter e in {-1, 0, 1}: r = w(F(x e)) / w(F(x)) (normalised weights at slack s + e and s).
Prints min r and the number of sets with r < 1, per (l, e).   Usage: python3 ratio.py DATA NAME [SMIN]"""
import sys
from essential import *
D = Data(sys.argv[1]); name = sys.argv[2]; smin = int(sys.argv[3]) if len(sys.argv) > 3 else 6
W = [None] + [cands(D.lev[s], s)[name] for s in range(1, D.B + 1)]; W = [None] + [w / w.sum() for w in W[1:]]
res = {}
for s in range(smin, D.B + 1):
    for l in (-1, 0, 1):
        if (s, l) not in D.F: continue
        M = D.sets(1, s, l).astype(float); m = M @ W[s]
        for e in (-1, 0, 1):
            if e < l - 1 or s + e > D.B or s + e < 1: continue
            N = (D.T(s, e).T @ M.T).T > 0; r = (N @ W[s + e]) / m; i = int(np.argmin(r)); k = res.setdefault((l, e), [9, 0, 0, None])
            k[1] += int((r < 1 - 1e-12).sum()); k[2] += len(r)
            if r[i] < k[0]: k[0] = r[i]; k[3] = (s, D.F[(s, l)][1][i], m[i])
for (l, e), (r, bad, n, wit) in sorted(res.items()):
    print(f"last letter {l:2d}, next letter {e:2d}: min ratio {r:.3f}, {bad} of {n} sets lose weight; worst: slack {wit[0]}, x = {' '.join(map(str, wit[1]))}, w(F(x)) = {wit[2]:.3f}")
