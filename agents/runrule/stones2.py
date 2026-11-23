"""Slack 2, letter 0: for each of the five states list the stones available and the state they lead to.
A state after m stones is written by its used rows and columns relative to m (rows 1..m minus the holes, plus the
extras); the stone (m+i, m+j) for the letter 0 has i + j = 2.  Labels: (row diagram | column diagram) as in cone.part.
Usage: python3 stones2.py"""
import sys
sys.path.insert(0, "../interface")
from cone import part
B = 6; base = (1 << B) - 1
def states(s):
    out = set()
    def rec(t, slack, last, depth):
        if slack == s: out.add(t)
        if depth == 0: return
        from count_rule import cstep
        from collections import Counter
        for e in range(-slack if last is not None else 0, B - slack + 1):
            for t2 in cstep(Counter({t: 1}), e, B): rec(t2, slack + e, e, depth - 1)
    rec((base, base), 0, None, 4); return sorted(out)
def show(mask):                                      # bit B+u <-> row (or column) m+1+u
    holes = [u + 1 for u in range(-B + 1, 0) if not mask >> (B + u) & 1]; extras = [u + 1 for u in range(0, B + 1) if mask >> (B + u) & 1]
    return "unused " + ",".join(f"m{h:+d}" if h else "m" for h in holes) + "; used beyond m: " + ",".join(f"m{e:+d}" for e in extras)
lab = lambda t: f"({''.join(map(str, part(t[0], B))) or '-'}|{''.join(map(str, part(t[1], B))) or '-'})"
for t in states(2):
    print(f"state {lab(t)}: rows [{show(t[0])}]  columns [{show(t[1])}]")
    rm, cm = t
    for u in range(-B, B + 1):                       # row position relative to m, bit B+u ; u <= 0 means row m+u... (bit B-1 = row m)
        if rm >> (B + u) & 1: continue
        v = 0 - u
        if v < -B or v > B or cm >> (B + v) & 1: continue
        r2, c2 = rm | 1 << (B + u), cm | 1 << (B + v)
        if not (r2 & 1 and c2 & 1): continue
        t2 = (r2 >> 1, c2 >> 1)
        print(f"     stone (m{u + 1:+d}, m{v + 1:+d})  ->  {lab(t2)}".replace("m+0", "m"))
