"""2-adic valuation of the number N(D) of solutions.  Usage: python3 val.py n
Enumerates all permutations of size n, groups by D, prints for each valid D without a tight cut: letters, N, v_2(N), odd part."""
import sys, itertools
from collections import Counter
n = int(sys.argv[1]); N = Counter()
def rec(r, used, sums, cur):
    if r == n: N[tuple(sorted(cur))] += 1; return
    for c in range(n):
        if not used >> c & 1 and not sums >> (r + c) & 1:
            cur.append(r + c + 2); rec(r + 1, used | 1 << c, sums | 1 << (r + c), cur); cur.pop()
rec(0, 0, 0, [])
def v2(x):
    v = 0
    while x % 2 == 0: x //= 2; v += 1
    return v
hist = Counter()
for D in sorted(N):
    e = [d - 2 * (k + 1) for k, d in enumerate(D)]; sl = 0; tight = False
    for x in e[:-1]:
        sl += x
        if sl == 0: tight = True
    if tight: continue
    v = v2(N[D]); hist[v] += 1
    if len(sys.argv) > 2: print(" ".join(f"{x:2d}" for x in e), " N =", N[D], " v2 =", v, " odd part", N[D] >> v, " max slack", max(sum(e[:i]) for i in range(n + 1)), " #odd letters", sum(x % 2 for x in e))
print(f"n = {n}: no-tight-cut D: {sum(hist.values())}; histogram of v_2(N): {sorted(hist.items())}")
