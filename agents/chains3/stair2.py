# Staircase words S(k, j) = k..1 0^j -1..-k.  Corner rule: remove the central run of c lines n-c, n-c+2, ..., n+c-2
# (a corner block of c stones) and ask whether the rest, shifted by -c, has a two-chain solution (two.py machine).
import sys
from lib import *
from two import accepts, runs
from two_check import rebuild
K, J = int(sys.argv[1]), int(sys.argv[2])
for k in range(1, K + 1):
    for j in range(1, J + 1):
        e = list(range(k, 0, -1)) + [0] * j + list(range(-1, -k - 1, -1)); n = len(e); L = set(lines(e)); good = []
        for c in range(0, n):
            ap = {n - c + 2 * t for t in range(c)}
            if not ap <= L: continue
            rest = sorted(x - c for x in L - ap); w = word_of(rest)
            if valid(w) and accepts(w): good.append(c)
        print(k, j, "corner sizes that work:", good)
