"""Does the conjecture survive repeated diagonals?  b = (b_1 <= ... <= b_n) integer, majorized by
(2,4,...,2n) (prefix sums >= k(k+1), equality at n).  Is b = rho + gamma for two permutations?
Reports the first failures per n.  Usage: python3 nonstrict.py nmax"""
import sys, itertools
def sums(n):
    S = set()
    perms = list(itertools.permutations(range(1, n+1)))
    ident = tuple(range(1, n+1))
    for g in perms:                      # wlog sort b, so pair identity-ordered rho with any gamma, then sort
        S.add(tuple(sorted(ident[i] + g[i] for i in range(n))))
    return S
def cands(n):
    def rec(k, last, tot, cur):
        if k == n:
            if tot == n * (n + 1): yield tuple(cur)
            return
        for x in range(last, 2 * n + 1):
            t = tot + x
            if t < (k + 1) * (k + 2): continue
            if t + x * (n - k - 1) > n * (n + 1): break
            cur.append(x); yield from rec(k + 1, x, t, cur); cur.pop()
    yield from rec(0, 2, 0, [])
for n in (range(2, int(sys.argv[1]) + 1) if __name__ == "__main__" else []):
    S = sums(n); bad = [b for b in cands(n) if b not in S]
    strictbad = [b for b in bad if len(set(b)) == n]
    print(n, "candidates", sum(1 for _ in cands(n)), "not a sum of two permutations:", len(bad), "strict among them:", len(strictbad), "first:", bad[:3])
    from collections import Counter
    print("   failures by max multiplicity:", dict(Counter(max(Counter(b).values()) for b in bad)),
          "| candidates by max multiplicity:", dict(Counter(max(Counter(b).values()) for b in cands(n))))
