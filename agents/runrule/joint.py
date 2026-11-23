"""COUNT with the state fixed on BOTH sides of the replaced block.  For every canonical step  x u y <- x v y  of a
valid nonzero word of length <= n, classify each solution by c = (f(state after x), g(state before y)) and test
#{solutions of x u y in class c} <= #{solutions of x v y in class c} for every c.
f, g range over: row diagram, column diagram, both, size of the row diagram.      Usage: python3 joint.py n"""
import sys
from collections import Counter, defaultdict
from countlib import solutions, canon, state
n = int(sys.argv[1]); sol = solutions(n)
size = lambda ex, ho: sum(ex) - sum(ho)
F = {"row": lambda t: t[:2], "col": lambda t: t[2:], "both": lambda t: t, "|lam|": lambda t: size(t[0], t[1]), "-": lambda t: 0,
     "sizes": lambda t: (size(t[0], t[1]), size(t[2], t[3]))}
PAIRS = [("row", "row"), ("row", "col"), ("both", "-"), ("-", "both"), ("both", "|lam|"), ("|lam|", "both"), ("both", "row"), ("row", "both"),
         ("both", "both"), ("sizes", "sizes"), ("|lam|", "|lam|"), ("row", "sizes"), ("sizes", "row")]
res = defaultdict(lambda: [0, 0, None])
for w in sol:
    if not any(w): continue
    name, lo, u, v = canon(w); w2 = w[:lo] + u + w[lo + len(v):]; fam = name.split("(")[0]
    su = [(state(s, lo), state(s, lo + len(u))) for s in sol[w2]]; sv = [(state(s, lo), state(s, lo + len(v))) for s in sol[w]]
    for f, g in PAIRS:
        hu = Counter((F[f](a), F[g](b)) for a, b in su); hv = Counter((F[f](a), F[g](b)) for a, b in sv); r = res[(fam, f, g)]; r[0] += 1
        bad = [c for c in hu if hu[c] > hv[c]]
        if bad:
            r[1] += 1
            if r[2] is None or len(w) < len(r[2][0]): r[2] = (w, w2, bad[0], hu[bad[0]], hv[bad[0]])
for (fam, f, g), (t, bad, ex) in sorted(res.items()):
    print(f"{fam:5} after x: {f:6} before y: {g:6} steps with a violating class: {bad:4} of {t}" + (f"   e.g. {ex[0]} <- {ex[1]} class {ex[2]}: {ex[3]} > {ex[4]}" if ex else ""))
