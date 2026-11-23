"""Meet in the middle: sizes of the forward and backward reachable interface sets.
F_k = pairs (used rows, used columns) reachable by placing the k smallest diagonals;
G_k = pairs from which the n-k largest diagonals can be completed.  D has a witness iff F_k meets G_k.
N_k = number of all pairs of partitions with sigma_k boxes that fit the board (k-subsets of [n]).
If |F_k| + |G_k| > N_k at one cut k, pigeonhole gives a witness (k = 1 is useless: F_1 is everything).
Reports, over all no-tight-cut valid D: the ratio at the middle cut k = n/2, its minimum over cuts, and min_k |F_k|/N_k.
Usage: python3 meet.py nmax"""
import sys
from math import comb
from check_walks import valid_Ds

def levels(n, e):
    F = [{(0, 0)}]
    for k in range(n):
        T = set()
        for R, C in F[-1]:
            for r in range(1, n + 1):
                if R >> r & 1: continue
                c = 2 * (k + 1) + e[k] - r
                if c < 1 or c > n or C >> c & 1: continue
                T.add((R | 1 << r, C | 1 << c))
        F.append(T)
    return F

def npairs(n, k, sig):
    # number of pairs of k-subsets of [n] with total excess sig: partitions in a k x (n-k) box
    # p[j] = number of partitions of j with at most k parts each <= n-k
    p = [0] * (sig + 1)
    def rec(parts_left, maxpart, tot):
        p[tot] += 1
        if parts_left == 0: return
        for x in range(1, maxpart + 1):
            if tot + x > sig: break
            rec(parts_left - 1, x, tot + x)
    rec(k, n - k, 0)
    return sum(p[a] * p[sig - a] for a in range(sig + 1))

for n in range(4, int(sys.argv[1]) + 1):
    cnt = 0; st = {"mid": [9, None, 0], "min": [9, None, 0], "minF": [9, None, 0]}
    for D in valid_Ds(n):
        s = [D[k] + n - (k + 1) for k in range(n)]
        if not all(sum(s[:k]) > comb(k, 2) for k in range(1, n)): continue
        e = [s[k] - k for k in range(n)]
        F = levels(n, e); Gm = levels(n, [-x for x in reversed(e)])
        sig = 0; vals = {}; dens = {}
        for k in range(1, n):
            sig += e[k - 1]; N = npairs(n, k, sig)
            vals[k] = (len(F[k]) + len(Gm[n - k])) / N; dens[k] = len(F[k]) / N
        cnt += 1
        for name, v in (("mid", vals[n // 2]), ("min", min(vals.values())), ("minF", min(dens.values()))):
            if v <= (1 if name != "minF" else 0.5): st[name][2] += 1
            if v < st[name][0]: st[name][0], st[name][1] = v, D
    print(f"n={n}: {cnt} D | middle cut (|F|+|G|)/N: worst {st['mid'][0]:.3f} {st['mid'][1]}, <=1 for {st['mid'][2]} | "
          f"min over cuts: worst {st['min'][0]:.3f}, <=1 for {st['min'][2]} | min_k |F_k|/N_k: worst {st['minF'][0]:.3f} {st['minF'][1]}, <=1/2 for {st['minF'][2]}")
