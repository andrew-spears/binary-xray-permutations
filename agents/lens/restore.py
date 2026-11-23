"""After each letter of a word started from G(s0): how many states of G(s) (after 0, 1, 2) or G-(s) (after a negative letter)
are not reached.  python3 restore.py s0 "letters" ["letters" ...]"""
import sys
sys.path.insert(0, "../l1sets"); sys.path.insert(0, "../l2sets")
import l1, neg0
l1.depth = lambda u: len(u[0]) + len(u[1]) + 60
def parts(n, mx=None):
    mx = n if mx is None else mx
    if n == 0: yield (); return
    for a in range(min(n, mx), 0, -1):
        for p in parts(n - a, a): yield (a,) + p
def allst(s): return [(lam, nu) for k in range(s + 1) for lam in parts(k) for nu in parts(s - k)]
_G = {}
def G(s, neg):
    if (s, neg) not in _G:
        _G[(s, neg)] = frozenset(u for u in allst(s) if (neg0.in_Gm(u) if neg else neg0.in_G(u)))
    return _G[(s, neg)]
s0 = int(sys.argv[1])
for word in sys.argv[2:]:
    F = G(s0, False); s = s0; out = []
    for e in map(int, word.split()):
        F = frozenset(v for u in F for k, v in l1.succs(u, e)); s += e
        miss = G(s, e < 0) - F
        out.append(f"{e}:{len(miss)}")
    print(f"s0={s0}  " + " ".join(out))
