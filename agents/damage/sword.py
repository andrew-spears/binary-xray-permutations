"""Statement S along single words: start Lev<=2(s0), after each letter <= 0 print |Lev2 - reached|, |violators of Theorem D in Lev2|, and the reached-nothing extras.
python3 sword.py s0 "2 2 2 2 2 1 0" ["word" ...]"""
import sys
from oh import *
from landau_lib import viol
lev = lambda u: max(cls(u), 1 - cls(u))
s0 = int(sys.argv[1])
for word in sys.argv[2:]:
    w = tuple(map(int, word.split())); setup(s0 + sum(max(e, 0) for e in w) + 2)
    F = frozenset(u for u in states(s0) if lev(u) <= 2); s = s0
    for i, e in enumerate(w, 1):
        F = step(F, e); s += e
        if e > 0: continue
        L2 = [u for u in states(s) if lev(u) <= 2]; D = {u for u in L2 if u not in F}; V = {u for u in L2 if viol(u, w[:i])}
        assert V <= D
        print(f"s0 {s0} word {' '.join(map(str, w[:i]))}: slack {s}, Lev2 {len(L2)}, missing {len(D)}, violators {len(V)}, extra {len(D - V)}:", " ".join(sorted(nm(u) for u in D - V)[:12]))
