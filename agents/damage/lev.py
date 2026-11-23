"""Same test as landau.py with the start family 'levels <= LV complete' (level = max(c, 1 - c)) instead of G(s0), and the target family levels <= LT:
D = Lev<=LT(s) - step_w(Lev<=LV(s0)),  V = violators of Theorem D in Lev<=LT(s) for the suffix w.  Words: letters LO..2 with a 2, ending in a letter <= 0.
python3 lev.py s0 LEN SMAX LV LT [minletter [all]]   (all: every word, any last letter)"""
import sys, os, collections
from oh import *
from landau_lib import viol
s0, LEN, SM, LV, LT = map(int, sys.argv[1:6]); LO = int(sys.argv[6]) if len(sys.argv) > 6 else -1; ALLW = len(sys.argv) > 7; setup(SM + 2)
lev = lambda u: max(cls(u), 1 - cls(u))
@functools.lru_cache(maxsize=None)
def Lev(s, L): return frozenset(u for u in states(s) if lev(u) <= L)
CUT = int(os.environ.get('CUT', 0)); rows = collections.defaultdict(list); bad = 0
def go(w, F, s, y, yh, n2):
    global bad
    if w and (ALLW or (n2 and w[-1] <= 0)):
        D = Lev(s, LT) - F; V = frozenset(u for u in Lev(s, LT) if viol(u, w)); bad += len(V - D)
        rows[(yh, y, max(w[-1], -2))].append((len(D), len(V), len(D - V), w, sorted(nm(u) for u in D - V)[:10]))
    if len(w) == LEN: return
    for e in range(2, LO - 1, -1):
        if (w and e < w[-1] - 1) or (not w and e < -1) or s + e > SM or s + e < 1: continue
        F2 = step(F, e)
        if CUT and e <= 0: F2 = F2 & Lev(s + e, LV)          # CUT=1: forget everything above level LV at every prefix ending in a letter <= 0
        go(w + (e,), F2, s + e, max(0, y + e - 1), y, n2 + (e >= 2))
go((), Lev(s0, LV), s0, 0, 0, 0)
print(f"s0 = {s0}, length <= {LEN}, slack <= {SM}, letters {LO}..2, start levels <= {LV}, target levels <= {LT}, CUT = {CUT};  states of V reached (must be 0): {bad}")
print("(yhat, y, last [-2 = any letter <= -2]): #words, |D| range, |V| range, #words with D != V, max |D - V|, example")
for key in sorted(rows):
    r = rows[key]; ex = max(r, key=lambda t: t[2])
    print(key, len(r), f"|D| {min(t[0] for t in r)}..{max(t[0] for t in r)}", f"|V| {min(t[1] for t in r)}..{max(t[1] for t in r)}", f"differ {sum(1 for t in r if t[2])}", f"max {ex[2]}",
          "|", (" ".join(map(str, ex[3])) + " : " + " ".join(ex[4])) if ex[2] else "")
