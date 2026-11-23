"""Print the greatest inductive family I(sigma, last letter) for |e| <= c as pairs of partitions, and the missing pairs.
Usage: python3 letters_show.py c B"""
import sys
from invariant import analyse
c = int(sys.argv[1]); B = int(sys.argv[2])
def part(mask):
    xs = sorted((j - B + 1 for j in range(2 * B) if mask >> j & 1), reverse=True)
    return tuple(x + i for i, x in enumerate(xs) if x + i > 0)
nodes, I, fails, allst = analyse(B, 1, cap=c)
for s in sorted(nodes):
    if s[0] == 0: continue
    al = allst(s[0]); miss = sorted((part(r), part(cm)) for r, cm in al - I[s])
    print(s, len(I[s]), "/", len(al), " missing:", miss if len(miss) <= 40 else len(miss))
