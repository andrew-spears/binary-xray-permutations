"""All distinct sets F(x), x an L1 prefix with slacks <= S, by slack; for each: a shortest word, number of zeros E of that word, size,
size of the parity set {|D| <= E} computed from that word, and (show) the states of the parity set that are missing.
  python3 fsets.py S [show]"""
import sys
from fam import *
from collections import deque
seen = {}; q = deque([(1, 0, ())])
while q:
    F, s, w = q.popleft()
    if (F, s) in seen: continue
    seen[F, s] = w
    for e in (1, 0, -1):
        if 0 <= s + e <= S: q.append((step(F, s, e), s + e, w + (e,)))
def parset(s, n, E):
    return sum(1 << i for i, t in enumerate(St[s]) if abs(dval(Mo, t, n + 2 * S + 4)[0]) <= E)
if __name__ == "__main__":
    for s in range(S + 1):
        for (F, s2), w in sorted(seen.items(), key=lambda kv: (len(kv[1]), kv[1])):
            if s2 != s: continue
            E = w.count(0); Pm = parset(s, len(w), E); assert F & ~Pm == 0
            print(f"s {s}: |F| = {bin(F).count('1'):4d} of parity set {bin(Pm).count('1'):4d} (E = {E}, n = {len(w)})  x = {' '.join(map(str, w))}" + (f"   missing: {names(Pm & ~F, s)}" if show else ""))
