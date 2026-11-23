# Exact check of one (word, pattern, phase): lists all solutions (stone by stone) and the parities of T(R, S).
# R = rows r (1-based) with pattern[(r - p) mod len] == '1'.
# Usage: python3 verify.py "1 1 0 -1 0 0 0 0 0 0 0 0 0 1 0 -1 -1" 00101 2
import sys, collections
e = list(map(int, sys.argv[1].split())); pat = sys.argv[2]; p = int(sys.argv[3]); n = len(e); L = len(pat)
inR = [pat[(r + 1 - p) % L] == '1' for r in range(n)]
f = collections.Counter(); N = 0
def rec(k, rows, cols, S):
    global N
    if k == n: N += 1; f[S] += 1; return
    d = 2 * k + e[k]
    for r in range(max(0, d - n + 1), min(d, n - 1) + 1):
        c = d - r
        if rows >> r & 1 or cols >> c & 1: continue
        rec(k + 1, rows | 1 << r, cols | 1 << c, S | (1 << k if inR[r] else 0))
rec(0, 0, 0, 0)
odd = [S for S in f if f[S] % 2]
print("word %s, R = %s: solutions %d, sets S that occur %d, with T(R, S) odd %d; counts T: %s" % (sys.argv[1], "".join("1" if x else "0" for x in inR), N, len(f), len(odd), sorted(f.values())))
