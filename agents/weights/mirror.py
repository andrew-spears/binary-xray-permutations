"""Which involution of the states is the mirror?  Tests A-family = sigma(F-family) with last letter l <-> first letter -l."""
import sys
from load import *
D = Data(sys.argv[1], False)
cands = {"conjugate both": lambda t: (conj(t[0]), conj(t[1])), "swap": lambda t: (t[1], t[0]), "identity": lambda t: t,
         "conjugate + swap": lambda t: (conj(t[1]), conj(t[0]))}
for name, f in cands.items():
    ok = True
    for (s, l) in D.F:
        if (s, -l) not in D.A: ok = False; break
        p = D.sigma(s, f); A = D.sets(-1, s, -l); M = D.sets(1, s, l)
        if {r.tobytes() for r in M[:, p]} != {r.tobytes() for r in A}: ok = False; break
    print(name, ok)
