"""Order-free F on sets of sums.  State = (rowmask, colmask), bit r-1 set = row r used (rows, columns >= 1)."""
from functools import lru_cache
def place(states, s):
    out = set()
    for A, B in states:
        for a in range(1, s):
            b = s - a
            if A >> (a - 1) & 1 or B >> (b - 1) & 1: continue
            out.add((A | 1 << (a - 1), B | 1 << (b - 1)))
    return out
_cache = {}
def F(sums):
    sums = tuple(sorted(sums))
    if sums in _cache: return _cache[sums]
    if not sums: r = {(0, 0)}
    else: r = place(F(sums[:-1]), sums[-1])
    _cache[sums] = r
    return r
def Sh(st):
    A, B = st
    return (A << 1 | 1, B << 1 | 1)
def sums_of(word):
    return tuple(2 * (j + 1) + e for j, e in enumerate(word))
def legal_words(K, B, lastmax=None):
    """all legal prefixes of length <= K with slacks <= B"""
    out = []
    def rec(w, s):
        out.append(tuple(w))
        if len(w) == K: return
        lo = 0 if not w else max(-s, w[-1] - 1)
        for e in range(lo, B - s + 1):
            w.append(e); rec(w, s + e); w.pop()
    rec([], 0)
    return out
def bits(m): return tuple(i + 1 for i in range(m.bit_length()) if m >> i & 1)
