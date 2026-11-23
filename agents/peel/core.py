import itertools, functools, sys
from collections import defaultdict

def canon(R, C, D):
    a, b = min(R), min(C)
    R2 = tuple(r - a + 1 for r in sorted(R)); C2 = tuple(c - b + 1 for c in sorted(C))
    D2 = frozenset(d - (b - a) for d in D)
    return R2, C2, D2

@functools.lru_cache(maxsize=None)
def achievable(R, C):
    """R, C canonical tuples. Returns set of frozensets D achievable (binary placements)."""
    m = len(R); off = m + max(C)  # diag d -> bit d+off
    states = {(0, 0)}
    for r in R:
        new = set()
        for cm, dm in states:
            for j, c in enumerate(C):
                if cm >> j & 1: continue
                b = 1 << (c - r + off)
                if dm & b: continue
                new.add((cm | 1 << j, dm | b))
        states = new
    out = set()
    for cm, dm in states:
        out.add(frozenset(i - off for i in range(dm.bit_length()) if dm >> i & 1))
    return out

def sum_test(R, C, D):
    R = sorted(R); C = sorted(C); D = sorted(D); m = len(R)
    if sum(D) != sum(C) - sum(R): return False
    for k in range(1, m):
        if sum(D[:k]) < sum(C[:k]) - sum(R[-k:]): return False
        if sum(D[-k:]) > sum(C[-k:]) - sum(R[:k]): return False
    return True

def all_sumtest_D(R, C):
    lo = min(C) - max(R); hi = max(C) - min(R); m = len(R)
    tot = sum(C) - sum(R)
    for D in itertools.combinations(range(lo, hi + 1), m):
        if sum(D) == tot and sum_test(R, C, D):
            yield frozenset(D)

def is_ok(R, C, D):
    R2, C2, D2 = canon(R, C, D)
    return D2 in achievable(R2, C2)

def holes(S):
    S = sorted(S); return [x for x in range(S[0], S[-1] + 1) if x not in set(S)]

def side_sets(m, kind):
    """canonical sets of size m starting at 1 for a side-class."""
    out = []
    if kind == 'h1':      # interval minus <=1 element
        out.append(tuple(range(1, m + 1)))
        for h in range(2, m + 1): out.append(tuple(x for x in range(1, m + 2) if x != h))
    elif kind.startswith('blk'):  # interval minus one contiguous block of length <= L
        L = int(kind[3:])
        out.append(tuple(range(1, m + 1)))
        for l in range(1, L + 1):
            for h in range(2, m + 1):
                out.append(tuple(x for x in range(1, m + l + 1) if not h <= x < h + l))
    elif kind.startswith('k'):    # interval minus <=K elements (any)
        K = int(kind[1:])
        for k in range(K + 1):
            for hs in itertools.combinations(range(2, m + k), k):
                out.append(tuple(x for x in range(1, m + k + 1) if x not in hs))
    elif kind == 'int':
        out.append(tuple(range(1, m + 1)))
    return out

def in_side(S, kind):
    h = holes(S)
    if kind == 'int': return not h
    if kind == 'h1': return len(h) <= 1
    if kind.startswith('blk'):
        L = int(kind[3:]); return not h or (len(h) <= L and h[-1] - h[0] == len(h) - 1)
    if kind.startswith('k'): return len(h) <= int(kind[1:])

def peels(R, C, D):
    R = sorted(R); C = sorted(C)
    res = []
    for name, r in (('top', R[0]), ('bot', R[-1])):
        for c in C:
            if c - r in D: res.append((name, r, c))
    for name, c in (('left', C[0]), ('right', C[-1])):
        for r in R:
            if c - r in D: res.append((name, r, c))
    return res

def apply(R, C, D, r, c):
    return tuple(x for x in R if x != r), tuple(x for x in C if x != c), D - {c - r}
