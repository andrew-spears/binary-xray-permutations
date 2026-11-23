"""v_2(N(D)) against p/2, p = number of odd letters (all valid D of size n).  Usage: python3 val2.py n"""
import sys
from collections import Counter
sys.argv, av = [sys.argv[0], "1"], sys.argv
import importlib.util
n = int(av[1]); N = Counter()
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
gap = Counter(); ex = {}
for D, c in N.items():
    p = sum(d % 2 for d in D); g = v2(c) - p // 2; gap[g] += 1; ex.setdefault(g, ([d - 2 * (k + 1) for k, d in enumerate(D)], c))
print(f"n = {n}: {len(N)} valid D; v_2(N) - p/2: {sorted(gap.items())}")
for g in sorted(ex)[:2] + sorted(ex)[-1:]: print("   gap", g, ex[g])
