"""Bounded letters |e_k| <= c: how many different reachable sets of interface states are there per summary
(sigma, last letter)?  Explores all prefixes of length <= N with no tight cut (no slack bound).  A prefix that
returns to slack 0 is dropped: its interface is empty again, so its extensions repeat the sets of shorter prefixes.
The per-length counts therefore do not include prefixes with a tight cut.
Usage: python3 letters_dfa.py c N"""
import sys
from collections import defaultdict
c = int(sys.argv[1]); N = int(sys.argv[2]); W = N + c + 2
base = (1 << W) - 1
def step(S, e):
    T = set()
    for rm, cm in S:
        for u in range(-W, W):
            if rm >> (W + u) & 1: continue
            v = e - u
            if v < -W or v >= W or cm >> (W + v) & 1: continue
            r2 = rm | 1 << (W + u); c2 = cm | 1 << (W + v)
            if r2 & c2 & 1: T.add((r2 >> 1, c2 >> 1))
    return frozenset(T)
def part(mask):
    xs = sorted((j - W + 1 for j in range(2 * W) if mask >> j & 1), reverse=True)
    return tuple(x + i for i, x in enumerate(xs) if x + i > 0)
start = (0, None, frozenset([(base, base)]))
level = {start}; sets = defaultdict(set); dead = 0
for k in range(N):
    nxt = set()
    for sig, ep, S in level:
        lo = 0 if ep is None else ep - 1
        for e in range(max(lo, -c, -sig), c + 1):
            if sig + e == 0:
                if sig and not step(S, e): dead += 1
                continue
            T = step(S, e)
            if not T: dead += 1
            nxt.add((sig + e, e, T)); sets[(sig + e, e)].add(T)
    level = nxt
    print(f"length {k+1}: {len(level)} distinct (sigma, e, set); dead {dead}", flush=True)
if __name__ == "__main__":
    for key in sorted(sets):
        fam = sets[key]; inter = frozenset.intersection(*fam); uni = frozenset.union(*fam)
        if key[0] <= 6: print(key, "sets:", len(fam), "sizes", sorted(len(x) for x in fam)[:8], "intersection", len(inter), "union", len(uni))
