"""Reached states by level, letter by letter.  level(u) = max(c, 1 - c), c = class; central = level 1.
python3 levels.py s0 "letters" [show]   start: G(s0), or the empty state if s0 = -1 (then the letters are a whole prefix).   Prints, after each letter, reached/all per level; with show, the
missing states of every level that is more than half reached (at most 40)."""
import sys
sys.path.insert(0, "../l1sets"); sys.path.insert(0, "../l2sets")
import l1, neg0
from collections import Counter
l1.depth = lambda u: len(u[0]) + len(u[1]) + 60
def parts(n, mx=None):
    mx = n if mx is None else mx
    if n == 0: yield (); return
    for a in range(min(n, mx), 0, -1):
        for p in parts(n - a, a): yield (a,) + p
_all = {}
def allst(s):
    if s not in _all: _all[s] = [(lam, nu) for k in range(s + 1) for lam in parts(k) for nu in parts(s - k)]
    return _all[s]
def level(u):
    c = l1.cls(u); return max(c, 1 - c)
s0 = int(sys.argv[1]); show = len(sys.argv) > 3
F = frozenset(u for u in allst(s0) if neg0.in_G(u)) if s0 >= 0 else frozenset([((), ())]); s = max(s0, 0); y = 0
for e in map(int, sys.argv[2].split()):
    F = frozenset(v for u in F for k, v in l1.succs(u, e)); s += e; y = max(0, y + e - 1)
    tot = Counter(level(u) for u in allst(s)); c = Counter(level(u) for u in F)
    print(f"{e:3d} s={s:3d} y={y}  " + "  ".join(f"L{k}: {c[k]}/{tot[k]}" for k in sorted(tot)))
    if show:
        for k in sorted(tot):
            if 2 * c[k] > tot[k] and c[k] < tot[k]:
                miss = sorted(l1.name(u) for u in allst(s) if level(u) == k and u not in F)
                print("      L%d missing:" % k, " ".join(miss[:40]))
