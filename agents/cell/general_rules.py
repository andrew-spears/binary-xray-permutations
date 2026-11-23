"""General R, C subsets of {1..N} (|R|=|C|=m, normalized: 1 and N each in R or C). For boards passing the
parity test (non-tight sum test): count parity-passing boards with no placement (holes), and check
rule d (some top-row cell peels) and 'any' (some cell peels). Usage: python3 general_rules.py N m"""
import sys, itertools
from core import *

N, m = int(sys.argv[1]), int(sys.argv[2])
cnt = dict(boards=0, passing=0, holes=0, d_fail=0, any_fail=0); ex = {}
for R in itertools.combinations(range(1, N + 1), m):
    for C in itertools.combinations(range(1, N + 1), m):
        if (1 not in R and 1 not in C) or (N not in R and N not in C): continue
        lo, hi = min(C) - max(R), max(C) - min(R)
        for D in itertools.combinations(range(lo, hi + 1), m):
            if not sumtest(R, C, D) or tight(R, C, D): continue
            cnt['boards'] += 1
            if not passes(R, C, D): continue
            cnt['passing'] += 1
            if placement(R, C, D) is None: cnt['holes'] += 1; ex.setdefault('hole', (R, C, D))
            r0 = R[0]
            if not any(passes(*peel(R, C, D, (r0, r0 + d))) for d in D if r0 + d in C):
                cnt['d_fail'] += 1; ex.setdefault('d', (R, C, D))
                if not any(passes(*peel(R, C, D, e)) for e in cells_of(R, C, D)):
                    cnt['any_fail'] += 1; ex.setdefault('any', (R, C, D))
print(N, m, cnt, ex)
