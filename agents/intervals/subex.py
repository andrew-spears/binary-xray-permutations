"""Interval orders as left-justified triangles.  Order the intervals by right endpoint; interval t lies above the first
k_t of them, 0 <= k_t <= t - 1 (any such sequence is an interval order, and every interval order arises).  Then
    below - above of interval t  =  k_t - #{t' > t : k_t' >= t}.
Which multisets of n values arise?  Compare with condition M (sorted partial sums >= -j(n-j), total 0).
usage: python3 subex.py n"""
import sys, itertools
from poset import multisets
n = int(sys.argv[1]); got = set()
for k in itertools.product(*[range(t) for t in range(1, n + 1)]):
    col = [0] * (n + 1)
    for kt in k: col[kt] += 1            # col[j] = #{t : k_t = j}; #{t' : k_t' >= t} = suffix sum (t' > t automatic)
    suf = 0; d = [0] * n
    for t in range(n, 0, -1):
        suf += col[t] if t <= n else 0
        d[t - 1] = k[t - 1] - suf
    got.add(tuple(sorted(d)))
M = set(multisets(n))
print(f"n = {n}: {len(M)} multisets with condition M; from interval orders: {len(got)}; M not reached: {len(M - got)}; reached outside M: {len(got - M)}", sorted(M - got)[:5])
