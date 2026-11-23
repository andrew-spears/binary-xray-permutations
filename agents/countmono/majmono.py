"""Is the number of solutions N(D) monotone along the slack order at fixed n?
Slack profile sigma(D) = (sigma_1, ..., sigma_{n-1}).  Tests, for all valid D of size n:
  (a) sigma(D) <= sigma(D') pointwise  =>  N(D) <= N(D') ?
  (b) the same only for D' = D with two stones moved one step towards each other (one 'transfer').
  (c) the same only for minimal moves (AGENTS.md: a+1 and b-1 empty, every mark between them occupied).
Usage: python3 majmono.py n"""
import sys, itertools
from collections import Counter
n = int(sys.argv[1])
N = Counter()
for p in itertools.permutations(range(n)):
    d = tuple(sorted(p[i] - i for i in range(n)))
    if len(set(d)) == n: N[d] += 1
def prof(d):
    s = 0; out = []
    for k in range(n): s += d[k] + n - 1 - k - k; out.append(s)
    return tuple(out)
def valid(d):
    p = prof(d); return all(x >= 0 for x in p) and p[-1] == 0
allD = [d for d in itertools.combinations(range(-(n - 1), n), n) if valid(d)]
print(f"n = {n}: {len(allD)} valid D, {sum(1 for d in allD if N[d] == 0)} without solution")
P = {d: prof(d) for d in allD}
bad = tot = 0; ex = None
for d in allD:
    for d2 in allD:
        if d != d2 and all(a <= b for a, b in zip(P[d], P[d2])):
            tot += 1
            if N[d] > N[d2]:
                bad += 1
                if ex is None or sum(P[d2]) - sum(P[d]) < ex[0]: ex = (sum(P[d2]) - sum(P[d]), d, N[d], d2, N[d2])
print(f"(a) comparable pairs {tot}, violations {bad}", ex or "")
bad = tot = 0; ex = None
S = set(allD)
for d in allD:
    ds = set(d)
    for a in d:
        for b in d:
            if a < b and a + 1 not in ds and b - 1 not in ds and b - a >= 3:
                d2 = tuple(sorted((ds - {a, b}) | {a + 1, b - 1}))
                if d2 in S:
                    tot += 1
                    if N[d] > N[d2]:
                        bad += 1
                        if ex is None: ex = (d, N[d], d2, N[d2])
print(f"(b) transfers {tot}, violations {bad}", ex or "")
bad = tot = 0; ex = None; ratio = None
for d in allD:
    ds = set(d)
    for a in d:
        for b in d:
            if a < b and b - a >= 3 and a + 1 not in ds and b - 1 not in ds and all(m in ds for m in range(a + 2, b - 1)):
                d2 = tuple(sorted((ds - {a, b}) | {a + 1, b - 1}))
                tot += 1
                r = N[d2] / N[d] if N[d] else None
                if r is not None and (ratio is None or r < ratio[0]): ratio = (r, d, N[d], d2, N[d2])
                if N[d] > N[d2]:
                    bad += 1
                    if ex is None: ex = (d, N[d], d2, N[d2])
print(f"(c) minimal moves {tot}, violations {bad}", ex or "", "least ratio", ratio)
