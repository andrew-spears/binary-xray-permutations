"""Shared helpers for agents/intervals2.
Triangle form of an interval order: k_1..k_n with 0 <= k_t <= t-1 (interval t, in order of right endpoint, lies above
the first k_t intervals); value v_t = k_t - #{t' : k_t' >= t}."""
import itertools
def valid_sets(n):
    """all sorted tuples of n distinct integers with sum_{i<=j} d_i >= -j(n-j), total 0."""
    out = []
    def rec(d, tot):
        j = len(d)
        if j == n:
            if tot == 0: out.append(tuple(d))
            return
        lo = d[-1] + 1 if d else -(n - 1)
        for v in range(lo, n):
            t = tot + v
            if t < -(j + 1) * (n - j - 1): continue
            rec(d + [v], t)
    rec([], 0)
    return out
def values(k):
    n = len(k); col = [0] * (n + 2)
    for kt in k: col[kt] += 1
    suf = 0; v = [0] * n
    for t in range(n, 0, -1):
        suf += col[t]
        v[t - 1] = k[t - 1] - suf
    return tuple(v)
def decode(v):
    """list v (order of right endpoints) -> k or None.  Deterministic peel from the end."""
    n = len(v); k = [0] * n; cnt = [0] * (n + 2)   # cnt[j] = #{t' processed: k_t' >= j}
    for t in range(n, 0, -1):
        kt = v[t - 1] + cnt[t]
        if kt < 0 or kt > t - 1: return None
        k[t - 1] = kt
        for j in range(1, kt + 1): cnt[j] += 1
    return tuple(k)
def all_lists(n):
    """dict: sorted distinct D -> list of realizable lists v"""
    res = {}
    for k in itertools.product(*[range(t) for t in range(1, n + 1)]):
        v = values(k)
        if len(set(v)) == n: res.setdefault(tuple(sorted(v)), []).append(v)
    return res
