"""Absolute-coordinate check of the NONNEG failure: x = 4 3 2 1 3 2 1 0 -1 2 against a nonnegative x' with the same
end slack 17 and last letter 2.  Prints |F(x)|, |F(x')| and the states of F(x') (shifted to the same number of
stones) that are not in F(x).  Usage: python3 cexA.py [letters of x' ...]   (default 2 1 5 4 3 2)"""
import sys
from explore import Fset, sh, sums
x = (4, 3, 2, 1, 3, 2, 1, 0, -1, 2)
xp = tuple(int(t) for t in sys.argv[1:]) or (2, 1, 5, 4, 3, 2)
assert sum(xp) == sum(x) and xp[-1] == x[-1] and min(xp) >= 0 and all(b >= a - 1 for a, b in zip(xp, xp[1:]))
Fx, Fp = Fset(sums(x)), Fset(sums(xp)); d = len(x) - len(xp)
if d >= 0: Fp = {(sh(A, d), sh(B, d)) for A, B in Fp}
else: Fx = {(sh(A, -d), sh(B, -d)) for A, B in Fx}
lost = sorted((sorted(A), sorted(B)) for A, B in Fp - Fx)
print(f"x = {x}: sums {sums(x)}, |F(x)| = {len(Fx)};  x' = {xp}: sums {sums(xp)}, |F(x')| = {len(Fp)};  in F(x') but not in F(x): {len(lost)}")
for A, B in lost: print("   rows", A, " cols", B)
