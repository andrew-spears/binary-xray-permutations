"""Equality cases of COUNT.  For every canonical step and every DEL0 step (delete one letter 0, result legal) on
valid nonzero words of length <= n: the ratio N(longer)/N(shorter), tabulated against the slack at the changed place
and against tight cuts (prefix sum 0 strictly inside the word) next to it.     Usage: python3 equal.py n"""
import sys
from collections import defaultdict
from fractions import Fraction
from countlib import solutions, canon
n = int(sys.argv[1]); sol = solutions(n); N = {w: len(s) for w, s in sol.items()}
def legal(w): return w in N
tab = defaultdict(lambda: [0, 0, None, []])           # steps, equalities (ratio == target), least ratio, examples
target = {"PEAK": 2, "RUN": Fraction(3, 2), "ZERO": 1, "DEL0": 1}
def note(fam, key, w, w2):
    r = Fraction(N[w], N[w2]); t = tab[(fam, key)]; t[0] += 1
    if t[2] is None or r < t[2]: t[2] = r
    if r == target[fam]:
        t[1] += 1
        if len(t[3]) < 3: t[3].append((w, N[w], w2, N[w2]))
for w in N:
    if not any(w): continue
    pre = [sum(w[:i]) for i in range(len(w) + 1)]
    name, lo, u, v = canon(w); fam = name.split("(")[0]; w2 = w[:lo] + u + w[lo + len(v):]
    note(fam, ("slack before v", pre[lo], "slack after v", pre[lo + len(v)]) if fam != "RUN" else (name,), w, w2)
    for i, e in enumerate(w):
        if e == 0 and legal(w[:i] + w[i + 1:]) and any(w[:i] + w[i + 1:]): note("DEL0", ("slack at the 0", pre[i]), w, w[:i] + w[i + 1:])
for (fam, key) in sorted(tab, key=str):
    t = tab[(fam, key)]
    print(f"{fam:5} {str(key):48} steps {t[0]:5}  ratio == {str(target[fam]):3}: {t[1]:5}  least ratio {float(t[2]):.3f}   {t[3][:2] if t[3] else ''}")
