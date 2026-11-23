"""Test peeling rules on boards R={1..m}, C = {1..m+h} minus h columns, all D passing the sum test
(tight Landau prefixes skipped unless --tight), that pass the parity test.
Rules (top row r0 = min R):
 a  largest d usable in the top row (r0+d in C)
 b  smallest d usable in the top row
 c  top-row cell of max weight in the HiGHS zero-objective solution for the lexicographically first passing a
 d  some top-row cell peels (<=> weight 1 at some vertex of some passing restricted LP)
 any  some cell anywhere peels
Iterative rounding (task 2), for EVERY passing a:
 V1  some vertex of LP_a has an entry 1 (exact: some cell e of LP_a with LP_a(board - e) feasible)
 R1  20 random objectives found such a vertex
Usage: python3 rules.py m h [--tight]"""
import sys, itertools, time
import numpy as np
from core import *

rng = np.random.default_rng(0)


def vertex_one_exact(R, C, D, a):
    for (r, c) in cells_of(R, C, D, a):
        R2, C2, D2 = peel(R, C, D, (r, c))
        if not R2 or lp(R2, C2, D2, {d: a[d] for d in D2}) is not None:
            return (r, c)
    return None


def vertex_one_random(R, C, D, a, k=20):
    for _ in range(k):
        s = lp(R, C, D, a, obj=lambda n: rng.standard_normal(n))
        if s and max(s[1]) >= 1 - 1e-9: return True
    return False


def run(m, h, use_tight=False, do_task2=True):
    R = tuple(range(1, m + 1))
    first_fail = {}; cnt = dict(boards=0, passing=0, ties_c=0, V1_fail=0, R1_miss=0, nA=0, all_a_no1=0)
    for dele in itertools.combinations(range(1, m + h + 1), h):
        C = tuple(c for c in range(1, m + h + 1) if c not in dele)
        lo, hi = min(C) - max(R), max(C) - min(R)
        for D in itertools.combinations(range(lo, hi + 1), m):
            if not sumtest(R, C, D): continue
            if not use_tight and tight(R, C, D): continue
            cnt['boards'] += 1
            if not passes(R, C, D): continue
            cnt['passing'] += 1
            r0 = R[0]
            T = [(r0, r0 + d) for d in sorted(D) if r0 + d in C]
            good = {e: passes(*peel(R, C, D, e)) for e in T}
            res = {}
            res['a'] = good[T[-1]] if T else False
            res['b'] = good[T[0]] if T else False
            a0 = passing(R, C, D)[0]
            cells, x = lp(R, C, D, a0)
            w = {e: v for e, v in zip(cells, x) if e[0] == r0}
            mx = max(w.values())
            best = [e for e, v in w.items() if v >= mx - 1e-9]
            if len(best) > 1: cnt['ties_c'] += 1
            if mx < 1 - 1e-9: cnt['c_frac'] = cnt.get('c_frac', 0) + 1
            res['c'] = good[max(best, key=lambda e: e[1])]
            res['d'] = any(good.values())
            res['any'] = res['d'] or any(passes(*peel(R, C, D, e)) for e in cells_of(R, C, D) if e[0] != r0)
            for k, v in res.items():
                if not v and k not in first_fail: first_fail[k] = (C, D, a0, {e: round(v, 3) for e, v in w.items()})
            if do_task2:
                As = passing(R, C, D, first=False)
                no1 = 0
                for a in As:
                    cnt['nA'] += 1
                    if vertex_one_random(R, C, D, a): continue
                    cnt['R1_miss'] += 1
                    if vertex_one_exact(R, C, D, a) is None:
                        cnt['V1_fail'] += 1; no1 += 1
                        first_fail.setdefault('V1', (C, D, a))
                    else:
                        first_fail.setdefault('R1', (C, D, a))
                if no1 == len(As):
                    cnt['all_a_no1'] += 1; first_fail.setdefault('allA', (C, D))
    return cnt, first_fail


if __name__ == "__main__":
    m, h = int(sys.argv[1]), int(sys.argv[2])
    t = time.time()
    cnt, ff = run(m, h, '--tight' in sys.argv, '--no2' not in sys.argv)
    print(f"m={m} h={h} {cnt} time {time.time() - t:.0f}s")
    for k in ['a', 'b', 'c', 'd', 'any', 'V1', 'R1', 'allA']:
        print(f"  {k}: {'no failure' if k not in ff else ff[k]}")
