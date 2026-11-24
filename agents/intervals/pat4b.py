"""Families S of length-4 patterns such that every valid arrangement (all n <= N) has a solution avoiding all of S.
Board convention: sigma(row) = column, d = column - row.
usage: python3 pat4b.py N"""
import sys, itertools, pickle, os
from iv import words
N = int(sys.argv[1])
pats = list(itertools.permutations(range(4))); idx = {p: i for i, p in enumerate(pats)}
name = lambda i: ''.join(str(x + 1) for x in pats[i])
masks = {}   # (n, D) -> set of pattern masks of its solutions
for n in range(4, N + 1):
    quads = list(itertools.combinations(range(n), 4))
    for s in itertools.permutations(range(n)):
        D = tuple(sorted(s[i] - i for i in range(n)))
        if any(D[i] == D[i + 1] for i in range(n - 1)): continue
        m = 0
        for q in quads:
            v = (s[q[0]], s[q[1]], s[q[2]], s[q[3]])
            m |= 1 << idx[tuple(sum(y < x for y in v) for x in v)]
        masks.setdefault((n, D), set()).add(m)
pickle.dump(masks, open(f"masks{N}.pkl", "wb"))
def covers(S):
    return all(any(m & S == 0 for m in ms) for ms in masks.values())
good = [i for i in range(24) if covers(1 << i)]
print("single patterns that work:", " ".join(name(i) for i in good))
best = []
fam = {0}
for r in range(1, len(good) + 1):
    new = set()
    for S in fam:
        for i in good:
            if not S >> i & 1 and covers(S | 1 << i): new.add(S | 1 << i)
    if not new: break
    fam = new
    print(f"families of {r} patterns that work: {len(fam)}")
    if len(fam) <= 12:
        for S in sorted(fam): print("   ", " ".join(name(i) for i in range(24) if S >> i & 1))
