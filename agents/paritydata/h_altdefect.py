"""H6: alternation defect.  For a in A(D): defect = #consecutive pairs (in sorted order) within the same
parity class of d having equal a.  Report max over D of min over a in A(D) of defect, and where it first exceeds 0,1,2."""
import sys
from collections import Counter
from pdata import *
src = sys.argv[2]; NMAX = int(sys.argv[1])
for n in range(1, NMAX + 1):
    W = {D: v[2] for D, v in load_wit(n).items()} if src == 'wit' else load_lp(n)
    h = Counter(); ex = {}
    for D, A in W.items():
        cls = [[k for k, d in enumerate(D) if d % 2 == p] for p in (0, 1)]
        best = 99
        for m in A:
            df = sum(1 for c in cls for i, j in zip(c, c[1:]) if ((m >> i) ^ (m >> j)) & 1 == 0)
            best = min(best, df)
        h[best] += 1; ex.setdefault(best, D)
    print(f'[{src}] n={n} min-defect histogram {sorted(h.items())} examples {sorted(ex.items())[-1:]}', flush=True)
