"""Fixed-n moves and COUNT.  A move raises one letter and lowers a later one: e_i += 1, e_j -= 1 (i < j), i.e. the
stones on diagonals a < b go to a + 1 and b - 1; it raises the slacks between i and j by 1.  For every valid word w of
length <= n and every such move with a legal result w', record N(w) vs N(w'), grouped by the block w[i..j] that is
changed.  Prints the blocks (up to length 5) with their number of placements, of decreases N(w') < N(w), and the
least ratio.      Usage: python3 moves.py n"""
import sys
from collections import defaultdict
from fractions import Fraction
from countlib import solutions
n = int(sys.argv[1]); sol = solutions(n); N = {w: len(s) for w, s in sol.items()}
tab = defaultdict(lambda: [0, 0, None, None])
for w in N:
    for i in range(len(w)):
        for j in range(i + 1, min(len(w), i + 5)):
            w2 = w[:i] + (w[i] + 1,) + w[i + 1:j] + (w[j] - 1,) + w[j + 1:]
            if w2 not in N: continue
            t = tab[w[i:j + 1]]; t[0] += 1; r = Fraction(N[w2], N[w])
            if r < 1: t[1] += 1
            if t[2] is None or r < t[2]: t[2] = r; t[3] = (w, N[w], w2, N[w2])
good = [(b, t) for b, t in tab.items() if t[1] == 0]; bad = [(b, t) for b, t in tab.items() if t[1]]
print(f"blocks: {len(tab)}; never decreasing: {len(good)}; sometimes decreasing: {len(bad)}")
print("never decreasing (block -> block after the move: placements, least ratio):")
for b, t in sorted(good, key=lambda z: (len(z[0]), -z[1][0]))[:40]:
    b2 = (b[0] + 1,) + b[1:-1] + (b[-1] - 1,); print(f"  {b} -> {b2}: {t[0]:6}  {float(t[2]):.3f}")
print("sometimes decreasing:")
for b, t in sorted(bad, key=lambda z: (len(z[0]), -z[1][0]))[:25]:
    b2 = (b[0] + 1,) + b[1:-1] + (b[-1] - 1,); print(f"  {b} -> {b2}: {t[1]} of {t[0]}  least {float(t[2]):.3f}  e.g. {t[3]}")
