"""Vacuity check for plainOK: count boards R={1..k}, C a k-subset of {lo..hi} (span k+h), any D passing the
sum test (tight allowed), that pass the PLAIN LP but fail the parity test.  Usage: python3 lp_holes.py k h"""
import sys, itertools
sys.path.insert(0, '/home/claude/agents/cell')
from core import lp, passes, sumtest

k, h = int(sys.argv[1]), int(sys.argv[2]); R = tuple(range(1, k + 1)); n = 0; ex = []
for C in itertools.combinations(range(1, k + h + 1), k):
    if 1 not in C or k + h not in C: continue   # exact span k+h
    for D in itertools.combinations(range(min(C) - k, max(C)), k):
        if not sumtest(R, C, D): continue
        if lp(R, C, D) is not None and not passes(R, C, D):
            n += 1; ex.append((C, D))
print(k, h, "plain-LP-feasible parity-failing:", n, ex[:3])
