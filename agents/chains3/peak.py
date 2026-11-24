# Rule PEAK-ZERO for the extra stone.  F = valid words with no letter >= 2 before a letter <= -2 and no two-chain
# solution.  Z0: the word has a letter 0 standing between two cuts of greatest slack ("peak zero").
# Z1: some solution = two chains + the first peak zero.  Z2: ... + some peak zero.  Z3: ... + the last peak zero.
# Z4: Z2 with the stones incomparable to the extra stone being its k nearest neighbours on each side in line order.
# Z5: ... + some letter 0 in a run of zeros that has a positive letter (or the start) before it and a negative letter
#     (or the end) after it (a zero at a local peak of the slack).  Z6: ... + some stone with letter 0.
# Usage: python3 peak.py N [first n] [show]
import sys
from collections import Counter
from lib import *
import two
from extra import extras
N = int(sys.argv[1]); N0 = int(sys.argv[2]) if len(sys.argv) > 2 else 6; show = len(sys.argv) > 3
for n in range(N0, N + 1):
    tot = 0; ok = Counter(); fail = {}; ks = Counter()
    for e in words(n):
        hi = hl = False
        for x in e:
            if x >= 2: hi = True
            if x <= -2 and hi: hl = True
        if hl or two.accepts(e): continue
        tot += 1; S = [sum(e[:t]) for t in range(n + 1)]; M = max(S)
        Z = [t for t in range(n) if S[t] == M and S[t + 1] == M]; X = extras(e); P = {x[0] for x in X}
        near = [x for x in X if x[0] in Z and x[2] == list(range(x[0] - len(x[2]), x[0])) and x[3] == list(range(x[0] + 1, x[0] + 1 + len(x[3])))]
        def lp(t):
            a = t
            while a > 0 and e[a - 1] == 0: a -= 1
            b = t
            while b < n - 1 and e[b + 1] == 0: b += 1
            return (a == 0 or e[a - 1] > 0) and (b == n - 1 or e[b + 1] < 0)
        LZ = [t for t in range(n) if e[t] == 0 and lp(t)]
        r = {"Z5": bool(set(LZ) & P), "Z6": any(e[t] == 0 for t in P), "Z0": bool(Z), "Z1": bool(Z) and Z[0] in P, "Z2": bool(set(Z) & P), "Z3": bool(Z) and Z[-1] in P, "Z4": bool(near)}
        if near: ks[min(len(x[2]) for x in near)] += 1
        for k, v in r.items():
            ok[k] += v
            if not v and k not in fail: fail[k] = e
        if show and near: x = min(near, key=lambda x: len(x[2])); print(" ".join(map(str, e)), "| stone", x[0], "k", len(x[2]), "| rest", " ".join(map(str, x[4])), "|", fmt(x[5]))
    print("n %d  words of F: %d  " % (n, tot) + "  ".join("%s %d%s" % (k, ok[k], "" if ok[k] == tot else " (fails: %s)" % " ".join(map(str, fail[k]))) for k in ["Z0", "Z1", "Z2", "Z3", "Z4", "Z5", "Z6"]), " k in Z4:", dict(sorted(ks.items())))
