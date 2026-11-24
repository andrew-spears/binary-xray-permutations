"""Row residues mod M.  f(a) = parity of the number of solutions of D in which stone k lies in a row = a_k (mod M)
(rows 0-based).  Prints, for each valid D of size n, N and the number of a with f(a) odd; with 'v' the odd a themselves.
Usage: python3 resid.py n M [v]"""
import sys
from collections import defaultdict, Counter
n, M = int(sys.argv[1]), int(sys.argv[2]); verbose = len(sys.argv) > 3
W = defaultdict(list)
def rec(r, used, sums, cur):
    if r == n: W[tuple(sorted(cur))].append(tuple(cur)); return
    for c in range(n):
        if not used >> c & 1 and not sums >> (r + c) & 1:
            cur.append(r + c); rec(r + 1, used | 1 << c, sums | 1 << (r + c), cur); cur.pop()
rec(0, 0, 0, [])
none = 0; hist = Counter()
for D in sorted(W):
    pos = {d: k for k, d in enumerate(D)}; f = Counter()
    for cur in W[D]:
        a = [0] * n
        for r, d in enumerate(cur): a[pos[d]] = r % M
        f[tuple(a)] ^= 1
    odd = sorted(a for a in f if f[a]); hist[len(odd)] += 1
    e = [d - 2 * k for k, d in enumerate(D)]
    if not odd: none += 1; print("  no odd pattern:", e, "N =", len(W[D]))
    if verbose: print(e, "N =", len(W[D]), "odd patterns:", len(odd), [''.join(map(str, a)) for a in odd[:12]])
print(f"n = {n}, M = {M}: valid D {len(W)}; without an odd residue pattern: {none}; histogram of #odd patterns: {sorted(hist.items())[:10]}")
