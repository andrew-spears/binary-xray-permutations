"""At a cut x | z the overlap pattern between left and right intervals is a Ferrers graph, so the left labels lam and
the right labels are conjugate partitions:  x z has an interval order  <=>  F(x) meets conj(F(zbar)), zbar = z reversed
and negated.  Test: do F(x) and conj F(zbar) have a least and a greatest element in dominance order, and is the meet of
the two greatest elements / the join of the two least elements in both sets?
usage: python3 cut.py n"""
import sys
from iv import words
from pm import succ
conj = lambda u: tuple(sum(1 for p in u if p > i) for i in range(u[0] if u else 0))
def ps(u, L): 
    out = []; t = 0
    for j in range(L): t += u[j] if j < len(u) else 0; out.append(t)
    return out
def dom(u, v, L): return all(a <= b for a, b in zip(ps(u, L), ps(v, L)))   # u below v
def meet(u, v, L):
    m = [min(a, b) for a, b in zip(ps(u, L), ps(v, L))]
    return tuple(x for x in (m[j] - (m[j - 1] if j else 0) for j in range(L)) if x)
join = lambda u, v, L: conj(meet(conj(u), conj(v), L))
n = int(sys.argv[1]); memo = {}
def F(x):
    if x not in memo:
        memo[x] = frozenset({()}) if not x else frozenset(v for u in F(x[:-1]) for v in succ(u, x[-1]))
    return memo[x]
cuts = nomin = nomax = badmeet = badjoin = 0; ex = []
for w in words(n):
    for k in range(1, n):
        x = w[:k]; zb = tuple(-e for e in reversed(w[k:])); s = sum(x)
        if s == 0: continue
        A = F(x); B = frozenset(conj(u) for u in F(zb)); L = s + 1; cuts += 1
        assert A & B
        def ext(S, lo):
            c = [u for u in S if all((dom(u, v, L) if lo else dom(v, u, L)) for v in S)]
            return c[0] if c else None
        a, b, c, d = ext(A, 1), ext(A, 0), ext(B, 1), ext(B, 0)
        if a is None or c is None: nomin += 1
        if b is None or d is None: nomax += 1
        if b is not None and d is not None and meet(b, d, L) not in A & B:
            badmeet += 1
            if len(ex) < 3: ex.append(("meet", x, w[k:], meet(b, d, L), sorted(A & B)[:4]))
        if a is not None and c is not None and join(a, c, L) not in A & B:
            badjoin += 1
            if len(ex) < 6: ex.append(("join", x, w[k:], join(a, c, L), sorted(A & B)[:4]))
print(f"n = {n}: {cuts} cuts with slack > 0; no least element {nomin}; no greatest {nomax}; meet of tops not common {badmeet}; join of bottoms not common {badjoin}")
for t in ex: print("  ", t)
