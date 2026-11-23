"""Bad top-row cells only. Classes for the peeled board P (first match):
 L      sum test fails (Landau/interval prefix)
 H2:XY  bipartite Hall violation in family pair XY (RD rows-diags, CD, RC)
 H3p    0/+-1 certificate where each family has a single sign (pure): "negative lines/diagonals N,
        positive P, every cell meeting k members of N meets >= k members of P, |P| < |N|"
 H3m    0/+-1 certificate needing mixed signs inside a family
 Wk     integer prices in [-k,k] needed
 PAR    plain LP feasible
Certificates are minimum-support. Also records whether L cases have a +-1 certificate.
Usage: python3 cls2.py m h [--sq]  (--sq: square start boards, h=0, all tight allowed? no: non-tight)"""
import sys, itertools, time, pickle
from collections import Counter
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix, hstack
sys.path.insert(0, '/home/claude/agents/cell')
from core import cells_of, lp, peel, passes, sumtest, tight
from classify import hall2, boards


def cert(R, C, D, K=1, signs=None, a=None):
    """min-support integer y in [-K,K], y_r+y_c+y_d>=0 on cells, sum y <= -1.
    signs: dict family->+1/-1 forcing sign. y = p - q, p,q in [0,K], binary support z."""
    cells = cells_of(R, C, D, a); m = len(R)
    keys = [('R', r) for r in sorted(R)] + [('C', c) for c in sorted(C)] + [('D', d) for d in sorted(D)]
    idx = {k: i for i, k in enumerate(keys)}; n = len(keys)
    rows, cols = [], []
    for j, (r, c) in enumerate(cells):
        for key in (('R', r), ('C', c), ('D', c - r)): rows.append(j); cols.append(idx[key])
    # vars: p(n) q(n) zp(n) zq(n)
    N = 4 * n
    I = np.eye(n)
    cons = [LinearConstraint(np.concatenate([np.ones(n), -np.ones(n), np.zeros(2 * n)])[None, :], -np.inf, -1),
            LinearConstraint(np.hstack([I, 0 * I, -K * I, 0 * I]), -np.inf, 0),
            LinearConstraint(np.hstack([0 * I, I, 0 * I, -K * I]), -np.inf, 0),
            LinearConstraint(np.hstack([0 * I, 0 * I, I, I]), -np.inf, 1)]
    if cells:
        A = coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(len(cells), n)).toarray()
        cons.append(LinearConstraint(np.hstack([A, -A, np.zeros((len(cells), 2 * n))]), 0, np.inf))
    ub = np.concatenate([np.full(2 * n, K), np.ones(2 * n)])
    if signs:
        for i, k in enumerate(keys):
            s = signs.get(k[0])
            if s == 1: ub[n + i] = 0; ub[3 * n + i] = 0
            if s == -1: ub[i] = 0; ub[2 * n + i] = 0
    res = milp(np.concatenate([np.zeros(2 * n), np.ones(2 * n)]), constraints=cons,
               integrality=np.ones(N), bounds=Bounds(np.zeros(N), ub))
    if res.status != 0: return None
    y = res.x[:n] - res.x[n:2 * n]
    return {keys[i]: int(round(v)) for i, v in enumerate(y) if abs(v) > 0.5}


def pure_cert(R, C, D, a=None):
    best = None
    for s in itertools.product((1, -1), repeat=3):
        y = cert(R, C, D, 1, dict(zip('RCD', s)), a)
        if y is not None and (best is None or len(y) < len(best)): best = y
    return best


def sig(y):
    out = []
    for F in 'RCD':
        P = [k[1] for k, v in y.items() if k[0] == F and v > 0]; Nn = [k[1] for k, v in y.items() if k[0] == F and v < 0]
        if P: out.append(f'{F}+{len(P)}')
        if Nn: out.append(f'{F}-{len(Nn)}')
    return ' '.join(out)


def classify(P):
    if not sumtest(*P):
        y = cert(*P, 1)
        return 'L', ('pm1' if y is not None else 'noPM1'), y
    b = hall2(*P)
    if b: return 'H2:' + ','.join(b), '', None
    y = pure_cert(*P)
    if y is not None: return 'H3p', sig(y), y
    y = cert(*P, 1)
    if y is not None: return 'H3m', sig(y), y
    for K in (2, 3, 4, 6):
        y = cert(*P, K)
        if y is not None: return f'W{K}', sig(y), y
    if lp(*P) is None: return 'W>6', '', None
    return 'PAR', par_kinds(*P), None


def par_kinds(R, C, D):
    """per parity choice a: cnt (count mismatch), else first class of the a-restricted board:
    H2:XY bipartite Hall, H3p, H3m, W. Returns sorted set of classes used."""
    Ds = sorted(D); nr1 = sum(r % 2 for r in R); nc1 = sum(c % 2 for c in C); used = Counter()
    for t in itertools.product((0, 1), repeat=len(Ds)):
        a = dict(zip(Ds, t))
        if sum(t) != nr1 or sum((ai + d) % 2 for ai, d in zip(t, Ds)) != nc1: used['cnt'] += 1; continue
        b = hall2(R, C, D, a)
        if b: used['H2'] += 1; continue
        if pure_cert(R, C, D, a) is not None: used['H3p'] += 1; continue
        if cert(R, C, D, 1, None, a) is not None: used['H3m'] += 1; continue
        used['W'] += 1
    return '+'.join(sorted(used))


if __name__ == '__main__':
    m, h = int(sys.argv[1]), int(sys.argv[2])
    t = time.time(); stat = Counter(); kinds = Counter(); sub = Counter(); ex = {}; recs = []
    for R, C, D in boards(m, h):
        if not passes(R, C, D): continue
        stat['boards'] += 1
        for d in sorted(D):
            if 1 + d not in C: continue
            P = peel(R, C, D, (1, 1 + d)); stat['cells'] += 1
            if passes(*P): continue
            stat['bad'] += 1
            k, s, y = classify(P)
            kinds[k] += 1; sub[(k, s)] += 1; ex.setdefault(k, (C, D, d, y)); ex.setdefault((k, s), (C, D, d, y))
            recs.append((C, D, d, k, s, y))
    with open(f'/home/claude/agents/farkas/cls2_m{m}_h{h}.txt', 'w') as f:
        f.write(f'm={m} h={h} {dict(stat)} time={time.time()-t:.0f}s\n')
        for k, v in kinds.most_common(): f.write(f'  {k}: {v}  first={ex[k]}\n')
        f.write(' subkinds:\n')
        for k, v in sub.most_common(): f.write(f'  {k}: {v}  first={ex[k]}\n')
    pickle.dump(recs, open(f'/home/claude/agents/farkas/cls2_m{m}_h{h}.pkl', 'wb'))
    print(open(f'/home/claude/agents/farkas/cls2_m{m}_h{h}.txt').read())
