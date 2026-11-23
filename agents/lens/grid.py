"""Reached / all states per pair of imbalances (a, b) = 2-core charges of the two diagrams, after each letter of a word
started at the empty state.  python3 grid.py "letters" [from]   prints the grid from letter number `from` on (default: last 4).
Rows a, columns b; entry = reached/all, '=' if all reached, '.' if no state exists."""
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
_all = {}
def allst(s):
    if s not in _all: _all[s] = [(lam, nu) for k in range(s + 1) for lam in parts(k) for nu in parts(s - k)]
    return _all[s]
def ab(u): return (l1.c0(u[0]), l1.c0(u[1]))
w = list(map(int, sys.argv[1].split())); frm = int(sys.argv[2]) if len(sys.argv) > 2 else len(w) - 3
F = frozenset([((), ())]); s = 0; y = 0
for i, e in enumerate(w, 1):
    F = frozenset(v for u in F for k, v in l1.succs(u, e)); s += e; y = max(0, y + e - 1)
    if i < frm: continue
    tot = Counter(ab(u) for u in allst(s)); c = Counter(ab(u) for u in F)
    A = sorted({k[0] for k in tot}); B = sorted({k[1] for k in tot})
    print(f"after letter {i} = {e}: slack {s}, y = {y}, reached {len(F)}/{len(allst(s))}")
    print("   a\\b " + "".join(f"{b:>10d}" for b in B))
    for a in A:
        print(f"   {a:3d} " + "".join(f"{('.' if not tot[(a, b)] else '=' + str(tot[(a, b)]) if c[(a, b)] == tot[(a, b)] else str(c[(a, b)]) + '/' + str(tot[(a, b)])):>10s}" for b in B))
