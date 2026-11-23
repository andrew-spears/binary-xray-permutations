"""Print the greatest slack-only family F(sigma) for |e| <= c in arm/leg (Frobenius) form.
A row set at time k is given by its advanced rows k+1+a (arms a) and its holes k-l (legs l); same for columns.
Usage: python3 letters_F.py c B maxsigma"""
import sys
from invariant import analyse
c = int(sys.argv[1]); B = int(sys.argv[2]); ms = int(sys.argv[3])
def frob(mask):
    arms = tuple(j - B for j in range(B, 2 * B) if mask >> j & 1)
    legs = tuple(B - 1 - j for j in range(B - 1, -1, -1) if not mask >> j & 1)
    return (arms, legs)
nodes, I, fails, allst = analyse(B, 0, upd=lambda h, e, s: (1 - c,), cap=c)
fmt = lambda f: "".join(map(str, f[0])) + "|" + "".join(map(str, f[1]))
for s in sorted(nodes):
    if not 0 < s[0] <= ms: continue
    al = allst(s[0])
    print("sigma", s[0], len(I[s]), "/", len(al))
    print("   kept:   ", " ".join(sorted(fmt(frob(r)) + "," + fmt(frob(cm)) for r, cm in I[s] if r >= cm)))
    print("   missing:", " ".join(sorted(fmt(frob(r)) + "," + fmt(frob(cm)) for r, cm in al - I[s] if r >= cm)))
