# Candidate canonical rules, each tested on every valid word up to n = N; prints the smallest failure.
#  R1 the solution that is lexicographically smallest (row by row) has at most three chains
#  R2 ... lexicographically largest
#  R3 some solution with the fewest blocks (runs of neighbouring rows going to neighbouring columns) has at most three chains
#  R4 corner rule: D = (two-chain solvable set) + (a corner block): some three-chain solution is X (-) identity or identity (-) X
#  R5 some three-chain solution has a third level (stones with two stones up-left of them in an antichain) forming one block
#  R6 some three-chain solution uses at most three places (values of column - row)
import sys
from lib import *
from two import accepts
def levels(pi):
    lev = []
    for i, c in enumerate(pi): lev.append(1 + max([lev[r] for r in range(i) if pi[r] > c], default=0))
    return lev
def corner(e):
    n = len(e); L = set(lines(e))
    for c in range(0, n):
        ap = {n - c + 2 * t for t in range(c)}
        if ap <= L:
            w = word_of(sorted(x - c for x in L - ap))
            if valid(w) and accepts(w): return True
    return False
N = int(sys.argv[1]); first = {}
for n in range(2, N + 1):
    for e in words(n):
        A = sols(e, n) if n <= 9 else None; S = sols(e, 3)
        tests = {}
        if A is not None:
            tests["R1"] = width(min(A)) <= 3; tests["R2"] = width(max(A)) <= 3
            mb = min(len(blocks(p)) for p in A); tests["R3"] = any(width(p) <= 3 for p in A if len(blocks(p)) == mb)
        tests["R4"] = corner(e)
        def oneblock(p):
            rows = [i for i, l in enumerate(levels(p)) if l == 3]
            return all(rows[t + 1] == rows[t] + 1 and p[rows[t + 1]] == p[rows[t]] + 1 for t in range(len(rows) - 1))
        tests["R5"] = any(oneblock(p) for p in S)
        tests["R6"] = any(len(set(c - i for i, c in enumerate(p))) <= 3 for p in S)
        for k, v in tests.items():
            if not v and k not in first: first[k] = e
for k in ["R1", "R2", "R3", "R4", "R5", "R6"]: print(k, "first failure:", first.get(k, "none up to n = %d%s" % (N, " (R1-R3 only to n = 9)" if k < "R4" else "")))
