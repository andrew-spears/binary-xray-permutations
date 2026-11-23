"""States lying in every reachable set F(x) with last letter 0 or 1 at slack s (then the delta weight on such a state
has a(0) = a(1) = 1).  Prints their number, how many have core2, the number of states c in every F(x) with last letter 1
whose mirror c* is in every F with last letter 0 (c is then in every A(y) with first letter 0: enough for the cut 1|0), and a
few states with the fewest corners.
Usage: python3 universal.py DATA [SMIN]"""
import sys
from weights import *
D = Data(sys.argv[1], False); smin = int(sys.argv[2]) if len(sys.argv) > 2 else 1
nm = lambda t: "|".join("".join(map(lambda a: str(a) if a < 10 else f"({a})", p)) or "-" for p in t)
for s in range(smin, D.B + 1):
    U0 = D.sets(1, s, 0).all(0); U1 = D.sets(1, s, 1).all(0); U = U0 & U1; L = D.lev[s]
    two = U1 & U0[D.sigma(s, lambda t: (conj(t[0]), conj(t[1])))]; c2 = candidates(L, s)["core2 uniform"] > 0
    u = sorted((L[i] for i in np.flatnonzero(U)), key=lambda t: (len(set(t[0])) + len(set(t[1])), t))
    print(f"s {s:2d}: {int(U.sum())} of {len(L)} states in every F, {int((U & c2).sum())} with core2; {int(two.sum())} good for 1|0:  " + "  ".join(nm(t) for t in u[:8]))
