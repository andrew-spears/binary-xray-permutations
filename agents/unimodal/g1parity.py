"""Parity of the number of placements with rows [m], columns [m+1] minus {c}, for every SET D of m sums.
Usage: python3 g1parity.py M"""
import sys
from itertools import permutations
from collections import Counter
M = int(sys.argv[1])
for m in range(2, M + 1):
    for c in range(1, m + 2):
        cols = [j for j in range(1, m + 2) if j != c]; cnt = Counter()
        for p in permutations(cols):
            D = tuple(sorted(i + 1 + p[i] for i in range(m)))
            if len(set(D)) == m: cnt[D] += 1
        odd = sum(1 for v in cnt.values() if v % 2); print(f"m={m} c={c}: {len(cnt)} sets D with a placement, {odd} with an odd number")
