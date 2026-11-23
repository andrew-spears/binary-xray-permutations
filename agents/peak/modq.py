"""Residue count test (generalises the parity count, card paritycount, from mod 2 to mod q).
A placement of the sums T on rows A, columns B gives a q x q matrix N (N[i][j] = number of stones with row = i,
column = j mod q) with row sums #{a in A: a = i}, column sums #{b in B: b = j} and, for every residue s,
sum of N[i][j] over i + j = s equal to #{t in T: t = s}.  If no such non-negative integer matrix exists, (A, B) is
not reachable.  feasible(A, B, T, q) decides this by exhaustive search (q <= 8, small boards)."""
import sys
from itertools import product
def feasible(A, B, T, q):
    r = [0] * q; c = [0] * q; n = [0] * q
    for a in A: r[a % q] += 1
    for b in B: c[b % q] += 1
    for t in T: n[t % q] += 1
    def comps(total, caps):
        if len(caps) == 1:
            if total <= caps[0]: yield (total,)
            return
        for v in range(min(total, caps[0]) + 1):
            for rest in comps(total - v, caps[1:]): yield (v,) + rest
    def rec(i, c, n):
        if i == q: return all(x == 0 for x in c) and all(x == 0 for x in n)
        for row in comps(r[i], c):
            n2 = list(n); ok = True
            for j, v in enumerate(row):
                n2[(i + j) % q] -= v
                if n2[(i + j) % q] < 0: ok = False; break
            if ok and rec(i + 1, [c[j] - row[j] for j in range(q)], n2): return True
        return False
    return rec(0, c, n)
if __name__ == "__main__":
    from explore import Fset, sh, sums
    cases = [((3, 4, 3, 3, 2, 1), "PEAK"), ((3, 4, 3, 2, 3, 2, 1), "PEAK"), ((3, 2, 4, 3, 3, 2, 1, 0), "PEAK"), ((2, 3, 3, 2, 2, 1, 1, 0), "ZERO")]
    for w, rule in cases:
        S = sums(w); k = len(w)
        if rule == "PEAK": Tu = S + [2 * k + 2]; Tv = S + [2 * k + 3, 2 * k + 4, 2 * k + 5]; j = 2
        else: Tu = S + [2 * k + 1]; Tv = S + [2 * k + 2, 2 * k + 3]; j = 1
        Fu = Fset(Tu); Fv = Fset(Tv)
        lost = [(sh(A, j), sh(B, j)) for A, B in Fu if (sh(A, j), sh(B, j)) not in Fv]
        print(rule, "x =", w, " lost", len(lost))
        for A, B in lost:
            print("   rows", sorted(A), "cols", sorted(B), " count test for the longer word: mod 2", feasible(A, B, Tv, 2), " mod 4", feasible(A, B, Tv, 4), " mod 8", feasible(A, B, Tv, 8))
