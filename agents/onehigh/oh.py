"""Common code for agents/onehigh: the interface machine (../universal/maya.py) on all pairs (lambda | mu) with slack <= TOP,
the families G(s), G-(s) of ../l1sets and ../l2sets (definitions re-implemented as in ../referee/check.py), bead sets.
State names are lambda|mu.  (M, B) = (M(lambda), M(mu')) as in l1sets/REPORT.md."""
import sys, functools
sys.path.insert(0, "../universal")
from maya import succ
TOP = 16; W = 2 * TOP + 12
def setup(top):
    global TOP, W
    TOP = top; W = 2 * TOP + 12
    for f in (beads, c0, preds, G, Gm, Cen): f.cache_clear()
def parts(n, m=None):
    if n == 0: yield (); return
    for k in range(min(n, m or n), 0, -1):
        for r in parts(n - k, k): yield (k,) + r
@functools.lru_cache(maxsize=None)
def states(s): return tuple((l, m) for i in range(s + 1) for l in parts(i) for m in parts(s - i))
conj = lambda p: tuple(sum(1 for x in p if x > i) for i in range(p[0])) if p else ()
@functools.lru_cache(maxsize=None)
def beads(p): return frozenset((p[i - 1] if i <= len(p) else 0) - i for i in range(1, W + 1))
@functools.lru_cache(maxsize=None)
def c0(p):
    b = beads(p); return sum(1 for k in range(0, W, 2) if k in b) - sum(1 for k in range(-W, 0, 2) if k not in b)
def MB(u): return beads(u[0]), beads(conj(u[1]))
def ab(u): return c0(u[0]), c0(conj(u[1]))
def cls(u): return sum(ab(u))
def slack(u): return sum(u[0]) + sum(u[1])
def central(u): return cls(u) == slack(u) % 2
def SC(u): return u[0] == conj(u[1])
def E0(u):
    M, B = MB(u)
    if any((k ^ 1) not in X for X in (M, B) for k in X): return False
    B2 = {b - 2 for b in B if b - 2 >= -W} | {-W, -W + 1}
    return B2 <= M and len(M - B2) == 2 and (min(M - B2) ^ 1) == max(M - B2)
@functools.lru_cache(maxsize=None)
def preds(u, e):
    """list of (k, t): t e-predecessor of u, M_u = (M_t - 1) u {k}; from the bead formula k in M, k + 1 - e not in B."""
    M, B = MB(u); out = []
    for k in sorted(M):
        if k > -W + 10 and k + 1 - e not in B:
            Mt = sorted((x + 1 for x in M if x != k), reverse=True); Bt = sorted((x - 1 for x in B | {k + 1 - e}), reverse=True)
            out.append((k, (tuple(x for x in (b + i for i, b in enumerate(Mt, 1)) if x > 0), conj(tuple(x for x in (b + i for i, b in enumerate(Bt, 1)) if x > 0)))))
    return tuple(out)
def inA(u):                                                    # A(4m^2+1): central, odd slack >= 5, all 1-predecessors in SC u E0
    s = slack(u); return s % 2 == 1 and s >= 5 and central(u) and all(SC(t) or E0(t) for k, t in preds(u, 1))
def T(u):
    s = slack(u); return s > 0 and ((s % 4 == 0 and (SC(u) or E0(u))) or inA(u))
def inG(u): return central(u) and not T(u)
def inU(u): return slack(u) > 0 and slack(u) % 4 == 0 and all(inA(t) for k, t in preds(u, -1))
def inGm(u): return central(u) and not inU(u)
@functools.lru_cache(maxsize=None)
def G(s): return frozenset(u for u in states(s) if inG(u))
@functools.lru_cache(maxsize=None)
def Gm(s): return frozenset(u for u in states(s) if inGm(u))
@functools.lru_cache(maxsize=None)
def Cen(s): return frozenset(u for u in states(s) if central(u))
def step(F, e): return frozenset(v for t in F for v in succ(t, e))
def run(F, z):
    for e in z: F = step(F, e)
    return F
def nm(u): return "|".join((("".join(map(str, p)) if max(p, default=0) < 10 else ".".join(map(str, p))) or "-") for p in u)
if __name__ == "__main__":                                       # self-test: bead formula for predecessors = maya.succ
    for s in range(9):
        for t in states(s):
            for e in range(-3, 4):
                if s + e >= 0:
                    for v in succ(t, e): assert any(x == t for k, x in preds(v, e)), (t, e, v)
        for u in states(s):
            for e in range(-3, 4):
                if s - e >= 0:
                    for k, t in preds(u, e): assert u in succ(t, e), (u, e, t)
    print("preds = inverse of maya.succ, slack <= 8, letters -3..3;  |G(s)| =", [len(G(s)) for s in range(11)])
