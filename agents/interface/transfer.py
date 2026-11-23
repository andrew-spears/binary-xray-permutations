"""Transfer graph X(c): c = multiset of n targets r'+c with total n(n+1)+1.  States = permutation matrices on [n]^2
with a marked stone, sums with the marked one raised by 1 equal to c.  The label of a state is the target of the
marked stone.  X(c) is the disjoint union over labels v of the witnesses of c - delta_v.
For every c = D + delta_i (D valid, distinct) report how the labels are spread over the components.
Usage: python3 transfer.py n [-v]"""
import sys
from itertools import permutations
from collections import Counter, defaultdict
n = int(sys.argv[1]); V = "-v" in sys.argv
def valid(N):
    def rec(pre, sig):
        k = len(pre)
        if k == N:
            if sig == 0: yield tuple(pre)
            return
        lo = pre[-1] - 1 if pre else 0
        for e in range(max(lo, -sig), N):
            pre.append(e); yield from rec(pre, sig + e); pre.pop()
    yield from rec([], 0)
bysum = defaultdict(list)
for p in permutations(range(1, n + 1)):
    bysum[tuple(sorted(i + 1 + p[i] for i in range(n)))].append(p)
def R(st):
    p, m = st
    if m == n - 1: return None
    q = list(p); q[m], q[m + 1] = q[m + 1], q[m]; return (tuple(q), m)
def C(st):
    p, m = st; c = p[m]
    if c == n: return None
    q = list(p); j = q.index(c + 1); q[m], q[j] = c + 1, c; return (tuple(q), j)
seen_c = set(); stats = Counter(); ex = {}
for e in valid(n):
    b = [2 * k + e[k - 1] for k in range(1, n + 1)]
    for i in range(n):
        c = b[:]; c[i] += 1; c = tuple(sorted(c))
        if c in seen_c: continue
        seen_c.add(c)
        X = {}
        for v in set(c):
            lst = list(c); lst.remove(v); lst.append(v - 1); key = tuple(sorted(lst))
            for p in bysum.get(key, []):
                for m in range(n):
                    if m + 1 + p[m] == v - 1: X[(p, m)] = v
        labels = set(X.values()); done = set(); comps = []
        for s in X:
            if s in done: continue
            comp = {s}; stack = [s]; end = False
            while stack:
                x = stack.pop()
                for t in (R(x), C(x)):
                    if t is None: end = True
                    elif t not in comp: comp.add(t); stack.append(t)
            done |= comp; comps.append((end, frozenset(X[x] for x in comp), len(comp)))
        stats["c"] += 1
        full = [cp for cp in comps if cp[1] == labels]
        if not full: stats["no component sees all labels"] += 1; ex.setdefault("nofull", (c, sorted(labels), [(a, sorted(l), k) for a, l, k in comps]))
        if all(cp[1] == labels for cp in comps): stats["every component sees all labels"] += 1
        if any(cp[1] != labels for cp in comps if cp[0]): stats["some path misses a label"] += 1; ex.setdefault("pathmiss", (c, sorted(labels), [(a, sorted(l), k) for a, l, k in comps]))
        if len(comps) == 1: stats["connected"] += 1
        stats["components"] += len(comps); stats["cycles"] += sum(1 for cp in comps if not cp[0])
print(n, dict(stats))
if V:
    for k, v in ex.items(): print(k, v)
