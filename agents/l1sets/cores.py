"""F(x) against its 2-core saturation.  For each distinct (F, slack) over L1 prefixes with slacks <= S: Pi = set of pairs of 2-core charges (a, b)
occurring in F, sat = all states of that slack with (a, b) in Pi; prints |F|, |sat|, Pi, the words (up to 3 shortest), and the missing states.
  python3 cores.py S"""
import sys
from fsets import *
def c0(m):
    W = Mo.W
    return sum(1 for k in range(0, W) if k % 2 == 0 and m >> (k + W) & 1) - sum(1 for k in range(-W, 0) if k % 2 == 0 and not m >> (k + W) & 1)
ab = [[(c0(t[0]), c0(t[1])) for t in L] for L in St]
def sat(F, s):
    Pi = {ab[s][i] for i in range(len(St[s])) if F >> i & 1}
    return sum(1 << i for i in range(len(St[s])) if ab[s][i] in Pi), Pi
if __name__ == "__main__":
    for s in range(S + 1):
        allPi = sorted(set(ab[s]))
        print(f"s {s}: core pairs possible: {allPi}")
        for (F, s2), w in sorted(seen.items(), key=lambda kv: (len(kv[1]), kv[1])):
            if s2 != s: continue
            T, Pi = sat(F, s)
            print(f"   |F| = {bin(F).count('1'):4d} of sat {bin(T).count('1'):4d}; a+b in {sorted({a + b for a, b in Pi})}, all pairs with these sums: {Pi == {p for p in allPi if sum(p) in {a + b for a, b in Pi}}}; x = {' '.join(map(str, w))}; missing: {names(T & ~F, s)}")
