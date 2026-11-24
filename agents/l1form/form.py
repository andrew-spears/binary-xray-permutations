"""Class l1 (letters e_k in {-1,0,+1}; stone k at (row, col) = (pi(k), rho(k)) with pi(k) + rho(k) = 2k + e_k, reflected rows).
RESTRICTED FORM:  at a + :  pi(k) = k,     rho(k) = k + 1
                  at a - :  pi(k) = k - 1, rho(k) = k
                  at a 0 :  pi(k) = k + t, rho(k) = k - t   for some integer t = t_k.
The images of the + and - positions under pi are Plus and Minus-1, disjoint exactly because '+ -' adjacent is not a legal
word (it would repeat a diagonal).  What is left is the MIDPOINT PROBLEM on the zeros Z:
     A = [n] minus (Plus u (Minus-1)),   B = [n] minus ((Plus+1) u Minus):   pair A with B so that the midpoints are exactly Z.
A is Z with each zero that stands just before a run of l minuses moved up by l; B is Z with each zero just after a run of
l pluses moved down by l.
This script counts solutions of the midpoint problem for every valid word of length n.
Usage: python3 form.py n [-v]"""
import sys
def words(n):
    def rec(w, s):
        if len(w) == n:
            if s == 0: yield tuple(w)
            return
        for e in (-1, 0, 1):
            if s + e < 0 or s + e > n - len(w) - 1: continue
            if e == -1 and w and w[-1] == 1: continue
            w.append(e); yield from rec(w, s + e); w.pop()
    yield from rec([], 0)
def sets(w):
    n = len(w); P = {k for k in range(1, n + 1) if w[k - 1] == 1}; M = {k for k in range(1, n + 1) if w[k - 1] == -1}
    Z = [k for k in range(1, n + 1) if w[k - 1] == 0]
    A = set(range(1, n + 1)) - P - {k - 1 for k in M}; B = set(range(1, n + 1)) - {k + 1 for k in P} - M
    return Z, A, B
def count(Z, A, B, limit=None):
    Z = list(Z); A = set(A); B = set(B)
    def rec(i):
        if i == len(Z): return 1
        z = Z[i]; tot = 0
        for a in list(A):
            b = 2 * z - a
            if b in B:
                A.discard(a); B.discard(b); tot += rec(i + 1); A.add(a); B.add(b)
                if limit and tot >= limit: return tot
        return tot
    return rec(0)
if __name__ == "__main__":
    n = int(sys.argv[1]); tot = bad = 0; mn = None
    for w in words(n):
        Z, A, B = sets(w); c = count(Z, A, B, None if "-v" in sys.argv else 1); tot += 1
        if c == 0:
            bad += 1
            if bad <= 5: print("  no restricted solution:", "".join("-0+"[e + 1] for e in w))
        if "-v" in sys.argv and (mn is None or c < mn[0]): mn = (c, w)
    print(f"n = {n}: {tot} valid words, {bad} without a solution of the restricted form" + (f"; fewest solutions {mn[0]} at {''.join('-0+'[e+1] for e in mn[1])}" if mn else ""))
