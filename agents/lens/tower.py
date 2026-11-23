"""Is the reached set a union of residue cells?  For m = 2, 4, 8: cell of a state = (number of beads in each residue class
mod m, relative to the empty diagram) for both diagrams (= rows used and columns used, counted mod m).
python3 tower.py "letters"  -> after the whole word: states in cells that are full / partly reached / not reached at all,
and the reached states among the partly reached cells."""
import sys
sys.path.insert(0, "../l1sets")
import l1
from collections import Counter
l1.depth = lambda u: len(u[0]) + len(u[1]) + 60
def parts(n, mx=None):
    mx = n if mx is None else mx
    if n == 0: yield (); return
    for a in range(min(n, mx), 0, -1):
        for p in parts(n - a, a): yield (a,) + p
def allst(s): return [(lam, nu) for k in range(s + 1) for lam in parts(k) for nu in parts(s - k)]
def ch(l, m):
    d = len(l) + m; d += (-d) % m; bs = set(l1.beads(l, d)); v = [0] * m
    for k in bs:
        if k >= 0: v[k % m] += 1
    for k in range(-d, 0):
        if k not in bs: v[k % m] -= 1
    return tuple(v)
w = list(map(int, sys.argv[1].split()))
F = frozenset([((), ())]); s = 0
for e in w:
    F = frozenset(v for u in F for k, v in l1.succs(u, e)); s += e
A = allst(s)
print(f"word {w}: slack {s}, reached {len(F)}/{len(A)}")
for m in (1, 2, 4, 8):
    key = lambda u: (ch(u[0], m), ch(u[1], m))
    tot = Counter(key(u) for u in A); c = Counter(key(u) for u in F)
    full = sum(t for k, t in tot.items() if c[k] == t); none = sum(t for k, t in tot.items() if c[k] == 0)
    part = len(A) - full - none; pr = sum(c[k] for k, t in tot.items() if 0 < c[k] < t)
    print(f"  m = {m}: {len(tot)} cells; states in full cells {full}, in empty cells {none}, in mixed cells {part} (of which reached {pr})")
