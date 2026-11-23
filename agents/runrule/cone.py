"""The cone of count vectors.  L_x(t) = number of placements of the prefix x ending in the interface state t.
For each slack s <= smax collect the vectors L_x (x legal prefix, length <= N, slacks <= B, slack s at the end),
written in partition labels and folded by transposition (L_x is symmetric under swapping rows and columns).
Prints the classes, the extreme rays of the cone they span (by prefix length, to see whether it stabilises) and its
facets, i.e. the linear inequalities satisfied by every L_x in range.     Usage: python3 cone.py B N smax"""
import sys
import numpy as np
from collections import Counter, defaultdict
from fractions import Fraction
from math import gcd
from functools import reduce
from scipy.spatial import ConvexHull
sys.path.insert(0, "../interface")
from count_rule import cstep
def part(mask, B):
    out = []; holes = 0
    for u in range(-B, B + 1):
        if mask >> (B + u) & 1:
            if holes: out.append(holes)
        else: holes += 1
    return tuple(reversed(out))
def label(t, B):
    return tuple(sorted((part(t[0], B), part(t[1], B))))          # unordered pair = class under transposition
def prefixes(B, N):
    base = (1 << B) - 1
    def rec(w, C, s, last):
        yield w, C, s
        if len(w) == N: return
        for e in range(0 if last is None else max(-s, last - 1), B - s + 1): yield from rec(w + (e,), cstep(C, e, B), s + e, e)
    yield from rec((), Counter({(base, base): 1}), 0, None)
def collect(B, N, smax):
    vecs = defaultdict(dict)                                       # s -> primitive vector (as tuple over classes) -> shortest prefix
    classes = defaultdict(set)
    raw = defaultdict(list)
    for w, C, s in prefixes(B, N):
        if s > smax or s == 0: continue
        d = Counter()
        for t, c in C.items(): d[label(t, B)] += c
        classes[s].update(d); raw[s].append((w, d))
    out = {}
    for s in raw:
        cl = sorted(classes[s]); V = {}
        for w, d in raw[s]:
            v = [d[c] for c in cl]; g = reduce(gcd, v); v = tuple(x // g for x in v)
            if v not in V or len(w) < len(V[v]): V[v] = w
        out[s] = (cl, V)
    return out
def hull(V):
    """extreme rays and facets of the cone spanned by the integer vectors V (dict vector -> prefix)"""
    P = np.array([np.array(v, float) / sum(v) for v in V]); keys = list(V)
    A = P[:, :-1]                                                   # drop last coordinate (sum = 1)
    if A.shape[1] == 1:
        i, j = A[:, 0].argmin(), A[:, 0].argmax(); return [keys[i], keys[j]], None
    h = ConvexHull(A, qhull_options="QJ" if False else "")
    return [keys[i] for i in h.vertices], h
if __name__ == "__main__":
    B, N, smax = map(int, sys.argv[1:4])
    data = collect(B, N, smax)
    for s in sorted(data):
        cl, V = data[s]
        print(f"\nslack {s}: {len(cl)} classes {cl}\n  {len(V)} distinct directions L_x")
        if len(cl) == 1: continue
        try: ext, h = hull(V)
        except Exception as ex: print("  hull failed:", str(ex)[:100]); continue
        print(f"  extreme rays: {len(ext)}; by length of the shortest prefix: {sorted(Counter(len(V[v]) for v in ext).items())}")
        for v in sorted(ext, key=lambda v: (len(V[v]), V[v]))[:14]: print("   ", v, "x =", V[v])
        if h is not None:
            print(f"  facets: {len(h.equations)}")
            for eq in h.equations[:30]:
                # a.p + b <= 0 on the hull, p = first k-1 normalised coordinates; homogenise with sum = 1
                a = list(eq[:-1]) + [0.0]; a = [-(x + eq[-1]) for x in a]; m = max(abs(x) for x in a)
                a = [x / m for x in a]
                print("    ", " + ".join(f"{x:.3f}*L{cl[i]}" for i, x in enumerate(a) if abs(x) > 1e-9), ">= 0")
