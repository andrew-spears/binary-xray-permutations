"""a(l) = min over prefixes x ending at slack s with last letter l of w(F(x)) / w(all), for one named candidate.
Usage: python3 perletter.py DATA NAME [LMIN LMAX]"""
import sys
from weights import *
D = Data(sys.argv[1], False); name = sys.argv[2]; lo, hi = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (-3, 4)
print(f"bound {D.B}, weights '{name}': a(l) for l = {lo} .. {hi}   [number of minimal sets at l = 0, 1]")
for s in range(1, D.B + 1):
    w = candidates(D.lev[s], s)[name]; w = w / w.sum(); a = mins(D, 1, s, w)
    print(f"{s:3d}  " + " ".join(f"{a[l]:.3f}" if l in a else "  -  " for l in range(lo, hi + 1)) + f"   [{len(D.F.get((s, 0), ([],))[0])}, {len(D.F.get((s, 1), ([],))[0])}]", flush=True)
