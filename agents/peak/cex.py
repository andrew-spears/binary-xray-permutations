"""Independent brute-force check of the PEAK counterexample (absolute coordinates, no window, no bitmasks).
x = (3, 4, 3, 3, 2, 1): sums 5, 8, 9, 11, 12, 13.   F(x 0): add 14.   F(x 1 0 -1): add 15, 16, 17.
PEAK would say Sh^2 F(x 0) is inside F(x 1 0 -1)  (Sh^2(A) = (A + 2) u {1, 2})."""
import sys
from explore import Fset, sh, sums
w = tuple(int(t) for t in sys.argv[1:]) or (3, 4, 3, 3, 2, 1)
S = sums(w); m = len(w) + 1
F0 = Fset(S + [2 * m]); F1 = Fset(S + [2 * m + 1, 2 * m + 2, 2 * m + 3])
lost = [(A, B) for A, B in F0 if (sh(A, 2), sh(B, 2)) not in F1]
print("x =", w, "sums", S, "slack", sum(w))
print("|F(x 0)| =", len(F0), " |F(x 1 0 -1)| =", len(F1), " states of F(x 0) missing from F(x 1 0 -1):", len(lost))
for A, B in lost: print("   rows", sorted(A), "cols", sorted(B))
def placement(T, A, B):
    """one placement of the sums T on rows A, columns B (None if there is none)"""
    T = sorted(T)
    def rec(i, A, B):
        if i == len(T): return []
        for a in sorted(A):
            b = T[i] - a
            if b in B:
                r = rec(i + 1, A - {a}, B - {b})
                if r is not None: return [(a, b)] + r
        return None
    return rec(0, frozenset(A), frozenset(B))
for A, B in lost:
    print("   placement of x 0 on rows", sorted(A), "cols", sorted(B), ":", placement(S + [2 * m], A, B),
          "| x 1 0 -1 on the shifted board:", placement(S + [2 * m + 1, 2 * m + 2, 2 * m + 3], sh(A, 2), sh(B, 2)))
