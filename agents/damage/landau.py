"""Theorem D (necessary condition) against the exact damage.  Start: G(s0) and All(s0); words over LETTERS appended (valid: next >= prev - 1, containing a 2).
D = fam(s) - step_w(G(s0));  V = states of fam(s) violating (D2) for the suffix w.  Theorem D says V is inside D (checked);  extras = D - V.
python3 landau.py s0 LEN SMAX [minletter [tail]]   (HI=3 in the environment: letters up to 3).  s0 = 0: D is computed from the exact F(w)"""
import sys, os, collections
from oh import *
s0, LEN, SM = map(int, sys.argv[1:4]); LO = int(sys.argv[4]) if len(sys.argv) > 4 else -1; TAIL = len(sys.argv) > 5; setup(SM + 2); HI = int(os.environ.get('HI', 2))
from landau_lib import viol
rows = collections.defaultdict(list); bad = []
def go(w, F, s, y, yh, n2):
    if w and n2 and w[-1] <= 0:
        fam = Gm if w[-1] < 0 else G; D = fam(s) - F; V = frozenset(u for u in fam(s) if viol(u, w))
        if V - D: bad.append((w, sorted(nm(u) for u in V - D)))
        rows[(yh, y, (max(w[-2], -2) if len(w) > 1 else 9) if TAIL else 9, max(w[-1], -2))].append((len(D), len(V), len(D - V), w, sorted(nm(u) for u in D - V)[:8]))
    if len(w) == LEN: return
    for e in range(HI, LO - 1, -1):
        if (w and e < w[-1] - 1) or (not w and e < -1) or s + e > SM or s + e < 1: continue
        go(w + (e,), step(F, e), s + e, max(0, y + e - 1), y, n2 + (e >= 2))
go((), G(s0), s0, 0, 0, 0)
print(f"s0 = {s0}, length <= {LEN}, slack <= {SM}, letters {LO}..{HI};  Theorem D violated (a state of V reached): {len(bad)} {bad[:3]}")
print("(yhat, y, letter before the last [9 = not shown], last [-2 = any letter <= -2]): #words, |D| range, |V| range, #words with D != V, max |D - V|, example")
for key in sorted(rows):
    r = rows[key]; ex = max(r, key=lambda t: t[2])
    print(key, len(r), f"|D| {min(t[0] for t in r)}..{max(t[0] for t in r)}", f"|V| {min(t[1] for t in r)}..{max(t[1] for t in r)}", f"differ {sum(1 for t in r if t[2])}", f"max {ex[2]}",
          "|", (" ".join(map(str, ex[3])) + " : " + " ".join(ex[4])) if ex[2] else "")
