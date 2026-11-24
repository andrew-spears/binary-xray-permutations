"""Top-stone peeling.  Multiset D (sorted) with sum_{i<=j} d_i >= -j(n-j), total 0  (condition M; for distinct values this
is Landau).  Peel: take a largest value k, put that element above the k smallest others, add 1 to those k, repeat.
1. check that peeling never fails for every M-multiset of size n and yields a poset with below - above = D;
2. for distinct D: over all ways of breaking ties, is some peeled poset an interval order?  2-dimensional (= a solution)?
usage: python3 poset.py n"""
import sys, itertools
from iv import words, comparability
def multisets(n):
    out = []
    def rec(d, tot):
        j = len(d)
        if j == n:
            if tot == 0: out.append(tuple(d))
            return
        lo = d[-1] if d else -(n - 1)
        for v in range(lo, n):
            t = tot + v
            if t < -(j + 1) * (n - j - 1): continue
            if t + v * (n - j - 1) > 0: break
            rec(d + [v], t)
    rec([], 0)
    return out
def peel(vals, allties=False):
    """vals: dict id -> value.  yields lists of (z, S) from the top down."""
    def rec(cur, hist):
        if not cur: yield hist; return
        k = max(cur.values())
        if k < 0 or k > len(cur) - 1: return
        tops = [i for i in cur if cur[i] == k]
        for z in (tops if allties else tops[-1:]):
            rest = sorted((i for i in cur if i != z), key=lambda i: (cur[i], i))
            if k == 0: forced, block, need = [], [], 0
            else:
                v = cur[rest[k - 1]]
                forced = [i for i in rest if cur[i] < v]; block = [i for i in rest if cur[i] == v]; need = k - len(forced)
            for extra in (itertools.combinations(block, need) if allties else [tuple(block[:need])]):
                S = forced + list(extra); new = {i: cur[i] + (i in S) for i in rest}
                yield from rec(new, hist + [(z, frozenset(S))])
    yield from rec(dict(vals), [])
def poset(n, hist):
    below = {z: S for z, S in hist}
    return below
def check(D, below):
    n = len(D)
    for z in below:                                   # transitive?
        for x in below[z]:
            if not below[x] <= below[z]: return False
    return all(len(below[z]) - sum(1 for w in below if z in below[w]) == D[z] for z in range(n))
def interval(below):
    S = sorted(below.values(), key=len)
    return all(a <= b for a, b in zip(S, S[1:]))
def two_dim(n, below):
    E = [(a, b) for a in range(n) for b in range(a + 1, n) if a not in below[b] and b not in below[a]]
    return comparability(n, E)
if __name__ == "__main__":
    n = int(sys.argv[1]); M = multisets(n); bad = 0
    for D in M:
        h = next(peel(dict(enumerate(D))), None)
        if h is None or not check(D, poset(n, h)): bad += 1
    print(f"n = {n}: {len(M)} multisets with condition M; peeling fails or gives a wrong poset: {bad}")
    W = words(n); ni = n2 = 0; exi = []; ex2 = []
    for w in W:
        D = tuple(w[k] + 2 * (k + 1) - n - 1 for k in range(n)); fi = f2 = False
        for h in peel(dict(enumerate(D)), True):
            b = poset(n, h)
            if not fi and interval(b): fi = True
            if not f2 and two_dim(n, b): f2 = True
            if fi and f2: break
        ni += fi; n2 += f2
        if not fi and len(exi) < 3: exi.append(w)
        if not f2 and len(ex2) < 3: ex2.append(w)
    print(f"   {len(W)} valid sets; some peeled poset is an interval order: {ni}; is 2-dimensional: {n2}", exi, ex2)
