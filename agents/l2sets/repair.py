"""After a letter >= 2, how many gentle letters (<= 1) until F(x) contains G(s) again?
  python3 repair.py LEN SMAX C     all legal prefixes with letters in [-C, C], length <= LEN, slacks <= SMAX
Prints, by t = number of letters since the last letter >= 2, how many prefixes have G(s) inside F(x), and the longest
gentle tails that still fail."""
import sys
sys.path.insert(0, "../l1sets")
import l1
from neg0 import in_G
LEN, SMAX, C = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
l1.depth = lambda u: len(u[0]) + len(u[1]) + 6 + 2 * LEN
def parts(n, m=None):
    m = n if m is None else m
    if n == 0: yield (); return
    for a in range(min(n, m), 0, -1):
        for p in parts(n - a, a): yield (a,) + p
Gs = {s: frozenset(u for k in range(s + 1) for lam in parts(k) for nu in parts(s - k) for u in [(lam, nu)] if in_G(u)) for s in range(SMAX + 1)}
stat = {}; worst = []
def rec(w, s, F, t, h):
    if w and t is not None:
        ok = Gs[s] <= F; st = stat.setdefault(t, [0, 0]); st[0] += 1; st[1] += ok
        if not ok and t >= 3: worst.append((t, h, w, len(Gs[s] - F), len(Gs[s])))
    if len(w) == LEN: return
    for e in range(max((w[-1] - 1) if w else 0, -s, -C), C + 1):
        if s + e > SMAX: break
        F2 = frozenset(v for u in F for k, v in l1.succs(u, e))
        if e >= 2: rec(w + (e,), s + e, F2, 0, h + 1)
        else: rec(w + (e,), s + e, F2, None if t is None else t + 1, h)
rec((), 0, frozenset([((), ())]), None, 0)
for t in sorted(stat): print(f"t = {t}: {stat[t][1]} of {stat[t][0]} prefixes have G(s) inside F(x)")
worst.sort(key=lambda z: (-z[0], z[1]))
for z in worst[:12]: print("  fails: t =", z[0], "high letters", z[1], "word", " ".join(map(str, z[2])), f"missing {z[3]} of {z[4]}")
