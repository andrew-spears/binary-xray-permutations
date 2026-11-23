"""Are the sets J(type) of blocks.py unions of classes of a finer invariant?  phi2 = (a, b) (2-core charges of lam and mu);
phi4 = 4-core charge vectors of lam and mu;  phi8 = 8-core charge vectors.  For each: number of (type, class) pairs that are split by J
(class meets J and its complement), over types with slack <= S - 2.
  python3 fine.py 2 S WIN MASK"""
import sys, runpy
from fx2 import *
g = runpy.run_path("blocks.py", run_name="__main__")
types, mask = g["types"], g["mask"]
def charges(m, p):
    W = Mo.W; out = []
    for r in range(p):
        out.append(sum(1 for k in range(0, W) if k % p == r and m >> (k + W) & 1) - sum(1 for k in range(-W, 0) if k % p == r and not m >> (k + W) & 1))
    return tuple(out)
for nm, p in (("phi2 = pair of 2-cores", 2), ("phi4 = pair of 4-cores", 4), ("phi3 = pair of 3-cores", 3), ("phi8 = pair of 8-cores", 8)):
    cls = [{} for _ in St]
    for s, L in enumerate(St):
        for i, t in enumerate(L): cls[s].setdefault((charges(t[0], p), charges(t[1], p)), []).append(i)
    split = tot = 0; ncl = [len(c) for c in cls]
    for (s, r), J in types.items():
        if s > S - 2 or not r: continue
        for key, idxs in cls[s].items():
            inm = [i for i in idxs if mask[s] >> i & 1]
            if not inm: continue
            k = sum(1 for i in inm if J >> i & 1); tot += 1; split += 0 < k < len(inm)
    print(f"{nm}: classes per slack {ncl}; split (type, class) pairs: {split} of {tot}")
print("fraction of each 4-core class inside J(type), over (type, class) with class size >= 4, slack <= S - 2:")
p = 4; cls = [{} for _ in St]
for s, L in enumerate(St):
    for i, t in enumerate(L): cls[s].setdefault((charges(t[0], p), charges(t[1], p)), []).append(i)
hist = {}
for (s, r), J in types.items():
    if s > S - 2 or not r: continue
    for key, idxs in cls[s].items():
        if len(idxs) < 4: continue
        k = sum(1 for i in idxs if J >> i & 1); f = k / len(idxs)
        b = "0" if k == 0 else "1" if k == len(idxs) else "miss 1-2" if len(idxs) - k <= 2 else "has 1-2" if k <= 2 else "middle"
        hist[b] = hist.get(b, 0) + 1
print("   ", hist)
