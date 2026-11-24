"""Midpoint concavity of the solution count along a root direction?
f(mu) = #{permutations sigma : (i + sigma(i))_i is a rearrangement of mu, stones with equal sums ordered}
      = (number of boards with sum multiset mu) * prod(multiplicity!)      (mu any integer vector, sums of 0..n-1)
Tests, for every sorted mu in the support region and every pair i < j:   f(mu + a) + f(mu - a) <= 2 f(mu),  a = e_i - e_j,
and the weaker   f(mu) >= f(mu +- a) / 2   (a neighbour of a solvable vector is solvable).
Usage: python3 conc.py n"""
import sys, itertools
from math import factorial
from collections import Counter
n = int(sys.argv[1]); B = Counter()
for p in itertools.permutations(range(n)): B[tuple(sorted(i + p[i] for i in range(n)))] += 1
def f(mu):
    mu = tuple(sorted(mu)); b = B.get(mu, 0)
    if not b: return 0
    for m in Counter(mu).values(): b *= factorial(m)
    return b
def below(mu):                       # majorised by 2 rho (Landau), entries sorted increasing
    return all(sum(mu[:k]) >= k * (k - 1) for k in range(1, n + 1)) and sum(mu) == n * (n - 1)
# all sorted vectors below 2 rho
vecs = set(); todo = [tuple(2 * i for i in range(n))]; vecs.add(todo[0])
while todo:
    mu = todo.pop()
    for i in range(n):
        for j in range(i + 1, n):
            v = list(mu); v[i] += 1; v[j] -= 1; v = tuple(sorted(v))
            if v not in vecs and below(v): vecs.add(v); todo.append(v)
stat = Counter(); ex = {}
for mu in vecs:
    fm = f(mu); reg = len(set(mu)) == n
    for i in range(n):
        for j in range(i + 1, n):
            if mu[i] == mu[j] and (i > 0 and mu[i - 1] == mu[i] or j < n - 1 and mu[j + 1] == mu[j]): continue   # one pair (first, last) per pair of equal values
            up = list(mu); up[i] += 1; up[j] -= 1; dn = list(mu); dn[i] -= 1; dn[j] += 1    # mu is increasing: up moves the two entries together, dn apart
            fu, fd = f(up), f(dn)                                                           # (at a tie mu[i] = mu[j] both are the same vector)
            for name, bad in (("concave", fu + fd > 2 * fm), ("half", max(fu, fd) > 2 * fm), ("zero with a solvable inner neighbour", fm == 0 and fu > 0),
                              ("zero with a solvable neighbour", fm == 0 and max(fu, fd) > 0)):
                for cls in ("all", "regular") if reg else ("all",):
                    stat[(name, cls, "tests")] += 1
                    if bad:
                        stat[(name, cls, "fail")] += 1
                        if (name, cls) not in ex: ex[(name, cls)] = (mu, (i, j), fd, fm, fu)
print(f"n = {n}: {len(vecs)} sorted vectors below 2 rho")
for name in ("concave", "half", "zero with a solvable inner neighbour", "zero with a solvable neighbour"):
    for cls in ("all", "regular"):
        print(f"  {name:38} mu {cls:8}: {stat[(name, cls, 'fail')]:6} failures of {stat[(name, cls, 'tests')]:7}   {ex.get((name, cls), '')}")
