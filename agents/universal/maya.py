"""The interface machine on pairs of partitions (lambda = row holes, mu = column holes).
Occupied row offsets relative to the frontier: {lambda_i - i : i >= 1}.  A letter e adds a row at a free offset u and
a column at a free offset v with u + v = e, then the frontier moves up by one.  The slack is |lambda| + |mu|."""
from functools import lru_cache

@lru_cache(maxsize=None)
def add(lam, u):
    """Partition after adding the row at offset u (None if occupied): the new row has h holes below it,
    u = h - #{parts > h}; the parts > h drop by one and h becomes a part."""
    for h in range(max(u, 0), u + len(lam) + 1):
        j = sum(1 for p in lam if p > h)
        if h - j == u:
            return tuple(p for p in tuple(q - 1 for q in lam[:j]) + (h,) + lam[j:] if p)
    return None

@lru_cache(maxsize=None)
def succ(st, e):
    lam, mu = st
    out = set()
    for u in range(-len(lam), e + len(mu) + 1):
        a = add(lam, u)
        if a is None: continue
        b = add(mu, e - u)
        if b is not None: out.add((a, b))
    return frozenset(out)

def step(S, e):
    out = set()
    for st in S: out |= succ(st, e)
    return frozenset(out)

START = frozenset([((), ())])

def F(word):
    S = START
    for e in word: S = step(S, e)
    return S
