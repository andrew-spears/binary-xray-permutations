import sys
from oh import *
SM = int(sys.argv[1]); setup(SM + 2)
All = lambda s: frozenset(states(s))
for arg in sys.argv[2:]:
    s0, W = arg.split(":"); s0 = int(s0); W = tuple(map(int, W.split()))
    s = s0 + sum(W); fam = Gm if W[-1] < 0 else G
    D = fam(s) - run(G(s0), W); L = fam(s) - run(All(s0), W); LC = fam(s) - run(Cen(s0), W)
    print(arg, "slack", s, "|D| |Loc| |LocCen|", len(D), len(L), len(LC), " D - Loc:", " ".join(sorted(nm(u) for u in D - L)), " LocCen - Loc:", " ".join(sorted(nm(u) for u in LC - L)))
