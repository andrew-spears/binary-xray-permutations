"""Which prefixes cut out the common core  C(s, l) = intersection of F(x) over legal prefixes x with slack s, last letter l ?
Prefixes of length <= K with slacks <= B, first letter > 0 (F(0x) = Sh F(x) is the same set of diagrams).
Prints |C(s, l)| and a small subfamily of prefixes with the same intersection (greedy).   Usage: python3 core_gen.py K B"""
import sys
from collections import defaultdict
from core import *
K, B = int(sys.argv[1]), int(sys.argv[2])
strip = lambda p: tuple(v for v in p if v)
fam = defaultdict(dict)
for x in legal_prefixes(K, B):
    if not x or x[0] == 0 or x[-1] > 1 or x[-1] < 0: continue
    k = len(x); S = frozenset((strip(part(a, k)), strip(part(b, k))) for a, b in Fx(x))
    fam[(sum(x), x[-1])].setdefault(S, x)          # one (shortest found) word per distinct set
name = lambda p: "".join(map(str, p)) or "-"
for (s, l) in sorted(fam):
    if s == 0: continue
    sets = fam[(s, l)]; C = frozenset.intersection(*sets); cur = None; gens = []
    while cur != C:
        best = min(sets, key=lambda S: (len(S) if cur is None else len(cur & S), len(sets[S])))
        cur = best if cur is None else cur & best; gens.append(sets[best])
    print(f"slack {s} last {l}: {len(sets)} distinct F, |C| = {len(C)}, cut out by {len(gens)}: " + "  ".join("".join(map(str, g)) for g in gens))
    if len(C) <= 8: print("      C =", " ".join(sorted(name(a) + "|" + name(b) for a, b in C)))
