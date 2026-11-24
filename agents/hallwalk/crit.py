# The Hall walk is a reflection.  For a solution (rows r_i, columns c_i = L_i - r_i) and a move of stones p (line a -> a+1)
# and q (line b -> b-1), put k1 = c_p + 1 - r_q and k2 = c_q - 1 - r_p.  For k in {k1, k2} let phi_k(r) = the row of the
# stone in column r + k (undefined off the board).  phi_k is a partial injection: its orbits are cycles and exactly |k| paths.
# Claim checked here: some Hall walk succeeds  <=>  for k = k1 or k = k2, r_p and r_q are NOT on two different paths of phi_k.
# In particular |k1| <= 1 or |k2| <= 1 is enough.
import sys
from collections import Counter
from hw import valid_sets, solutions, walk, moves
def comp(n, rowofcol, k, r):
    """('cycle', None) or ('path', start row) for the phi_k orbit of row r."""
    x = r
    while True:                       # go backwards: predecessor of x is the row y with phi(y) = x, i.e. y = col(x) - k
        y = colof[x] - k
        if y < 1 or y > n: return ('path', x)
        x = y
        if x == r: return ('cycle', None)
N = int(sys.argv[1])
for n in range(4, N + 1):
    bad = 0; pairs = 0; nm = 0; nosmall = 0; small_ok = 0; worst = None; kstat = Counter()
    for L in valid_sets(n):
        sols = solutions(L)
        for (x, y, T) in moves(L):
            nm += 1; hassmall = False; best = 99
            for pi in sols:
                pairs += 1
                colof = {pi[i]: L[i] - pi[i] for i in range(n)}
                rp, rq, cp, cq = pi[x], pi[y], L[x] - pi[x], L[y] - pi[y]
                pred = False
                for k in (cp + 1 - rq, cq - 1 - rp):
                    A = comp(n, None, k, rp); B = comp(n, None, k, rq)
                    if not (A[0] == 'path' and B[0] == 'path' and A[1] != B[1]): pred = True
                    best = min(best, abs(k))
                    if abs(k) <= 1: hassmall = True
                act = any(walk(L, T, pi, p, q, f, s)[0] for (p, q) in ((x, y), (y, x)) for f in (0, 1) for s in (0, 1))
                if act != pred: bad += 1; worst = worst or (L, T, pi)
            kstat[best] += 1
            if not hassmall: nosmall += 1
    print("n =", n, "moves", nm, "pairs", pairs, "criterion wrong:", bad, worst, "| moves with no solution having |k| <= 1:", nosmall, "| smallest |k| over solutions:", sorted(kstat.items()))
