"""Odd states of a prefix (used by par.py and extreme.py)."""
from parity import shape
def conj(p):
    return tuple(sum(1 for a in p if a > i) for i in range(p[0])) if p else ()
def odd_states(x):
    cur = {((), ())}
    for k, e in enumerate(x, 1):
        d = 2 * k + e; nxt = set()
        for (R, C) in cur:
            for r in range(1, d):
                c = d - r
                if r in R or c in C: continue
                nxt ^= {(tuple(sorted(R + (r,))), tuple(sorted(C + (c,))))}
        cur = nxt
    return frozenset((tuple(a for a in shape(R) if a), tuple(a for a in shape(C) if a)) for R, C in cur)
