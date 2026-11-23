"""COUNT on the canonical shortening step, by brute force over permutations (no interface machine, no slack bound):
for every valid nonzero word w of length n <= nmax, N(shorten(w)) <= N(w), where shorten is the PEAK / ZERO / RUN
step of agents/interface/run_rule.py and N = number of permutation matrices.   Usage: python3 canon.py nmax"""
import os, sys, itertools
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "interface"))
from run_rule import shorten
nmax = int(sys.argv[1]); N = {}
for n in range(1, nmax + 1):
    c = Counter()
    for p in itertools.permutations(range(n)):
        d = sorted(p[i] - i for i in range(n))
        if all(d[i] < d[i + 1] for i in range(n - 1)):
            c[tuple(d[k] + n - 1 - 2 * k for k in range(n))] += 1      # the word e_1 .. e_n
    N[n] = c
    if n == 1: continue
    stats = {}
    for w, cnt in c.items():
        if not any(w): continue
        u, name = shorten(w); name = name.split("(")[0]
        r = cnt / N[len(u)].get(u, 0) if N[len(u)].get(u, 0) else float("inf")
        t = stats.setdefault(name, [0, 0, None]); t[0] += 1; t[1] += r < 1
        if t[2] is None or r < t[2][0]: t[2] = (r, u, w)
    unsolved = 0
    print(f"n = {n}: {len(c)} solvable words;", "; ".join(f"{k}: {v[0]} steps, {v[1]} violations, least ratio {v[2][0]:.3g}" for k, v in sorted(stats.items())), flush=True)
