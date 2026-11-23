"""Criterion PAR for unimodal words.  O(x) = states with an odd number of placements of the prefix x.
A unimodal word x | y (cut after the last positive letter) is solvable if O(x) meets conj O(x'), x' = -reverse(y).
For every slack s <= S: all nonnegative-letter prefixes x (last letter 1) and x' (last letter 0, one trailing zero;
zeros never repeated, since by the parity theorem O depends only on the skew shape of x) are compared.
Usage: python3 par.py S [cap]     (cap: largest letter allowed, default no cap)"""
import sys
from collections import defaultdict
from parity import shape
S = int(sys.argv[1]); cap = int(sys.argv[2]) if len(sys.argv) > 2 else S
from par_lib import odd_states, conj
fam = defaultdict(dict)                       # (slack, last letter) -> {O(x): shortest x}
def rec(x, s):
    if x and x[-1] in (0, 1) and s >= 1:
        O = odd_states(x); fam[(s, x[-1])].setdefault(O, tuple(x))
    lo = max(x[-1] - 1, 0) if x else 1
    for e in range(lo, min(cap, S - s) + 1):
        if e == 0 and x[-1] == 0: continue
        x.append(e); rec(x, s + e); x.pop()
rec([], 0)
for s in range(1, S + 1):
    A = fam[(s, 1)]; B = fam[(s, 0)]; fails = []
    for O, x in A.items():
        for O2, x2 in B.items():
            if not any((conj(l), conj(g)) in O2 for l, g in O): fails.append((x, x2))
    common = set.intersection(*[set(O) for O in A]) if A else set()
    commonB = set.intersection(*[{(conj(l), conj(g)) for l, g in O} for O in B]) if B else set()
    print(f"slack {s}: {len(A)} distinct odd sets (last 1), {len(B)} (last 0); pairs without a common odd state: {len(fails)} of {len(A) * len(B)}"
          f"; states odd for every x and (conjugated) every x': {len(common & commonB)}")
    for x, x2 in fails[:3]: print("     e.g. x =", x, " x' =", x2)
