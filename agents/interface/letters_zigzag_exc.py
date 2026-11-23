"""Find the witnesses of M from which neither alternating chain works (see letters_zigzag.py). Usage: python3 letters_zigzag_exc.py n"""
import sys
from itertools import product
sys.argv, argv = [sys.argv[0], "2"], sys.argv
import letters_zigzag as Z
n = int(argv[1]); m = n - 2
for e in product((-1, 0, 1), repeat=m):
    s = 0; ok = True
    for x in e:
        s += x
        if s < 0: ok = False; break
    if not ok or s: continue
    ws = Z.witnesses(m, e)
    bad = [w for w in ws if not any(Z.chain(n, [(1, 1)] + [(r + 1, c + 1) for r, c in w] + [(n, n)], f) for f in (0, 1))]
    if bad: print("M =", e, "witnesses", len(ws), "bad", len(bad), "e.g.", bad[0])
