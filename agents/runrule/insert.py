"""Block insertion.  For a valid word b (prefix sums >= 0, total 0, solvable) test, over all words of length <= n:
  INSERT(b): N(x b y) >= N(b) N(x y)       whenever x y and x b y are both legal words with a solution
  SUBST(b):  N(x b y) >= N(b) N(x 0 y)     whenever x 0 y and x b y are
DEL0 is INSERT((0)); PEAK is SUBST((1,0,-1)) with N(b) = 2.  At a tight cut (slack 0 after x) both are equalities.
Usage: python3 insert.py n kmax     (blocks of length <= kmax)"""
import sys
from collections import defaultdict
from fractions import Fraction
from countlib import solutions
n, kmax = int(sys.argv[1]), int(sys.argv[2]); sol = solutions(n); N = {w: len(s) for w, s in sol.items()}
blocks = sorted((b for b in N if len(b) <= kmax), key=lambda b: (len(b), b))
tot = {"INSERT": [0, 0], "SUBST": [0, 0]}; worst = {}
for b in blocks:
    for kind, mid in (("INSERT", ()), ("SUBST", (0,))):
        if kind == "SUBST" and not any(b): continue
        cnt = bad = eq = 0; least = None; ex = None
        for w in N:
            if len(w) + len(b) - len(mid) > n: continue
            for i in range(len(w) + 1):
                if w[i:i + len(mid)] != mid: continue
                w2 = w[:i] + b + w[i + len(mid):]
                if w2 not in N: continue
                cnt += 1; r = Fraction(N[w2], N[b] * N[w])
                if r < 1: bad += 1
                if r == 1: eq += 1
                if least is None or r < least: least = r; ex = (w, N[w], w2, N[w2])
        if cnt == 0: continue
        tot[kind][0] += cnt; tot[kind][1] += bad
        if bad or len(b) <= 3 or b in ((2, 1, 0, -1, -2), (1, 1, 0, -1, -1), (1, 0, -1, 1, 0, -1)):
            print(f"{kind:6} b = {str(b):22} N(b) = {N[b]:3}  placements {cnt:6}  violations {bad:5}  equalities {eq:6}  least ratio {float(least):.3f}" + (f"  e.g. {ex}" if bad else ""))
print("totals (placements, violations):", tot, "blocks:", len(blocks))
