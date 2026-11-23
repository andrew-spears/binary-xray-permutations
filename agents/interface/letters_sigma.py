"""|e| <= c, family indexed by the slack alone: greatest F(sigma) with  F(sigma+e) inside step_e(F(sigma))  for every
letter e in [-c, c] (order rule e_{k+1} >= e_k - 1 only partly used: the summary forgets the last letter and allows every e >= -1).
Usage: python3 letters_sigma.py c B [-v]"""
import sys
from invariant import analyse
c = int(sys.argv[1]); B = int(sys.argv[2])
def part(mask):
    xs = sorted((j - B + 1 for j in range(2 * B) if mask >> j & 1), reverse=True)
    return tuple(x + i for i, x in enumerate(xs) if x + i > 0)
nodes, I, fails, allst = analyse(B, 0, upd=lambda h, e, s: (1 - c,), cap=c)   # pretend the last letter was 1-c: every e >= -c is legal
print("fails:", len(fails))
for s in sorted(nodes):
    if s[0] == 0: continue
    al = allst(s[0]); miss = sorted((part(r), part(cm)) for r, cm in al - I[s])
    print("sigma", s[0], ":", len(I[s]), "/", len(al), " missing:", miss if len(miss) <= 14 else "...")
    if "-v" in sys.argv: print("     kept:", sorted((part(r), part(cm)) for r, cm in I[s])[:60])
