"""Deterministic rules for the letter 0: always take the largest (resp. smallest) admissible i.  Prints the attractors (cycles) and the
longest time to reach them.   python3 greedy.py S"""
import sys
from maya import *
conj = lambda l: tuple(sum(1 for a in l if a > j) for j in range(l[0])) if l else ()
for s in range(1, int(sys.argv[1]) + 1):
    Mo = Maya(s); L = Mo.states(s); nm = lambda t: Mo.name(t)
    for rule, pick in (("max i", -1), ("min i", 0)):
        g = {t: Mo.succ(t, 0)[pick] for t in L}        # succ lists i increasing
        cyc = {}; worst = 0
        for t in L:
            seen = {}; u = t; k = 0
            while u not in seen: seen[u] = k; u = g[u]; k += 1
            c = []; v = u
            while True:
                c.append(v); v = g[v]
                if v == u: break
            key = min(c); cyc[key] = c; worst = max(worst, seen[u])
        print(f"s {s} rule {rule}: {len(cyc)} cycles, lengths {sorted(len(c) for c in cyc.values())}, longest transient {worst}; " +
              " ; ".join(" > ".join(nm(v) for v in c) for c in list(cyc.values())[:4] if len(c) <= 6), flush=True)
