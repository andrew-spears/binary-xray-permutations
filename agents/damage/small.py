"""Exact reachable sets from the empty word against Theorem D, by the slack of the previous cut.
For every legal prefix x (letters LO..2, slack <= SMAX, length <= LEN) ending in a letter <= 0:  D = (Lev<=2(s) - T(s)) - F(x),  V = violators of Theorem D for x.
A cut = a prefix ending in a letter <= 0 (or the empty word); pc = slack at the cut before the last block (block = letters >= 1 then one letter <= 0).
Printed: for each pc, the number of prefixes, how many have D != V, and the largest D - V.   python3 small.py LEN SMAX [minletter [DEPTH]]   (DEPTH > 0: group by the least slack among the last DEPTH cuts before the prefix, the empty word included)"""
import sys, collections
from oh import *
from landau_lib import viol, inN
LEN, SM = map(int, sys.argv[1:3]); LO = int(sys.argv[3]) if len(sys.argv) > 3 else -1; DEPTH = int(sys.argv[4]) if len(sys.argv) > 4 else 0; setup(SM + 2)
lev = lambda u: max(cls(u), 1 - cls(u))
@functools.lru_cache(maxsize=None)
def Fam(s): return frozenset(u for u in states(s) if lev(u) <= 2 and not T(u))
rows = collections.defaultdict(list); bad = 0
def go(w, F, s, pc, cut, hist=(0,)):
    global bad
    if w and w[-1] <= 0:
        assert all(viol(u, w) == inN(u, w) for u in states(s)) and not any(inN(u, w) for u in F)      # Corollary N on ALL states of slack s
        D = Fam(s) - F; V = frozenset(u for u in Fam(s) if viol(u, w)); bad += len(V - D)
        rows[min(hist[:-1][-DEPTH:] or (0,)) if DEPTH else pc].append((len(D - V), w, sorted(nm(u) for u in D - V)[:8]))
    if len(w) == LEN: return
    for e in range(2, LO - 1, -1):
        if (w and e < w[-1] - 1) or (not w and e < 0) or s + e > SM or s + e < 0: continue
        go(w + (e,), step(F, e), s + e, cut if e <= 0 else pc, s + e if e <= 0 else cut, hist + (s + e,) if e <= 0 else hist)
go((), frozenset([((), ())]), 0, 0, 0)
print(f"exact F from the empty word, length <= {LEN}, slack <= {SM}, letters {LO}..2;  states of V reached (must be 0): {bad}")
print("slack of previous cut: #prefixes ending in a letter <= 0, #with D != V, max |D - V|, example")
for pc in sorted(rows):
    r = rows[pc]; ex = max(r, key=lambda t: (t[0], -len(t[1])))
    print(pc, len(r), sum(1 for t in r if t[0]), ex[0], "|", (" ".join(map(str, ex[1])) + " : " + " ".join(ex[2])) if ex[0] else "")
