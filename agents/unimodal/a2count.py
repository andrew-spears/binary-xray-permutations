"""c(x) = number of A2 placements of a 0/1 word x: rows [m], columns [m+1] minus {m+1-s}, sums {2k + x_k}.
Prints, per length, the distribution of c(x) over all words 1...0 (the other words reduce to these).
Usage: python3 a2count.py M"""
import sys
from itertools import product
from collections import Counter
from a2look import sols
M = int(sys.argv[1])
for m in range(2, M + 1):
    cnt = Counter(); ex = {}
    for w in product((0, 1), repeat=m - 2):
        x = (1,) + w + (0,); c = len(sols(x)[0]); cnt[c] += 1; ex.setdefault(c, x)
    print(m, sorted(cnt.items()), "even counts:", sum(v for k, v in cnt.items() if k % 2 == 0), " words with c = 1:", cnt[1])
