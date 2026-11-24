"""Two failures of ZERO that are forced-stone arguments, not small-modulus residue counts (REPORT.md, section 1).
x = (2, c, c-1, ..., 1) 0^m; claim: F(x -1) is not inside F(x 0 -1), for (m, c) = (1, 5) [slack 17] and (2, 6) [slack 23].
Brute force over the order-free model of lib.py; prints the missing states, one placement of each in the short word,
and the moduli m <= 16 whose residue count excludes the target (modcount.py).   Usage: python3 far.py   (about 1 minute)"""
from lib import *
from modcount import failing_moduli
def one_placement(sums, A, B):
    if not sums: return []
    s = sums[-1]
    for a in bits(A):
        b = s - a
        if b >= 1 and B >> (b - 1) & 1:
            r = one_placement(sums[:-1], A & ~(1 << (a - 1)), B & ~(1 << (b - 1)))
            if r is not None: return r + [(a, b)]
    return None
for m, c in [(1, 4), (1, 5), (2, 5), (2, 6)]:
    x = (2,) + tuple(range(c, 0, -1)) + (0,) * m
    su, sv = sums_of(x + (-1,)), sums_of(x + (0, -1))
    X, Y = F(su), F(sv); miss = [t for t in X if Sh(t) not in Y]
    print(f"x = {x}, slack {sum(x)}: |F(x -1)| = {len(X)}, |F(x 0 -1)| = {len(Y)}, missing {len(miss)}")
    for A, B in miss[:2]:
        TA, TB = Sh((A, B))
        print("   state rows", bits(A), "cols", bits(B), "sums", su); print("      placement", one_placement(su, A, B))
        print("   target rows", bits(TA), "cols", bits(TB), "sums", sv)
        print("      residue count excludes the target for m in", failing_moduli(bits(TA), bits(TB), sv, 16), "(m <= 16)")
