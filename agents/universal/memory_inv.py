"""Largest invariant indexed by (slack, last m letters), the candidate induction for universal states.
Type of a legal prefix (all partial sums <= B) = (end slack, last m letters); a prefix with at most m letters is its
own type.  J(type) = a set of states with J(t2) inside step_e(J(t)) for every edge t --e--> t2, J(empty word) = start.
Then J(type of x) is inside F(x) for every prefix x (induction on x), and by the reversal symmetry conj J(type of
-reverse(y)) is inside A(y).  The script computes the largest such J and reports, per slack s,
  common(0)  = states in J(t) for every type t at slack s with last letter 0,
  common(<=1)= the same with last letter <= 1,
  universal  = common(0) & conj common(<=1)            (nonempty = universal state with an inductive certificate),
  bad pairs  = pairs of types (t, t') at slack s, last letters adding to <= 1, with J(t) & conj J(t') empty
               (no bad pair = every word through slack s has a solution, with an inductive certificate).
Usage: python3 memory_inv.py B m"""
import sys
from collections import defaultdict
from maya import succ
from load import cc, nm
B, m = int(sys.argv[1]), int(sys.argv[2])

def parts(n, mx=None):
    if mx is None: mx = n
    if n == 0: yield (); return
    for a in range(min(n, mx), 0, -1):
        for p in parts(n - a, a): yield (a,) + p
lev = [[(l, mu) for i in range(s + 1) for l in parts(i) for mu in parts(s - i)] for s in range(B + 1)]
idx = [{st: i for i, st in enumerate(L)} for L in lev]
pred = defaultdict(int)                                    # (slack of c, index of c, e) -> bitmask of predecessors
for s in range(B + 1):
    for i, b in enumerate(lev[s]):
        for e in range(-s, B - s + 1):
            for c in succ(b, e): pred[(s + e, idx[s + e][c], e)] |= 1 << i

root = (0, (), True)                                       # (slack, last letters, word has at most m letters)
types, out, todo = {root}, defaultdict(list), [root]
while todo:
    t = todo.pop(); s, w, short = t
    for e in range(max(w[-1] - 1, -s) if w else 0, B - s + 1):
        w2 = w + (e,)
        t2 = (s + e, w2, True) if short and len(w2) <= m else (s + e, w2[-m:], False)
        out[t].append((e, t2))
        if t2 not in types: types.add(t2); todo.append(t2)
J = {t: (1 << len(lev[t[0]])) - 1 for t in types}; J[root] = 1
work, queued = [root], {root}
for t in types:
    if t != root: work.append(t); queued.add(t)
while work:
    t = work.pop(); queued.discard(t); Jt = J[t]
    for e, t2 in out[t]:
        s2 = t2[0]; old = J[t2]; new = 0; x = old
        while x:
            low = x & -x; i = low.bit_length() - 1; x ^= low
            if pred.get((s2, i, e), 0) & Jt: new |= low
        if new != old:
            J[t2] = new
            if t2 not in queued: work.append(t2); queued.add(t2)
def states(s, mask): return {lev[s][i] for i in range(len(lev[s])) if mask >> i & 1}
def conjmask(s, mask):
    r = 0
    for st in states(s, mask): r |= 1 << idx[s][cc(st)]
    return r
print(f"bound {B}, memory {m}: {len(types)} types")
tot = [0, 0, []]
for s in range(1, B + 1):
    ts = [t for t in types if t[0] == s and t[1]]
    full = (1 << len(lev[s])) - 1; c0 = c1 = full
    for t in ts:
        if t[1][-1] == 0: c0 &= J[t]
        if t[1][-1] <= 1: c1 &= J[t]
    U = states(s, c0 & conjmask(s, c1))
    byl = defaultdict(set)
    for t in ts: byl[t[1][-1]].add(J[t])
    cj = {l: {conjmask(s, x) for x in v} for l, v in byl.items()}
    bad = sum(1 for l in byl for l2 in cj if l + l2 <= 1 for a in byl[l] for b in cj[l2] if not a & b)
    tot[0] += sum(1 for t in ts if not J[t]); tot[1] += bad
    if not U: tot[2].append(s)
    if len(sys.argv) > 3: continue
    print(f"  slack {s:2d}: {len(ts):5d} types, {sum(1 for t in ts if not J[t]):5d} with J empty, common(0) {len(states(s, c0)):5d},"
          f" common(<=1) {len(states(s, c1)):5d}, universal {len(U):4d}, bad pairs of distinct J sets {bad:5d}  ",
          " ".join(sorted(nm(x) for x in U)[:3]))
print(f"summary: bound {B}, memory {m}: types with J empty {tot[0]}, bad pairs {tot[1]}, slacks without universal state {tot[2]}")
