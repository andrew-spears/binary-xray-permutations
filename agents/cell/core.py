"""Core: parity-restricted LP, parity test, peeling.
Board = (R, C, D) with R, C, D tuples of ints. Cell (r, c) has diagonal c - r.
a = dict d -> parity of the row used for diagonal d."""
import itertools
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix


def cells_of(R, C, D, a=None):
    Cs = set(C)
    return [(r, r + d) for d in sorted(D) for r in R
            if r + d in Cs and (a is None or r % 2 == a[d])]


def lp(R, C, D, a=None, obj=None):
    """Restricted LP. Returns (cells, x) or None if infeasible."""
    cells = cells_of(R, C, D, a)
    m = len(R)
    if not cells: return None
    Ri = {r: i for i, r in enumerate(sorted(R))}
    Ci = {c: i for i, c in enumerate(sorted(C))}
    Di = {d: i for i, d in enumerate(sorted(D))}
    rows, cols = [], []
    for j, (r, c) in enumerate(cells):
        rows += [Ri[r], m + Ci[c], 2 * m + Di[c - r]]; cols += [j, j, j]
    if len(set(rows)) < 3 * m: return None
    A = coo_matrix((np.ones(len(rows)), (rows, cols)), shape=(3 * m, len(cells))).tocsr()
    c = np.zeros(len(cells)) if obj is None else obj(len(cells))
    res = linprog(c, A_eq=A, b_eq=np.ones(3 * m), bounds=(0, None), method="highs")
    if res.status != 0: return None
    return cells, res.x


def parity_choices(R, C, D):
    """All a passing the integral class-count check (necessary for LP feasibility)."""
    Ds = sorted(D); Cs = set(C)
    ch = [sorted({r % 2 for r in R if r + d in Cs}) for d in Ds]
    if any(not x for x in ch): return
    nr1 = sum(r % 2 for r in R); nc1 = sum(c % 2 for c in C)
    for t in itertools.product(*ch):
        if sum(t) != nr1: continue
        if sum((ai + d) % 2 for ai, d in zip(t, Ds)) != nc1: continue
        yield dict(zip(Ds, t))


def passing(R, C, D, first=True, hint=None):
    """List of passing parity choices a (first one only if first=True)."""
    out = []
    if hint is not None and lp(R, C, D, hint) is not None:
        out.append(hint)
        if first: return out
    for a in parity_choices(R, C, D):
        if hint is not None and a == hint: continue
        if lp(R, C, D, a) is not None:
            out.append(a)
            if first: return out
    return out


def peel(R, C, D, cell):
    r, c = cell
    return (tuple(x for x in R if x != r), tuple(x for x in C if x != c),
            tuple(x for x in D if x != c - r))


def placement(R, C, D):
    Cs = set(C); Ds = sorted(D, key=lambda d: sum(1 for r in R if r + d in Cs))
    used_r, used_c, sol = set(), set(), {}
    def rec(i):
        if i == len(Ds): return True
        d = Ds[i]
        for r in R:
            if r not in used_r and r + d in Cs and r + d not in used_c:
                used_r.add(r); used_c.add(r + d); sol[d] = r
                if rec(i + 1): return True
                used_r.discard(r); used_c.discard(r + d); del sol[d]
        return False
    return dict(sol) if rec(0) else None


def passes(R, C, D):
    """Parity test; placement-derived parity tried first as a hint."""
    if len(R) == 0: return True
    p = placement(R, C, D)
    if p is not None: return True   # integral placement is itself a feasible restricted LP point
    return bool(passing(R, C, D))


def sumtest(R, C, D):
    m = len(R); Rs, Cs, Ds = sorted(R), sorted(C), sorted(D)
    if sum(Ds) != sum(Cs) - sum(Rs): return False
    for k in range(1, m):
        if sum(Ds[:k]) < sum(Cs[:k]) - sum(Rs[-k:]): return False
        if sum(Ds[-k:]) > sum(Cs[-k:]) - sum(Rs[:k]): return False
    return True


def tight(R, C, D):
    m = len(R); Rs, Cs, Ds = sorted(R), sorted(C), sorted(D)
    for k in range(1, m):
        if sum(Ds[:k]) == sum(Cs[:k]) - sum(Rs[-k:]): return True
        if sum(Ds[-k:]) == sum(Cs[-k:]) - sum(Rs[:k]): return True
    return False
