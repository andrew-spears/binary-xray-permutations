"""Theorem D against the exact reachable set at EVERY prefix (any last letter, any letters, every level).
For every legal prefix x from the empty word (letters LO..HI, length <= LEN, slack <= SM):  A = states of slack s not violating Theorem D for x,  F = F(x)  (F is inside A).
Printed per (young excess y, last letter): #prefixes, #with A != F, total |A|, total |A - F|; then |A - F| by level.
python3 dall.py LEN SM LO HI [MINS]    (MINS: only prefixes of slack >= MINS are counted)"""
import sys, collections
from oh import *
from landau_lib import viol, excess
LEN, SM, LO, HI = map(int, sys.argv[1:5]); MINS = int(sys.argv[5]) if len(sys.argv) > 5 else 0; setup(SM + 2)
lev = lambda u: max(cls(u), 1 - cls(u))
rows = collections.defaultdict(lambda: [0, 0, 0, 0]); bylev = collections.Counter(); totlev = collections.Counter(); ex = {}
def go(w, F, s):
    if w and s >= MINS:
        A = [u for u in states(s) if not viol(u, w)]; assert all(u in A for u in F) if len(F) < 50 else True
        d = [u for u in A if u not in F]; key = (excess(w), w[-1]); r = rows[key]
        r[0] += 1; r[1] += bool(d); r[2] += len(A); r[3] += len(d)
        for u in A: totlev[(key[1] <= 0, lev(u))] += 1
        for u in d: bylev[(key[1] <= 0, lev(u))] += 1
        if d and (key not in ex or len(w) < len(ex[key][0])): ex[key] = (w, sorted(nm(u) for u in d)[:6], len(d), len(A))
    if len(w) == LEN: return
    for e in range(HI, LO - 1, -1):
        if (w and e < w[-1] - 1) or (not w and e < 0) or s + e > SM or s + e < 0: continue
        go(w + (e,), step(F, e), s + e)
go((), frozenset([((), ())]), 0)
print(f"exact F from the empty word, length <= {LEN}, slack {MINS}..{SM}, letters {LO}..{HI}")
print("(y, last letter): #prefixes, #with A != F, sum |A|, sum |A - F|, shortest example (word : |A - F| of |A| : some states)")
for key in sorted(rows):
    r = rows[key]; e = ex.get(key)
    print(key, *r, "|", (" ".join(map(str, e[0])) + f" : {e[2]} of {e[3]} : " + " ".join(e[1])) if e else "")
print("A - F by (last letter <= 0, level): missing / total", {k: f"{bylev[k]}/{totlev[k]}" for k in sorted(totlev)})
