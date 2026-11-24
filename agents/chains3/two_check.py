# Check the two-chain machine (two.py) both ways: (i) the machine accepts e  <=>  complete search finds a two-chain solution;
# (ii) every accepted run rebuilds a permutation with the right lines and at most two chains.
import sys
from lib import *
from two import step, runs, accepts
def rebuild(e, c):
    n = len(e); st = ((), ()); jA = jB = 0; pi = [None] * n
    for i in range(n):
        lam, mu = st
        if c[i] == "A":
            al = len(mu); phi = e[i] + al; row, col = jA + jB - al, jA + jB + phi; jA += 1
        else:
            al = len(lam); phi = e[i] + al; row, col = jB + jA + phi, jB + jA - al; jB += 1
        pi[row] = col
        st = [s for s, cc in step(st, e[i]) if cc == c[i]][0]
    return tuple(pi)
if __name__ == "__main__":
    N = int(sys.argv[1])
    for n in range(2, N + 1):
        W = words(n); bad = mism = nr = 0
        for e in W:
            R = runs(e); a = bool(R); bad += not a; nr += len(R)
            if bool(sols(e, 2, 1)) != a: mism += 1
            S = set()
            for c in R:
                pi = rebuild(e, c); S.add(pi)
                if not check(e, pi, 2): mism += 1
            if len(S) != len(sols(e, 2)): mism += 1
        print("n", n, "words", len(W), "without two chains", bad, "accepted runs", nr, "mismatches", mism)
