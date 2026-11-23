"""Reflection positivity test.  For prefixes x, y ending at the same slack s, G[x, y] = N(x mirror(y)) =
number of solutions of the word x followed by the mirror (reversed, negated) of y.  Is G positive semidefinite?
Usage: python3 rp.py K B    (prefixes of length <= K, slacks <= B, legal: first letter >= 0, e >= last - 1)"""
import sys, numpy as np
from collections import defaultdict
def prefixes(K, B):
    out = defaultdict(list)                       # slack -> list of (word, {(R, C): count})
    def go(w, s, last, L):
        if w: out[s].append((tuple(w), L))
        if len(w) == K: return
        k = len(w) + 1
        for e in range(0 if last is None else max(-s, last - 1), B - s + 1):
            t = 2 * k + e; M = defaultdict(int)
            for (R, C), c in L.items():
                for r in range(1, t):
                    if r not in R and t - r not in C: M[(R | {r}, C | {t - r})] += c
            if M: w.append(e); go(w, s + e, e, dict(M)); w.pop()
    go([], 0, None, {(frozenset(), frozenset()): 1}); return out
def gram(P):
    m = len(P); G = np.zeros((m, m))
    for i, (x, Lx) in enumerate(P):
        for j, (y, Ly) in enumerate(P):
            n = len(x) + len(y); full = set(range(1, n + 1)); tot = 0
            for (R, C), c in Lx.items():
                if max(R) > n or max(C) > n: continue
                R2 = frozenset(n + 1 - r for r in full - R); C2 = frozenset(n + 1 - r for r in full - C)
                tot += c * Ly.get((R2, C2), 0)
            G[i, j] = tot
    return G
if __name__ == "__main__":
    K, B = int(sys.argv[1]), int(sys.argv[2]); out = prefixes(K, B)
    for s in sorted(out):
        P = out[s]; G = gram(P); ev = np.linalg.eigvalsh(G)
        print(f"slack {s}: {len(P)} prefixes, rank {np.linalg.matrix_rank(G)}, least eigenvalue {ev[0]:.4f}, largest {ev[-1]:.1f}, symmetric {np.allclose(G, G.T)}")
    P = out[2]; G = gram(P); best = None                    # smallest explicit violation of Cauchy-Schwarz
    for i in range(len(P)):
        for j in range(len(P)):
            if G[i, j] ** 2 > G[i, i] * G[j, j] and (best is None or len(P[i][0]) + len(P[j][0]) < best[0]):
                best = (len(P[i][0]) + len(P[j][0]), P[i][0], P[j][0], G[i, i], G[j, j], G[i, j])
    print("slack 2, N(x mirror y)^2 > N(x mirror x) N(y mirror y):", best)
