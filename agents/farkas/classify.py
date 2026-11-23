"""Hierarchical obstruction classes for the peeled board P of each bad top-row cell.
 L    : P fails the sum test (Landau / interval prefix)
 H2:XY: bipartite Hall violation between families X,Y (no perfect matching rows-diags 'RD',
        cols-diags 'CD', rows-cols 'RC' using cells of P) -- includes dead line / dead diagonal
 H3   : 0/+-1 three-family certificate (MILP): y in {-1,0,1}, y_r+y_c+y_d >= 0 on cells, sum y <= -1
 Wk   : needs integer prices in [-k,k] (k=2,3,...)  (MILP)
 PAR  : plain LP feasible (parity is the only obstruction)
Usage: python3 classify.py m h [--sq]"""
import sys, itertools, time, pickle
from collections import Counter
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix, csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching
sys.path.insert(0, '/home/claude/agents/cell')
from core import cells_of, lp, peel, passes, sumtest, tight


def hall2(R, C, D, a=None):
    cells = cells_of(R, C, D, a); m = len(R)
    Ri = {r: i for i, r in enumerate(sorted(R))}; Ci = {c: i for i, c in enumerate(sorted(C))}
    Di = {d: i for i, d in enumerate(sorted(D))}
    bad = []
    for name, f, g in (('RD', lambda r, c: Ri[r], lambda r, c: Di[c - r]),
                       ('CD', lambda r, c: Ci[c], lambda r, c: Di[c - r]),
                       ('RC', lambda r, c: Ri[r], lambda r, c: Ci[c])):
        if not cells: bad.append(name); continue
        M = csr_matrix((np.ones(len(cells)), ([f(*e) for e in cells], [g(*e) for e in cells])), shape=(m, m))
        if (maximum_bipartite_matching(M, perm_type='column') >= 0).sum() < m: bad.append(name)
    return bad


def int_cert(R, C, D, K):
    cells = cells_of(R, C, D); m = len(R)
    idx = {('R', r): i for i, r in enumerate(sorted(R))}
    idx.update({('C', c): m + i for i, c in enumerate(sorted(C))})
    idx.update({('D', d): 2 * m + i for i, d in enumerate(sorted(D))})
    n = 3 * m; rows, cols = [], []
    for j, (r, c) in enumerate(cells):
        for key in (('R', r), ('C', c), ('D', c - r)): rows.append(j); cols.append(idx[key])
    cons = [LinearConstraint(np.ones((1, n)), -np.inf, -1)]
    if cells:
        A = coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(len(cells), n)).tocsr()
        cons.append(LinearConstraint(A, 0, np.inf))
    # minimize support-ish: sum |y| via split is heavier; just minimize nothing but prefer small L1 via aux
    res = milp(np.zeros(n), constraints=cons, integrality=np.ones(n), bounds=Bounds(-K, K))
    if res.status != 0: return None
    inv = {i: k for k, i in idx.items()}
    return {inv[i]: int(round(v)) for i, v in enumerate(res.x) if abs(v) > 0.5}


def classify(R, C, D):
    if not sumtest(R, C, D): return 'L', None
    b = hall2(R, C, D)
    if b: return 'H2:' + ','.join(b), None
    for K in (1, 2, 3, 4, 6, 8):
        y = int_cert(R, C, D, K)
        if y is not None: return ('H3' if K == 1 else f'W{K}'), y
    if lp(R, C, D) is not None: return 'PAR', None
    return 'W>8', None


def boards(m, h):
    R = tuple(range(1, m + 1))
    for dele in itertools.combinations(range(1, m + h + 1), h):
        C = tuple(c for c in range(1, m + h + 1) if c not in dele)
        lo, hi = min(C) - max(R), max(C) - min(R)
        for D in itertools.combinations(range(lo, hi + 1), m):
            if not sumtest(R, C, D) or tight(R, C, D): continue
            yield R, C, D


if __name__ == '__main__':
    m, h = int(sys.argv[1]), int(sys.argv[2])
    t = time.time(); stat = Counter(); kinds = Counter(); ex = {}; rows = []
    for R, C, D in boards(m, h):
        if not passes(R, C, D): continue
        stat['boards'] += 1
        for d in sorted(D):
            if 1 + d not in C: continue
            P = peel(R, C, D, (1, 1 + d)); stat['cells'] += 1
            g = passes(*P)
            k, y = classify(*P)
            rows.append((C, D, d, g, k, y))
            if g:
                stat['good'] += 1
                if k != 'PAR' and not k.startswith('PAR'):
                    # good cell but plain LP infeasible?? (cannot happen) -> record
                    pass
                continue
            stat['bad'] += 1; kinds[k] += 1; ex.setdefault(k, (C, D, d, y))
    with open(f'/home/claude/agents/farkas/cls_m{m}_h{h}.txt', 'w') as f:
        f.write(f'm={m} h={h} {dict(stat)} time={time.time()-t:.0f}s\n')
        for k, v in kinds.most_common(): f.write(f'  {k}: {v}  smallest-ex(C,D,d,cert)={ex[k]}\n')
    pickle.dump(rows, open(f'/home/claude/agents/farkas/cls_m{m}_h{h}.pkl', 'wb'))
    print(open(f'/home/claude/agents/farkas/cls_m{m}_h{h}.txt').read())
