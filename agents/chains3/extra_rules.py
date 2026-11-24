# Rules for the extra stone (two chains + one stone).  Family F: valid words with no letter >= 2 before a letter <= -2
# and without a two-chain solution.  For each word: P = set of positions (line order) that can be the extra stone,
# and the least number of stones incomparable to the extra stone.
# Usage: python3 extra_rules.py N
import sys
from collections import Counter
from lib import *
import two
from extra import extras
N = int(sys.argv[1])
for n in range(6, N + 1):
    tot = 0; none = []; fail = {}; mininc = Counter(); ok = Counter()
    for e in words(n):
        hi = False; hl = False
        for x in e:
            if x >= 2: hi = True
            if x <= -2 and hi: hl = True
        if hl or two.accepts(e): continue
        tot += 1; X = extras(e)
        if not X: none.append(e); continue
        P = {x[0] for x in X}; mininc[min(len(x[2]) + len(x[3]) for x in X)] += 1
        rules = {"first or last line": bool(P & {0, n - 1}),
                 "a stone with letter 0": any(x[1] == 0 for x in X),
                 "at most 2 incomparable stones": any(len(x[2]) + len(x[3]) <= 2 for x in X),
                 "at most 3 incomparable stones": any(len(x[2]) + len(x[3]) <= 3 for x in X),
                 "largest letter (first such)": e.index(max(e)) in P,
                 "a stone next to a cut of least slack": any(i in P or i - 1 in P for i in range(1, n) if sum(e[:i]) == min(sum(e[:t]) for t in range(1, n))),
                 "a stone next to a cut of greatest slack": any(i in P or i - 1 in P for i in range(1, n) if sum(e[:i]) == max(sum(e[:t]) for t in range(1, n)))}
        for k, v in rules.items():
            ok[k] += v
            if not v and k not in fail: fail[k] = e
    print("n %d: words of F %d, of which not two chains + one stone: %d %s; least number of incomparable stones: %s" % (n, tot, len(none), none[:1], dict(sorted(mininc.items()))))
    for k in ok: print("     %-42s holds for %d of %d   first failure %s" % (k, ok[k], tot, fail.get(k, "-")))
