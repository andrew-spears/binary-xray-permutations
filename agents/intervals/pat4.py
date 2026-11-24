"""For each pattern of length 4: how many valid arrangements have a solution avoiding it (board: sigma(row) = column, d = column - row).
usage: python3 pat4.py n"""
import sys, itertools
from iv import words
N = int(sys.argv[1])
pats = list(itertools.permutations(range(4)))
pid = {}
for a in range(4):
    for b in range(4):
        for c in range(4):
            for d in range(4): pass
def patt(t):
    s = sorted(t); return tuple(s.index(x) for x in t)
for n in range(4, N + 1):
    valid = set(tuple(w[k] + 2 * (k + 1) - n - 1 for k in range(n)) for w in words(n))
    got = {p: set() for p in pats}
    quads = list(itertools.combinations(range(n), 4))
    for s in itertools.permutations(range(n)):
        D = tuple(sorted(s[i] - i for i in range(n)))
        if any(D[i] == D[i + 1] for i in range(n - 1)): continue
        has = set()
        for q in quads:
            v = (s[q[0]], s[q[1]], s[q[2]], s[q[3]])
            # rank pattern
            has.add(tuple(sum(y < x for y in v) for x in v))
            if len(has) == 24: break
        for p in pats:
            if p not in has: got[p].add(D)
    res = sorted(((len(got[p]), ''.join(str(x + 1) for x in p)) for p in pats), reverse=True)
    print(f"n = {n}: {len(valid)} valid;", " ".join(f"{p}:{c}" for c, p in res))
