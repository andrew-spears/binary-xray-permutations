"""Classify Farkas certificates for bad top-row cells.
Boards: R={1..m}, C={1..m+h} minus h cols, D passing non-tight sum test and the parity test (as cell/rules.py).
For each bad top-row cell e (peeled board P fails parity test):
  level L   : P fails the sum test (Landau/interval prefix)
  level DEAD: some d of P has no cell at all
  level LP  : plain LP on P infeasible -> min-L1 Farkas certificate classified
  level PAR : plain LP feasible; for every parity choice a classify why LP_a fails:
              deadA (some d has no cell of parity a(d)), cnt (parity count mismatch),
              hall:XY (min-L1 certificate supported on two families X,Y in {R,C,D} => bipartite Hall),
              tri (certificate uses all three families)
Usage: python3 farkas.py m h  -> out_m{m}_h{h}.txt, examples pickled"""
import sys, itertools, time, pickle
from collections import Counter
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
sys.path.insert(0, '/home/claude/agents/cell')
from core import cells_of, lp, passing, peel, passes, sumtest, tight


def certificate(R, C, D, a=None):
    """Min-L1 y=(u_r,v_c,w_d) with u_r+v_c+w_d >= 0 on allowed cells and sum y = -1. None if LP feasible."""
    cells = cells_of(R, C, D, a)
    Rs, Cs, Ds = sorted(R), sorted(C), sorted(D); m = len(R)
    idx = {('R', r): i for i, r in enumerate(Rs)}
    idx.update({('C', c): m + i for i, c in enumerate(Cs)})
    idx.update({('D', d): 2 * m + i for i, d in enumerate(Ds)})
    n = 3 * m
    # variables p (n), q (n); y = p - q
    rows, cols, vals = [], [], []
    for j, (r, c) in enumerate(cells):
        for key in (('R', r), ('C', c), ('D', c - r)):
            i = idx[key]; rows += [j, j]; cols += [i, n + i]; vals += [-1, 1]  # -(y) <= 0
    Aub = coo_matrix((vals, (rows, cols)), shape=(max(len(cells), 1), 2 * n)).tocsr() if cells else None
    Aeq = np.concatenate([np.ones(n), -np.ones(n)])[None, :]
    res = linprog(np.ones(2 * n), A_ub=Aub, b_ub=np.zeros(len(cells)) if cells else None,
                  A_eq=Aeq, b_eq=[-1], bounds=(0, None), method='highs-ds')
    if res.status != 0: return None
    y = res.x[:n] - res.x[n:]
    inv = {i: k for k, i in idx.items()}
    return {inv[i]: y[i] for i in range(n) if abs(y[i]) > 1e-9}


def normalize(y):
    mn = min(abs(v) for v in y.values())
    out = {k: Fraction(v / mn).limit_denominator(60) for k, v in y.items()}
    return out


def kind_of(y):
    """signature: per family R,C,D the sign of its prices (+,-,+-, or absent) and whether all |y| equal."""
    y = normalize(y); sig = []
    for F in 'RCD':
        vs = [v for k, v in y.items() if k[0] == F]
        if not vs: continue
        sg = ('+' if any(v > 0 for v in vs) else '') + ('-' if any(v < 0 for v in vs) else '')
        sig.append(F + sg)
    unit = all(abs(v) == 1 for v in y.values())
    return ' '.join(sig) + ('' if unit else ' W')


def parity_kinds(R, C, D):
    Ds = sorted(D); Cs = set(C)
    nr1 = sum(r % 2 for r in R); nc1 = sum(c % 2 for c in C)
    out = Counter(); tri_ex = None
    for t in itertools.product((0, 1), repeat=len(Ds)):
        a = dict(zip(Ds, t))
        if any(not any(r % 2 == a[d] and r + d in Cs for r in R) for d in Ds):
            out['deadA'] += 1; continue
        if sum(t) != nr1 or sum((ai + d) % 2 for ai, d in zip(t, Ds)) != nc1:
            out['cnt'] += 1; continue
        y = certificate(R, C, D, a)
        assert y is not None, (R, C, D, a)
        k = kind_of(y); out[k] += 1
        if (k.endswith('W') or '+-' in k) and tri_ex is None: tri_ex = (a, normalize(y))
    return out, tri_ex


def run(m, h):
    R = tuple(range(1, m + 1)); r0 = 1
    stat = Counter(); levels = Counter(); combo = Counter(); ex = {}
    for dele in itertools.combinations(range(1, m + h + 1), h):
        C = tuple(c for c in range(1, m + h + 1) if c not in dele)
        lo, hi = min(C) - max(R), max(C) - min(R)
        for D in itertools.combinations(range(lo, hi + 1), m):
            if not sumtest(R, C, D) or tight(R, C, D): continue
            if not passes(R, C, D): continue
            stat['boards'] += 1
            for d in sorted(D):
                if r0 + d not in C: continue
                e = (r0, r0 + d); P = peel(R, C, D, e)
                stat['cells'] += 1
                if passes(*P): continue
                stat['bad'] += 1
                R2, C2, D2 = P
                if not sumtest(*P):
                    levels['L'] += 1; ex.setdefault('L', (C, D, d)); continue
                if any(not any(r + dd in C2 for r in R2) for dd in D2):
                    levels['DEAD'] += 1; ex.setdefault('DEAD', (C, D, d)); continue
                y = certificate(*P)
                if y is not None:
                    k = 'LP-' + kind_of(y); levels[k] += 1
                    ex.setdefault(k, (C, D, d, normalize(y))); continue
                pk, tri_ex = parity_kinds(*P)
                key = 'PAR:' + '+'.join(sorted(pk))
                levels[key] += 1
                ex.setdefault(key, (C, D, d, dict(pk), tri_ex))
    return stat, levels, ex


if __name__ == '__main__':
    m, h = int(sys.argv[1]), int(sys.argv[2])
    t = time.time(); stat, levels, ex = run(m, h)
    with open(f'/home/claude/agents/farkas/out_m{m}_h{h}.txt', 'w') as f:
        f.write(f'm={m} h={h} {dict(stat)} time={time.time()-t:.0f}s\n')
        for k, v in levels.most_common(): f.write(f'  {k}: {v}  ex={ex[k]}\n')
    pickle.dump((stat, levels, ex), open(f'/home/claude/agents/farkas/ex_m{m}_h{h}.pkl', 'wb'))
    print(open(f'/home/claude/agents/farkas/out_m{m}_h{h}.txt').read())
