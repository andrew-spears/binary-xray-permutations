"""Inductive form of the damage statement, letters <= 2.  Type of a prefix ending in a letter <= 0: (slack s, r = young excess BEFORE the last letter, last letter).
Family K(s, r, last) = (G(s) if last = 0 else G-(s)) minus N_r(s),  N_r(s) = {two-line deficiency <= r + C} u {-|nn, nn|-},
two-line deficiency = s - (longest row or column of lambda) - (longest row or column of mu).
Block = W 0 with W in {1,2}* ending in 1, or one letter e <= 0 (e >= last - 1).  Test: K(type') inside step_block(K(type)).
python3 ind.py SMIN SMAX RMAX [C] [show]     source slacks SMIN..SMAX, all slacks inside the block <= SMAX"""
import sys, collections
from oh import *
SMIN, SMAX, RMAX = map(int, sys.argv[1:4]); C = int(sys.argv[4]) if len(sys.argv) > 4 else 0; MODE = 1 if C >= 0 else 0; SHOW = len(sys.argv) > 5; setup(SMAX + 2)
line = lambda p: max(p[0], len(p)) if p else 0
dfc = lambda u: slack(u) - line(u[0]) - line(u[1])
def inN(u, r, last):
    lam, mu = u; s = slack(u)
    if MODE == 1: return r > 0 and (dfc(u) <= r + C or (s % 2 == 0 and u in ((( ), (s // 2, s // 2)), ((s // 2, s // 2), ()))))
    if max(lam[:1] + mu[:1] + (0,)) > s - r: return True                                  # R_r
    cap = 0
    for k in range(1, len(lam) + len(mu) + 1):                                      # C_r (depends on the last letter)
        cap += (lam[k - 1] if k <= len(lam) else 0) + (mu[k - 1] if k <= len(mu) else 0)
        if k >= 2 and cap <= k - 2 + last + min(r, k - 1) and cap < s: return True
    return False
def K(s, r, last): return frozenset(u for u in (G(s) if last == 0 else Gm(s)) if not inN(u, r, last))
def blocks(s, last):
    for e in range(0, last - 2, -1):
        if s + e >= 0: yield (e,)
    def rec(w, t):
        if w[-1] == 1: yield w + (0,)
        for e in (1, 2):
            if t + e <= SMAX: yield from rec(w + (e,), t + e)
    for e in (1, 2):
        if s + e <= SMAX: yield from rec((e,), s + e)
tot = 0; fails = collections.defaultdict(list); empt = set()
for s in range(SMIN, SMAX + 1):
    for last in range(0, -s - 1, -1):
        for r in range(0, RMAX + 1):
            F0 = K(s, r, last)
            if not F0 and s > 0: empt.add((s, r, last)); continue
            y = max(0, r + last - 1)
            for w in blocks(s, last):
                F = F0; t = s; yy = y; rr = r
                for e in w: F = step(F, e); t += e; rr = yy; yy = max(0, yy + e - 1)
                tot += 1; miss = K(t, rr, w[-1]) - F
                if miss: fails[(len(w) > 1, t >= 11)].append((s, r, last, w, t, rr, sorted(nm(u) for u in miss)))
print(f"source slack {SMIN}..{SMAX}, r <= {RMAX}, C = {C}: {tot} (type, block) pairs; empty source families skipped: {len(empt)}; failures:", {k: len(v) for k, v in fails.items()}, " key = (block has letters >= 1, target slack >= 11)")
for k, v in sorted(fails.items()):
    v.sort(key=lambda x: (len(x[6]), x[4]))
    for x in v[: 12 if SHOW else 4]: print("  ", k, "source (s, r, last)", x[:3], "block", " ".join(map(str, x[3])), "-> (s, r)", x[4:6], "missing", len(x[6]), " ".join(x[6][:10]))
