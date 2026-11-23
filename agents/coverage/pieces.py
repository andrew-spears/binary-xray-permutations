"""For uncovered D, min over witnesses of #AP pieces (one-line notation, contiguous runs with constant step).
Usage: python3 pieces.py n"""
import sys
from collections import Counter
from common import *

n = int(sys.argv[1])
cnt = Counter(); ex = {}
for line in open(f"uncovered_{n}.txt"):
    D = sorted(eval(line.split("  ")[0]))
    best = [n + 1, None]
    p = [0] * n

    # DFS tracking pieces greedily: state (pieces, start of current piece, step)
    def rec(i, usedD, usedC, pieces, plen, step):
        if pieces >= best[0] or (pieces == best[0] - 1 and False):
            return
        if i == n:
            best[0], best[1] = pieces, tuple(p)
            return
        r = i + 1
        for j, d in enumerate(D):
            if usedD >> j & 1:
                continue
            c = r + d
            if 1 <= c <= n and not usedC >> c & 1:
                p[i] = c
                if i == 0:
                    np_, nl, ns = 1, 1, None
                elif plen == 1:
                    np_, nl, ns = pieces, 2, c - p[i - 1]
                elif c - p[i - 1] == step:
                    np_, nl, ns = pieces, plen + 1, step
                else:
                    np_, nl, ns = pieces + 1, 1, None
                rec(i + 1, usedD | 1 << j, usedC | 1 << c, np_, nl, ns)

    rec(0, 0, 0, 0, 0, None)
    cnt[best[0]] += 1
    ex.setdefault(best[0], []).append((D, best[1]))
print(n, dict(sorted(cnt.items())))
for k in sorted(ex):
    for D, w in ex[k][:3]:
        print(" ", k, D, w)
