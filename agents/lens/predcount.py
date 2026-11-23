"""min over states of level l of the number of e-predecessors of level l - 1 (even e) / of the same level (odd e).
python3 predcount.py S   (all states of slack <= S)"""
import sys
sys.path.insert(0, "../l1sets")
import l1
l1.depth = lambda u: len(u[0]) + len(u[1]) + 30
def parts(n, mx=None):
    mx = n if mx is None else mx
    if n == 0: yield (); return
    for a in range(min(n, mx), 0, -1):
        for p in parts(n - a, a): yield (a,) + p
def level(u):
    c = l1.cls(u); return max(c, 1 - c)
S = int(sys.argv[1]); mn = {}
for s in range(S + 1):
    for k in range(s + 1):
        for lam in parts(k):
            for nu in parts(s - k):
                u = (lam, nu); l = level(u)
                for e in (-4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6):
                    if s - e < 0: continue
                    P = [level(t) for _, t in l1.preds(u, e)]
                    for tgt, nm in ((l - 1, "down"), (l, "same"), (l + 1, "up")):
                        key = (e, l, nm); mn[key] = min(mn.get(key, 99), sum(1 for x in P if x == tgt))
for e in (-4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6):
    print(f"e = {e:2d}: " + "  ".join(f"L{l}: down>={mn[(e, l, 'down')]} same>={mn[(e, l, 'same')]}" for l in (1, 2, 3, 4) if (e, l, 'down') in mn))
