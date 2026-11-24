"""COUNT class by class.  For every canonical step w' = x u y  <-  w = x v y (w valid nonzero, length <= n) and a
statistic c of the interface state t, compare the histograms over solutions:
   left cut : t = state after x      (common L_x):  #{sol of xuy, c(t) = c} <= #{sol of xvy, c(t) = c} ?
   right cut: t = state before y     (common R_y):  same question.
Also the cuts one letter earlier (left-1) and one letter later (right+1).
Prints, per rule family, cut and statistic, the number of steps where some class has more solutions of the shorter word.
Usage: python3 refine.py n"""
import sys
from collections import Counter, defaultdict
from countlib import solutions, canon, state
n = int(sys.argv[1]); sol = solutions(n)
def size(ex, ho): return sum(ex) - sum(ho)          # number of cells of the Young diagram
STATS = {
    "full state":            lambda t: t,
    "row side only":         lambda t: t[:2],
    "(|lam|, |mu|)":         lambda t: (size(t[0], t[1]), size(t[2], t[3])),
    "{|lam|, |mu|}":         lambda t: tuple(sorted((size(t[0], t[1]), size(t[2], t[3])))),
    "(#row holes, #col holes)": lambda t: (len(t[1]), len(t[3])),
    "#row holes + #col holes":  lambda t: len(t[1]) + len(t[3]),
    "(lam_1, mu_1) top extras": lambda t: (max(t[0], default=0), max(t[2], default=0)),
    "lowest holes":          lambda t: (min(t[1], default=1), min(t[3], default=1)),
    "|lam| only":            lambda t: size(t[0], t[1]),
    "#row holes only":       lambda t: len(t[1]),
    "none (COUNT itself)":   lambda t: 0,
    "sizes and hole counts": lambda t: (size(t[0], t[1]), size(t[2], t[3]), len(t[1]), len(t[3])),
}
res = defaultdict(lambda: [0, 0, None]); steps = Counter()
for w in sol:
    if not any(w): continue
    name, lo, u, v = canon(w); w2 = w[:lo] + u + w[lo + len(v):]; fam = name.split("(")[0]; steps[fam] += 1
    cuts = [("left", lo, lo), ("right", lo + len(u), lo + len(v))]
    if lo >= 1: cuts.append(("left-1", lo - 1, lo - 1))                 # one letter earlier / later
    if lo + len(v) < len(w): cuts.append(("right+1", lo + len(u) + 1, lo + len(v) + 1))
    for cut, mu, mv in cuts:
        tu = [state(s, mu) for s in sol[w2]]; tv = [state(s, mv) for s in sol[w]]
        for sname, f in STATS.items():
            hu = Counter(map(f, tu)); hv = Counter(map(f, tv)); r = res[(fam, cut, sname)]; r[0] += 1
            bad = [c for c in hu if hu[c] > hv[c]]
            if bad:
                r[1] += 1
                if r[2] is None or len(w) < len(r[2][0]): r[2] = (w, w2, bad[0], hu[bad[0]], hv[bad[0]])
print(f"canonical steps of valid nonzero words of length <= {n}:", dict(steps))
for (fam, cut, sname), (t, bad, ex) in sorted(res.items()):
    print(f"{fam:5} {cut:7} {sname:26} steps with a violating class: {bad:5} of {t}" + (f"   e.g. {ex[0]} <- {ex[1]} class {ex[2]}: {ex[3]} > {ex[4]}" if ex else ""))
