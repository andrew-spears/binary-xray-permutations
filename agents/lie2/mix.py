"""Part B, mixtures.  rho_l, rho_s = half sums of the long / short positive roots (rho_l = sum of w_i over long simple
roots, rho_s over short ones).  For a = rho_l + s rho_s and b = rho_l + t rho_s: how many regular dominant
mu <= a + b are not conjugate to a + w b?   (s, t) = (1, 1) is the statement of agents/lie; (1, r) is rho + w rho^vee.
Usage: python3 mix.py TYPE rank [smax]"""
import sys
from rs import *
T, n = sys.argv[1], int(sys.argv[2]); smax = int(sys.argv[3]) if len(sys.argv) > 3 else 3
R = RS(T, n); short = [i for i in R.rng if R.d[i] != 1]
assert R.rho_l == tuple(int(i not in short) for i in R.rng) and R.rho_s == tuple(int(i in short) for i in R.rng)
print(f"{T}{n}: short simple roots {[i + 1 for i in short]}, r = {1 / min(R.d)}")
for s in range(1, smax + 1):
    for t in range(s, smax + 1):
        a = tuple(s if i in short else 1 for i in R.rng); b = tuple(t if i in short else 1 for i in R.rng)
        P = {R.dom(tuple(x + y for x, y in zip(a, v))) for v in R.orbit(b)}
        reg = [m for m in R.below(tuple(x + y for x, y in zip(a, b))) if min(m) >= 1]
        miss = sorted(m for m in reg if m not in P)
        print(f"   s = {s}, t = {t}: regular {len(reg)}, misses {len(miss)}", miss[:6])
