"""LR numbers against placement counts.  For a prefix x with letters >= 0 (d_k = 2k + x_k), L_x(R, C) = number of
placements with used rows R and columns C, and c_x(lam, gam) = coefficient of s_lam(X) s_gam(Y) in the skew Schur
function s_theta(x)(X u Y) = det(h_{d_j - 2i}) (an LR number; L = c mod 2 by ../unimodal/REPORT.md).
Question: is every state with c > 0 reachable (L > 0)?  Is c <= L?   Usage: python3 lrpos.py LEN SLACK"""
import sys
sys.argv, av = [sys.argv[0], "1", "1"], sys.argv
sys.path.insert(0, "../unimodal")
from parity import placements, shape, strip, kostka, splits, partitions, words
from itertools import permutations
def lr(x, lam, gam):
    m = len(x); D = [2 * k + e for k, e in enumerate(x, 1)]; tot = 0
    for p in permutations(range(m)):
        al = [D[p[i]] - 2 * (i + 1) for i in range(m)]
        if min(al) < 0: continue
        sg = 1
        for i in range(m):
            for j in range(i): sg *= -1 if p[j] > p[i] else 1
        al = tuple(a for a in al if a)
        for a, b in splits(al):
            if sum(a) == sum(lam): tot += sg * kostka(lam, a) * kostka(gam, b)
    return tot
LEN, S = int(av[1]), int(av[2]); nw = pos = unreach = bigger = reach = 0; ex = []
for x in words(LEN, S, False):
    P = {(strip(shape(R)), strip(shape(C))): v for (R, C), v in placements(x).items()}; nw += 1; sl = sum(x); reach += len(P)
    for a in range(sl + 1):
        for lam in partitions(a):
            for gam in partitions(sl - a):
                c = lr(x, lam, gam); assert c >= 0
                if c:
                    pos += 1; L = P.get((lam, gam), 0)
                    if L == 0: unreach += 1; ex.append((x, lam, gam, c))
                    elif c > L: bigger += 1
                assert (c - P.get((lam, gam), 0)) % 2 == 0
print(f"prefixes with letters >= 0, length <= {LEN}, slack <= {S}: {nw}; reachable states {reach}; states with c > 0: {pos}; of these unreachable (L = 0): {unreach}; reachable with c > L: {bigger}", ex[:4])
