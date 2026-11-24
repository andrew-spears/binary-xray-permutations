"""The cut that suffices.  A legal word (e_{j+1} >= e_j - 1, first letter >= 0, last letter <= 0) that is not all 0
has a first letter <= 0; if it is not e_1 the letter before it is 1 and it is 0.  Cut between that 1 and 0: the prefix
ends in 1, the mirrored suffix ends in 0.  So for a mirror-symmetric w it is enough that
        a(0) + a(1) > 1,     a(l) = min over prefixes x ending at slack s with last letter l of w(F(x)) / w(all).
Prints a(0), a(1), a(0) + a(1) per slack for mirror-symmetric explicit candidates.
The candidates are those of weights.py (see candidates() there).
Usage: python3 essential.py DATA [SMIN]"""
import sys
from weights import *
cands = candidates
if __name__ == "__main__":
    D = Data(sys.argv[1], False); smin = int(sys.argv[2]) if len(sys.argv) > 2 else 2; names = None
    for s in range(smin, D.B + 1):
        C = cands(D.lev[s], s); M0 = D.sets(1, s, 0); M1 = D.sets(1, s, 1)
        if names is None:
            names = list(C); print(f"bound {D.B}: a(0)  a(1)  a(0)+a(1)\n  s " + " ".join(f"{n:>20s}" for n in names))
        row = []
        for n in names:
            w = C[n] / C[n].sum(); a0 = (M0 @ w).min(); a1 = (M1 @ w).min(); row.append(f"{a0:.3f} {a1:.3f} {a0 + a1:6.3f} ")
        print(f"{s:3d} " + " ".join(row), flush=True)
