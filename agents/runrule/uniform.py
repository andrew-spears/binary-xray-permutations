"""Cones of count vectors of FORMAL words (formal = any letters, stones in the given order, repeated or decreasing
diagonals allowed; the interface machine counts their placements just the same).
C_j(S) = cone spanned by the count vectors of formal words with slacks in [0, S] that end at slack j.
Part 1: the cones C_0(S)..C_S(S), by closing under all letters until no new extreme ray appears (extreme rays found
        by linear programming); prints the generators of C_s(S).
Part 2: every LEGAL beginning x (slacks <= B, length <= N) ending at slack s: is L_x in C_s(S) ?
Question U(s): is C_s(S) = C_s(s) for all S, i.e. do excursions above slack s give nothing new at slack s?
Vectors are written over the classes of states under transposition (per-state counts), labels (row|column) of cone.part.
Usage: python3 uniform.py s S B N [rounds]"""
import sys
import numpy as np
from collections import Counter
from math import gcd
from functools import reduce
from scipy.optimize import linprog
sys.path.insert(0, "../interface")
from count_rule import cstep
from cone import part, prefixes
def prim(C):
    g = reduce(gcd, C.values()); return Counter({t: c // g for t, c in C.items()})
def key(C): return tuple(sorted(C.items()))
def classes_of(vecs, B):
    cl = sorted({tuple(sorted((part(t[0], B), part(t[1], B)))) for C in vecs for t in C}); return cl
def coords(C, cl, B):
    d = {}
    for t, c in C.items():
        k = tuple(sorted((part(t[0], B), part(t[1], B)))); assert d.setdefault(k, c) == c
    return [d.get(k, 0) for k in cl]
def in_cone(v, G):
    """is v a nonnegative combination of the rows of G ?"""
    if len(G) == 0: return False
    A = np.array(G, float).T; b = np.array(v, float); sc = b.sum()
    r = linprog(np.zeros(A.shape[1]), A_eq=A / sc, b_eq=b / sc, bounds=(0, None), method="highs")
    return r.status == 0
def extreme(vs):
    vs = [list(v) for v in dict.fromkeys(map(tuple, vs))]; out = []
    for i, v in enumerate(vs):
        others = [w for j, w in enumerate(vs) if j != i]
        if not in_cone(v, others): out.append(v)
    return out
def low_cones(s, rounds, B):
    """generators (as Counters over states) of the cones C_j of formal words with slacks in [0, s]"""
    base = (1 << B) - 1
    gens = {j: {} for j in range(s + 1)}; gens[0][key(Counter({(base, base): 1}))] = Counter({(base, base): 1})
    word = {key(Counter({(base, base): 1})): ()}
    hist = []
    for rd in range(rounds):
        new = {j: dict(gens[j]) for j in gens}
        for j in gens:
            for C in gens[j].values():
                for e in range(-j, s - j + 1):
                    D = cstep(C, e, B)
                    if D:
                        D = prim(D); k = key(D); new[j + e][k] = D; w = word[key(C)] + (e,)
                        if k not in word or len(w) < len(word[k]): word[k] = w
        changed = False
        for j in new:
            cl = classes_of(new[j].values(), B); vs = {tuple(coords(C, cl, B)): C for C in new[j].values()}
            ext = extreme(list(vs)); kept = {key(vs[tuple(v)]): vs[tuple(v)] for v in ext}
            if set(kept) != set(gens[j]): changed = True
            gens[j] = kept
        hist.append([len(gens[j]) for j in range(s + 1)])
        if not changed: break
    return gens, hist, not changed, word
if __name__ == "__main__":
    s, S, Bd, N = map(int, sys.argv[1:5]); rounds = int(sys.argv[5]) if len(sys.argv) > 5 else 12; B = max(Bd, S) + 2
    gens, hist, stable, word = low_cones(S, rounds, B)
    print(f"formal words with slacks in [0, {S}]: numbers of extreme rays of C_0..C_{S} after each round: {hist}; stable: {stable}")
    cl = classes_of(gens[s].values(), B); GC = sorted(gens[s].values(), key=lambda C: coords(C, cl, B)); G = [coords(C, cl, B) for C in GC]
    print(f"C_{s}({S}): classes {['(%s|%s)' % (''.join(map(str, a)) or '-', ''.join(map(str, b)) or '-') for a, b in cl]}")
    for g, C in zip(G, GC): print("   generator", g, "  a formal word with this count vector (up to a factor):", word[key(C)])
    print(f"   rank {np.linalg.matrix_rank(np.array(G))}, generators {len(G)}")
    seen = {}; tot = 0
    for w, C, sl in prefixes(Bd, N):
        if sl != s or not w: continue
        tot += 1; v = tuple(coords(prim(C), cl + [k for k in classes_of([C], B) if k not in cl], B))    # a class no generator has gets its own coordinate
        if v not in seen: seen[v] = w
    out = [(v, w) for v, w in seen.items() if any(v[len(cl):]) or not in_cone(v[:len(cl)], G)]
    print(f"legal beginnings at slack {s} (slacks <= {Bd}, length <= {N}): {tot}, distinct directions {len(seen)}, outside C_{s}({S}): {len(out)}")
    for v, w in sorted(out, key=lambda z: len(z[1]))[:5]: print("   outside:", w, v)
    # DEL0 on pairs of generators:  N(Z, Z') = sum_t Z(t) Z'(J t),  N0 = the same after a letter 0 on the left
    def mirror(m): return sum(1 << (B + (-1 - u)) for u in range(-B, B) if not m >> (B + u) & 1)
    Jt = lambda t: (mirror(t[0]), mirror(t[1]))
    form = lambda Z, Z2: sum(c * Z2.get(Jt(t), 0) for t, c in Z.items())
    Dm = [[form(cstep(Z, 0, B), Z2) - form(Z, Z2) for Z2 in GC] for Z in GC]
    neg = sum(x < 0 for r in Dm for x in r)
    print(f"DEL0 form N(Z 0 Z') - N(Z Z') on pairs of generators of C_{s}({S}): {neg} negative of {len(G) ** 2}; symmetric: {all(Dm[i][j] == Dm[j][i] for i in range(len(G)) for j in range(len(G)))}")
    if len(G) <= 8:
        for r in Dm: print("   ", r)
    # facets of the cone (inequalities valid on all generators, tight on a spanning set), by brute force for small cones
    if len(G) <= 12:
        from itertools import combinations
        from fractions import Fraction
        def null1(rows):
            """the integer vector spanning the null space of the rows, if it is one-dimensional"""
            if not rows: return None                               # a cone of rank 1 has no facet
            M = [[Fraction(x) for x in r] for r in rows]; nc = len(M[0]); piv = []; r = 0
            for c in range(nc):
                p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
                if p is None: continue
                M[r], M[p] = M[p], M[r]; M[r] = [x / M[r][c] for x in M[r]]
                for i in range(len(M)):
                    if i != r and M[i][c] != 0: M[i] = [x - M[i][c] * y for x, y in zip(M[i], M[r])]
                piv.append(c); r += 1
            free = [c for c in range(nc) if c not in piv]
            if len(free) != 1: return None
            v = [Fraction(0)] * nc; v[free[0]] = Fraction(1)
            for i, c in enumerate(piv): v[c] = -M[i][free[0]]
            l = reduce(lambda x, y: x * y // gcd(x, y), [x.denominator for x in v]); v = [int(x * l) for x in v]; g = reduce(gcd, v)
            return [x // g for x in v]
        d = np.linalg.matrix_rank(np.array(G)); facets = set()
        for sub in combinations(range(len(G)), d - 1):
            n = null1([G[i] for i in sub])
            if n is None: continue
            vals = [sum(a * b for a, b in zip(n, v)) for v in G]
            if all(x >= 0 for x in vals): facets.add(tuple(n))
            elif all(x <= 0 for x in vals): facets.add(tuple(-x for x in n))
        names = ["L(%s|%s)" % ("".join(map(str, a)) or "-", "".join(map(str, b)) or "-") for a, b in cl]
        print(f"facets of C_{s}({S}): {len(facets)}")
        for n in sorted(facets): print("    0 <= " + " ".join(f"{'+' if c > 0 else '-'} {abs(c) if abs(c) != 1 else ''}{nm}" for c, nm in zip(n, names) if c))
    gs = {tuple(g) for g in G}; cidx = {c: i for i, c in enumerate(cl)}
    def Jvec(C): return tuple(coords(Counter({Jt(t): c for t, c in C.items()}), cl, B))
    print(f"all generators 0/1 vectors: {all(set(g) <= {0, 1} for g in G)};  generator set invariant under the half-turn J: {all(Jvec(C) in gs for C in GC)}")
