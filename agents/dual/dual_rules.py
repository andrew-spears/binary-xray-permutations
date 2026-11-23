"""Test LP-duality-inspired peeling rules (top row r0 = 1) on all boards R={1..m}, C = {1..m+h} minus h
columns, D passing the non-tight sum test and the parity test. "good" = peeled board passes.
For tie-breaking we report STRICT failures (some cell in the rule's argmax set is bad) and
LENIENT failures (every argmax cell is bad).

Rules (all computed from the full board only):
 V1any   exists passing a and top-row e with LP_a & x_e = 1 feasible (=> peel e passes with a restricted)
 V1all   for every passing a such a top-row e exists
 landau  argmax over top-row e of min sum-test slack of the peeled board
 tightK  find the tightest upper-side prefix k (involves rows 1..k); take the usable top-row d among the
         k largest diagonals: tightK_lo = smallest such d, tightK_hi = largest
 rc*     min/max objective sum r*d*x over LP_a (best a); among top-row cells with reduced cost 0 pick:
         rc_wmax / rc_wmin = extremal diagonal potential w_d; rc_x = max primal weight
Usage: python3 dual_rules.py m h"""
import sys, itertools, time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
sys.path.insert(0, '/home/claude/agents/cell')
from core import cells_of, lp, passing, peel, passes, sumtest, tight

EPS = 1e-7


def slacks(R, C, D):
    m = len(R); Rs, Cs, Ds = sorted(R), sorted(C), sorted(D)
    lo = [sum(Ds[:k]) - (sum(Cs[:k]) - sum(Rs[-k:])) for k in range(1, m)]
    hi = [(sum(Cs[-k:]) - sum(Rs[:k])) - sum(Ds[-k:]) for k in range(1, m)]
    return lo, hi


def lp_dual(R, C, D, a, sign):
    cells = cells_of(R, C, D, a); m = len(R)
    Ri = {r: i for i, r in enumerate(sorted(R))}; Ci = {c: i for i, c in enumerate(sorted(C))}
    Di = {d: i for i, d in enumerate(sorted(D))}
    rows, cols = [], []
    for j, (r, c) in enumerate(cells):
        rows += [Ri[r], m + Ci[c], 2 * m + Di[c - r]]; cols += [j, j, j]
    A = coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(3 * m, len(cells))).tocsr()
    cost = np.array([sign * r * (c - r) for r, c in cells], float)
    res = linprog(cost, A_eq=A, b_eq=np.ones(3 * m), bounds=(0, None), method="highs")
    y = res.eqlin.marginals
    u = {r: y[Ri[r]] for r in R}; v = {c: y[m + Ci[c]] for c in C}; w = {d: y[2 * m + Di[d]] for d in D}
    rc = {(r, c): cst - u[r] - v[c] - w[c - r] for (r, c), cst in zip(cells, cost)}
    return res.fun, dict(zip(cells, res.x)), rc, w


def judge(sel, good):
    if not sel: return 'strict', 'lenient'
    s = 'strict' if any(not good[e] for e in sel) else None
    l = 'lenient' if all(not good[e] for e in sel) else None
    return s, l


def run(m, h):
    R = tuple(range(1, m + 1)); r0 = 1
    cnt = {}; ff = {}
    def fail(k, kind, ex):
        cnt[k + ':' + kind] = cnt.get(k + ':' + kind, 0) + 1
        ff.setdefault(k + ':' + kind, ex)
    nb = 0
    for dele in itertools.combinations(range(1, m + h + 1), h):
        C = tuple(c for c in range(1, m + h + 1) if c not in dele)
        lo_, hi_ = min(C) - max(R), max(C) - min(R)
        for D in itertools.combinations(range(lo_, hi_ + 1), m):
            if not sumtest(R, C, D) or tight(R, C, D): continue
            if not passes(R, C, D): continue
            nb += 1
            T = [(r0, r0 + d) for d in sorted(D) if r0 + d in C]
            good = {e: passes(*peel(R, C, D, e)) for e in T}
            ex = (C, D, {e[1] - 1: good[e] for e in T})
            As = passing(R, C, D, first=False)
            # V1
            v1 = []
            for a in As:
                ok = [e for e in T if a[e[1] - 1] == 1 and
                      (m == 1 or lp(*peel(R, C, D, e), {d: a[d] for d in D if d != e[1] - 1}) is not None)]
                v1.append(ok)
            if not any(v1): fail('V1any', 'none', ex)
            if not all(v1): fail('V1all', 'none', ex)
            # Landau argmax on peeled board
            phi = {}
            for e in T:
                R2, C2, D2 = peel(R, C, D, e)
                if len(R2) <= 1: phi[e] = 1e9; continue
                if not sumtest(R2, C2, D2): phi[e] = -1; continue
                l, hh = slacks(R2, C2, D2); phi[e] = min(l + hh)
            mx = max(phi.values())
            for kind in judge([e for e in T if phi[e] == mx], good):
                if kind: fail('landau', kind, ex + (phi,))
            # tightest upper prefix
            l, hh = slacks(R, C, D)
            k = 1 + int(np.argmin(hh)); top = set(sorted(D)[-k:])
            sel = [e for e in T if e[1] - 1 in top]
            for name, pick in (('tightK_lo', sel[:1]), ('tightK_hi', sel[-1:])):
                for kind in judge(pick, good):
                    if kind: fail(name, kind, ex + (k,))
            # dual rules
            for sign, sn in ((1, 'min'), (-1, 'max')):
                best = None
                for a in As:
                    f, x, rc, w = lp_dual(R, C, D, a, sign)
                    if best is None or f < best[0] - EPS: best = (f, x, rc, w)
                f, x, rc, w = best
                Z = [e for e in T if e in rc and abs(rc[e]) < EPS]
                for name, key in (('wmax', lambda e: w[e[1] - 1]), ('wmin', lambda e: -w[e[1] - 1]),
                                  ('x', lambda e: x[e])):
                    if Z:
                        top_v = max(key(e) for e in Z)
                        pick = [e for e in Z if key(e) >= top_v - EPS]
                    else: pick = []
                    for kind in judge(pick, good):
                        if kind: fail(f'rc_{sn}_{name}', kind, ex)
    return nb, cnt, ff


if __name__ == "__main__":
    m, h = int(sys.argv[1]), int(sys.argv[2])
    t = time.time(); nb, cnt, ff = run(m, h)
    print(f"m={m} h={h} boards={nb} time={time.time() - t:.0f}s")
    for k in sorted(cnt): print(f"  {k}: {cnt[k]}  first={ff[k]}")
