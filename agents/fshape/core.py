"""Shared helpers for agents/fshape.  Absolute, order-free form (see ../interface/SHORTEN_BRIEF.md).
A prefix x = (e_1..e_k) has sums t_j = 2j + e_j.  A state is (A, B): bitmasks of used rows / columns (bit r = row r, r >= 1).
F(T) = set of (A, B) over placements of the sums T on distinct rows and distinct columns."""
from functools import lru_cache
def sums(x): return tuple(2 * (j + 1) + e for j, e in enumerate(x))
def step(S, t):
    """all states after adding one stone of sum t to the states in S"""
    out = set()
    for A, B in S:
        for r in range(1, t):
            if A >> r & 1 or B >> (t - r) & 1: continue
            out.add((A | 1 << r, B | 1 << (t - r)))
    return out
@lru_cache(None)
def F(T):
    """T: sorted tuple of sums"""
    if not T: return frozenset([(0, 0)])
    return frozenset(step(F(T[:-1]), T[-1]))
def Fx(x): return F(sums(x))
def bits(m): return tuple(i for i in range(m.bit_length()) if m >> i & 1)
def mask(s):
    m = 0
    for i in s: m |= 1 << i
    return m
def sh(m, c=1): return (m << c) | ((1 << (c + 1)) - 2)          # Sh^c: shift up by c, fill rows 1..c
def legal_prefixes(K, B, letters=None):
    """all legal prefixes of length <= K with slacks <= B (distinct diagonals); letters = allowed set or None"""
    out = []; stack = [((), 0)]
    while stack:
        w, s = stack.pop(); out.append(w)
        if len(w) == K: continue
        lo = 0 if not w else max(-s, w[-1] - 1)
        for e in range(lo, B - s + 1):
            if letters is not None and e not in letters: continue
            stack.append((w + (e,), s + e))
    return out
def part(m, k):
    """partition (parts x_i - i, decreasing) of the k-set with mask m"""
    return tuple(sorted((x - i - 1 for i, x in enumerate(bits(m))), reverse=True))
def partitions(n, m=None):
    if m is None: m = n
    if n == 0: yield (); return
    for i in range(min(n, m), 0, -1):
        for p in partitions(n - i, i): yield (i,) + p
def setof(lam, k):
    """mask of the k-set with partition lam (largest part goes to the largest element)"""
    lam = tuple(lam) + (0,) * (k - len(lam)); m = 0
    for i in range(k): m |= 1 << (k - i + lam[i])
    return m
def all_states(k, s):
    out = []
    for i in range(s + 1):
        for l in partitions(i):
            if len(l) > k: continue
            for mu in partitions(s - i):
                if len(mu) > k: continue
                out.append((setof(l, k), setof(mu, k)))
    return out
def nodd(m): return bin(m & 0xAAAAAAAAAAAAAAAA).count("1")       # rows are numbered from 1: odd rows are odd bits
def pcount(a, x):
    """(P): the four class sizes, or None"""
    k = len(x); p = sum(e & 1 for e in x); z = k - p; ro, co = nodd(a[0]), nodd(a[1])
    if (ro + co - p) & 1: return None
    oo = (ro + co - p) // 2; oe = (p + ro - co) // 2
    if min(oo, z - oo, oe, p - oe) < 0: return None
    return oo, z - oo, oe, p - oe
