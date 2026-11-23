"""Does forced-move propagation + (sum test, bipartite Hall) explain the bad cells not caught by L/H2?
Propagation: while some row/col/diagonal has exactly one cell, place it (delete its row, col, diag).
Usage: python3 prop.py m h   (reads cls2_m{m}_h{h}.pkl)"""
import sys, pickle
from collections import Counter
sys.path.insert(0, '/home/claude/agents/cell')
from core import cells_of, peel, sumtest
from classify import hall2


def propagate(R, C, D):
    while R:
        cells = cells_of(R, C, D)
        cnt = {}
        for (r, c) in cells:
            for k in (('R', r), ('C', c), ('D', c - r)): cnt.setdefault(k, []).append((r, c))
        for k in [('R', r) for r in R] + [('C', c) for c in C] + [('D', d) for d in D]:
            if k not in cnt: return None  # dead
        f = next((v[0] for v in cnt.values() if len(v) == 1), None)
        if f is None: return R, C, D
        R, C, D = peel(R, C, D, f)
    return R, C, D


def caught(P):
    Q = propagate(*P)
    if Q is None: return 'dead'
    if not Q[0]: return None
    if not sumtest(*Q): return 'L'
    if hall2(*Q): return 'H2'
    return None


if __name__ == "__main__":
    m, h = int(sys.argv[1]), int(sys.argv[2])
    recs = pickle.load(open(f'/home/claude/agents/farkas/cls2_m{m}_h{h}.pkl', 'rb'))
    R = tuple(range(1, m + 1)); out = Counter(); ex = {}
    for C, D, d, k, s, y in recs:
        P = peel(R, C, D, (1, 1 + d))
        c = caught(P)
        out[(k, c is not None)] += 1
        if c is None: ex.setdefault(k, (C, D, d, s, y))
    print(m, h, sorted(out.items()))
    for k, v in ex.items(): print('  uncaught', k, v)
