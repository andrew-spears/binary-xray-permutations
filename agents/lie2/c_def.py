"""Part C: induction on the deficiency  delta = (n(n+1) - sum m)/2  (delta = 0 is type A_{n-1}: all signs forced +).
Step tested: a target with delta > 0 has a solution in which one minus row (i, -v), reading |i - v|, can be flipped to +
(reading i + v) so that the values stay distinct -- i.e. m comes from a solved target m' of smaller deficiency by one flip.
Variants: the flipped row reads the smallest value m_n; the flipped row reads the largest value read by a minus row.
Usage: python3 c_def.py n"""
import sys
from ctype import targets, solutions
n = int(sys.argv[1]); T = [m for m in targets(n) if sum(m) < n * (n + 1)]
any_, small, big, one = [], [], [], []
for m in T:
    a = s = b = o = False; M = set(m)
    for sol in solutions(n, m):
        minus = [(i, -v) for i, v in sol if v < 0]
        top = max(abs(i - v) for i, v in minus)
        o |= len(minus) == 1
        for i, v in minus:
            if i + v not in M:
                a = True; s |= abs(i - v) == m[-1]; b |= abs(i - v) == top
    if not a: any_.append(m)
    if not s: small.append(m)
    if not b: big.append(m)
    if not o: one.append(m)
print(f"C_{n}: {len(T)} targets with delta > 0.  No flippable minus row in any solution: {len(any_)} {any_[:3]}")
print(f"   none where the flipped row reads m_n: {len(small)} {small[:3]}")
print(f"   none where the flipped row reads the largest minus value: {len(big)} {big[:3]}")
print(f"   no solution with exactly one minus row: {len(one)} {one[:3]}")
