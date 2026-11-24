# The two-chain machine.  State: two partitions (P, Q).  A step with letter e is one of
#   A: delete the first row of Q (length q1) and give P a new first column of height e + q1  (needs e + q1 >= number of rows of P)
#   B: delete the first row of P (length p1) and give Q a new first column of height e + p1  (needs e + p1 >= number of rows of Q)
# A word has a two-chain solution iff some sequence of A/B steps leads from (-, -) back to (-, -).
import sys
from functools import lru_cache
def addcol(P, h):
    if h < len(P): return None
    return tuple(x + 1 for x in P) + (1,) * (h - len(P))
def stepA(P, Q, e): 
    q1 = Q[0] if Q else 0; N = addcol(P, e + q1)
    return None if N is None else (N, Q[1:])
def stepB(P, Q, e):
    r = stepA(Q, P, e); return None if r is None else (r[1], r[0])
def runs(w):
    """all choice words leading back to (-, -)"""
    out = []
    def rec(i, P, Q, c):
        if i == len(w):
            if not P and not Q: out.append(c)
            return
        for ch, f in (("A", stepA), ("B", stepB)):
            r = f(P, Q, w[i])
            if r is not None: rec(i + 1, r[0], r[1], c + ch)
    rec(0, (), (), ""); return out
def solvable(w):
    @lru_cache(None)
    def rec(i, P, Q):
        if i == len(w): return not P and not Q
        for f in (stepA, stepB):
            r = f(P, Q, w[i])
            if r is not None and rec(i + 1, r[0], r[1]): return True
        return False
    return rec(0, (), ())
if __name__ == "__main__":
    if sys.argv[1] == "check":        # against brute force
        from blocks import words, sols, lis
        for n in range(2, int(sys.argv[2]) + 1):
            bad = 0; cnt = 0
            for w in words(n):
                D = [e + 2 * (k + 1) - n - 1 for k, e in enumerate(w)]
                bf = sum(1 for p in sols(D, n) if lis(p) <= 2); m = len(runs(w)); cnt += 1
                if (bf > 0) != (m > 0): bad += 1
            print("n =", n, "words", cnt, "disagreements between machine and brute force:", bad)
    else:
        w = tuple(int(x) for x in sys.argv[1:]); print(runs(w))
