"""Unreachable states that pass the plain LP: which of them pass the mod-m test (m = 2 is the parity test of card `parity`)?
mod-m test: choose for every sum the residue mod m of its row (numbers matching the rows and columns), then the LP on the
allowed cells must be feasible.  All legal prefixes of length <= K with slacks <= B.   Usage: python3 exact2.py K B"""
import sys
from core import *
from lp import lp, plp
K, B = int(sys.argv[1]), int(sys.argv[2])
n = pairs = unr = 0; surv = {2: [], 3: [], 4: [], "2 and 3": []}
for x in legal_prefixes(K, B):
    if not x: continue
    k, s, T = len(x), sum(x), sums(x); Fs = Fx(x)
    for a in all_states(k, s):
        pairs += 1
        if a in Fs: continue
        unr += 1
        if not lp(a[0], a[1], T): continue
        n += 1; e = (x, bits(a[0]), bits(a[1])); ok = {m: plp(a[0], a[1], T, m) for m in (2, 3)}
        for m in (2, 3):
            if ok[m]: surv[m].append(e)
        if ok[2] and plp(a[0], a[1], T, 4): surv[4].append(e)
        if ok[2] and ok[3]: surv["2 and 3"].append(e)
print(f"K = {K}, B = {B}: {pairs} (prefix, state) pairs, {unr} unreachable, of these LP-feasible: {n}")
for m, l in surv.items():
    print(f"   pass the mod-{m} test: {len(l)}" + (f"; first: {min(l, key=lambda e: (len(e[0]), sum(e[0])))}" if l else ""))
