"""Largest step-closed type system for letters <= 2, type = (slack, y, tail), y' = max(0, y + e - 1), tail = last letter, with the letter before it if that is not smaller (REPORT3 'y A1').
J(type) = greatest family with J(type') inside step_e(J(type)) for every transition; J(start) = {vacuum}.  Prints, per type, J by level and what of G / G- is missing.
python3 ty.py B [show]"""
import sys, collections, pickle, os
from oh import *
B = int(sys.argv[1]); SHOW = len(sys.argv) > 2; setup(B + 2)
SUCC = {}
def st(F, e):
    out = set()
    for t in F:
        k = (t, e)
        if k not in SUCC: SUCC[k] = tuple(succ(t, e))
        out.update(SUCC[k])
    return frozenset(out)
start = (0, 0, ()); types = {start}; trans = collections.defaultdict(list); todo = [start]
while todo:
    t = todo.pop(); s, y, tl = t; l = tl[-1] if tl else 0
    for e in range(2, -B - 1, -1):
        if e < l - 1 or s + e < 0 or s + e > B: continue
        t2 = (s + e, max(0, y + e - 1), (l, e) if tl and l >= e else (e,)); trans[t2].append((t, e))
        if t2 not in types: types.add(t2); todo.append(t2)
J = {t: frozenset(states(t[0])) for t in types}; J[start] = frozenset([((), ())])
order = sorted(types - {start}, key=lambda t: (t[0], t[1], t[2]))
it = 0
while True:
    ch = 0; it += 1
    for t in order:
        new = J[t]
        for (p, e) in trans[t]: new = new & st(J[p], e)
        if new != J[t]: J[t] = new; ch += 1
    print("iteration", it, "changed", ch, file=sys.stderr)
    if not ch: break
empty = sorted(t for t in types if not J[t])
print(f"bound {B}: {len(types)} types, empty families: {len(empty)} {empty[:5]}")
pickle.dump(J, open(f"ty{B}.pkl", "wb"))
lev = lambda u: max(cls(u), 1 - cls(u))
def dfc(u):                                     # two-line deficiency: slack - longest line of lambda - longest line of mu
    return slack(u) - sum(max(p[0], len(p)) for p in u if p)
for t in order:
    s, y, tl = t; l = tl[-1]
    if s < 4 or l < -2: continue
    al = collections.Counter(lev(u) for u in states(s)); got = collections.Counter(lev(u) for u in J[t])
    fam = Gm(s) if l < 0 else G(s); miss = sorted(fam - J[t], key=lambda u: (dfc(u), nm(u)))
    print(t, " ".join(f"L{k} {got[k]}/{al[k]}" for k in sorted(al)), f"| G or G- missing {len(miss)}", "deficiency:count", dict(sorted(collections.Counter(dfc(u) for u in miss).items())),
          (" ".join(nm(u) for u in miss[:30]) if SHOW else ""))
