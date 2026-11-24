"""DEL0 (delete a letter 0: x 0 y -> x y) and the number of holes.  h_r, h_c = number of row / column holes of the state
after x (a hole = an unused row or column among the first m, m = |x|).  For every DEL0 placement in words of length
<= n, and each statistic c of the state after x, test class by class  N_c(x y) <= N_c(x 0 y)  (solutions counted by
the class of the state after x).  Split: ZERO placements (y starts with -1) / the others.
Also tabulates what the 0-stone does: it fills a row hole (row <= m), fills a column hole (column <= m), or sits on
the main diagonal (m+1, m+1); and the change of h_r + h_c across it.      Usage: python3 del0holes.py n"""
import sys
from collections import Counter, defaultdict
from countlib import solutions, state
n = int(sys.argv[1]); sol = solutions(n)
STATS = {"h_r": lambda t: len(t[1]), "h_c": lambda t: len(t[3]), "h_r + h_c": lambda t: len(t[1]) + len(t[3]),
         "(h_r, h_c)": lambda t: (len(t[1]), len(t[3])), "min(h_r, h_c), max": lambda t: tuple(sorted((len(t[1]), len(t[3])))),
         "|h_r - h_c|": lambda t: abs(len(t[1]) - len(t[3])), "h_r - h_c": lambda t: len(t[1]) - len(t[3])}
res = defaultdict(lambda: [0, 0, None]); stone = Counter(); dh = Counter()
for w in sol:
    for m, e in enumerate(w):
        if e != 0: continue
        w2 = w[:m] + w[m + 1:]
        if w2 not in sol or not any(w2): continue
        kind = "ZERO" if m + 1 < len(w) and w[m + 1] == -1 else "other"
        tu = [state(s, m) for s in sol[w2]]; tv = [state(s, m) for s in sol[w]]
        for name, f in STATS.items():
            hu = Counter(map(f, tu)); hv = Counter(map(f, tv)); r = res[(kind, name)]; r[0] += 1
            bad = [c for c in hu if hu[c] > hv[c]]
            if bad:
                r[1] += 1
                if r[2] is None or len(w) < len(r[2][0]): r[2] = (w, m, bad[0], hu[bad[0]], hv[bad[0]])
        for s in sol[w]:
            t = state(s, m); t2 = state(s, m + 1); r0, c0 = s[m]; h = len(t[1]) + len(t[3]); h2 = len(t2[1]) + len(t2[3])
            what = "row hole" if r0 <= m else "column hole" if c0 <= m else "main diagonal"
            stone[(kind, what)] += 1; dh[(kind, what, h2 - h)] += 1
for (kind, name), (t, bad, ex) in sorted(res.items()):
    print(f"{kind:5} {name:20} placements with a violating class: {bad:5} of {t}" + (f"   e.g. {ex[0]} (0 at index {ex[1]}) class {ex[2]}: {ex[3]} > {ex[4]}" if ex else ""))
print("the 0-stone (over all solutions of x 0 y): what it fills, and the change of h_r + h_c")
for k in sorted(dh): print(f"   {k[0]:5} fills {k[1]:13} change {k[2]:+d}: {dh[k]}")
