"""Finite matrices per slack level.  States of slack s are the pairs of partitions of total size s.  For a rule u -> v
with letter sum 0 (DEL0: () -> (0); PEAK: (0) -> (1,0,-1)) let D_s = T_v - T_u on the states of slack s, and J the
mirror (180 degree rotation of the board), so that  N(x v y) - N(x u y) = L_x^T G_s L_{y*},  G_s = D_s J,
y* = y reversed and negated.  Prints for each s: dimension, symmetry, rank, signature and the most negative entry of G_s.
Usage: python3 gram.py smax"""
import sys
import numpy as np
from collections import Counter
sys.path.insert(0, "../interface")
from count_rule import cstep
smax = int(sys.argv[1]); B = smax + 4; base = (1 << B) - 1
def mirror(m): return sum(1 << (B + (-1 - u)) for u in range(-B, B) if not m >> (B + u) & 1)
J = lambda t: (mirror(t[0]), mirror(t[1]))
def size(m): return sum(u + 1 for u in range(0, B + 1) if m >> (B + u) & 1) + sum(u + 1 for u in range(-B, 0) if not m >> (B + u) & 1) * -1
levels = {0: {(base, base)}}                                   # closure: states by slack
for _ in range(2 * smax + 2):
    for s in list(levels):
        for t in list(levels[s]):
            for e in range(-s, smax + 1 - s):
                for t2 in cstep(Counter({t: 1}), e, B): levels.setdefault(s + e, set()).add(t2)
def apply(t, w):
    C = Counter({t: 1})
    for e in w: C = cstep(C, e, B)
    return C
# sanity: N(xy) = sum_t L_x(t) L_{y*}(J t)
x, y = (1, 1, 0), (0, -1, -1); Lx = apply((base, base), x); Ly = apply((base, base), tuple(-e for e in reversed(y)))
assert sum(c * Ly[J(t)] for t, c in Lx.items()) == apply((base, base), x + y)[(base, base)], "mirror convention"
for name, u, v in (("DEL0", (), (0,)), ("PEAK", (0,), (1, 0, -1))):
    for s in range(smax + 1):
        S = sorted(levels[s]); idx = {t: i for i, t in enumerate(S)}; n = len(S); D = np.zeros((n, n))
        for t in S:
            for t2, c in apply(t, v).items(): D[idx[t], idx[t2]] += c
            for t2, c in apply(t, u).items(): D[idx[t], idx[t2]] -= c
        G = np.zeros((n, n))
        for t in S: G[:, idx[t]] = D[:, idx[J(t)]]
        sym = np.allclose(G, G.T); ev = np.linalg.eigvalsh((G + G.T) / 2)
        print(f"{name} slack {s}: dim {n}, G symmetric {sym}, rank {np.linalg.matrix_rank(G)}, eigenvalues >0: {(ev > 1e-9).sum()} <0: {(ev < -1e-9).sum()}, min entry {G.min():.0f}, entries <0: {(G < 0).sum()} of {n * n}")
