"""analyze.py: read raw_n.txt (from blocks.c) and print counts + rule tests.
Usage: python3 analyze.py NMAX > analysis.txt"""
import sys

def load(n):
    rows = {}
    for line in open(f"raw_{n}.txt"):
        v = list(map(int, line.split()))
        mask = v[0]
        D = tuple(m - (n - 1) for m in range(2 * n - 1) if mask >> m & 1)
        rows[D] = dict(nwit=v[1], flags=v[2], W2=v[3], Wm=v[4], Wo=v[5], Wf=v[6], Wc=v[7], Wok=v[8], We=v[9])
    return rows

def tight(D):
    n = len(D); t = 0
    for k in range(1, n):
        t += D[k - 1] + n - k
        if t == k * (k - 1) // 2:
            return True
    return False

def xs(mask, n):  # lower stones x of pairs in mask
    return [m - (n - 1) for m in range(2 * n - 1) if mask >> m & 1]

def canon(D):
    return D <= tuple(sorted(-d for d in D))

NMAX = int(sys.argv[1])
data = {n: load(n) for n in range(2, NMAX + 1)}
F = ["has2", "two_disj2", "has3", "has132/213", "has321", "c2_direct", "c2_tight", "c2_distinct",
     "c3_dir|tight", "cany_dir|tight", "c2_dir|tight", "wit_directsum"]
print("== Q1 counts (valid no-tight-cut D, mirror-reduced) ==")
print("n  #D  " + " ".join(F) + "  Wmerge Woneside Wfar Wcorner")
nonhave = {}
for n in range(3, NMAX + 1):
    Ds = [D for D in data[n] if not tight(D) and canon(D)]
    cnt = [0] * len(F); cm = co = cf = cc = 0
    nonhave[n] = []
    for D in Ds:
        r = data[n][D]
        for b in range(len(F)):
            if r["flags"] >> b & 1: cnt[b] += 1
        ce = locals().get("ce",0); ce += r["We"] != 0; cm += r["Wm"] != 0; co += r["Wo"] != 0; cf += r["Wf"] != 0; cc += r["Wc"] != 0
        if not r["flags"] & 1: nonhave[n].append(D)
    print(n, len(Ds), " ".join(map(str, cnt)), cm, co, cf, cc, "Wext", ce); ce = 0
print("D with no 2-block in any witness:")
for n in nonhave:
    print(" ", n, nonhave[n][:6], len(nonhave[n]))

# ---- Q2: rules, over ALL no-tight-cut D (no mirror reduction) that have a 2-block
print("\n== Q2 rule tests (all no-tight-cut D with a 2-block, both mirrors) ==")
def realized(n, D):
    return n in data and D in data[n]
def merge(D, x):
    return tuple(sorted([d for d in D if d not in (x, x + 2)] + [x + 1]))

rules = {}
def rule(name):
    def deco(f): rules[name] = f; return f
    return deco
# each rule returns (list of predicted x, mode) mode 'any' or 'all'
def pairs(D): S = set(D); return [x for x in D if x + 2 in S]
for mode in ("any", "all", "left", "right"):
    def mk(sel, mode=mode):
        def f(D, n):
            P = sel(D, n)
            if mode == "left": P = P[:1]
            if mode == "right": P = P[-1:]
            return P, ("all" if mode in ("all", "left", "right") else "any")
        return f
    rules[f"empty_mid[{mode}]"] = mk(lambda D, n: [x for x in pairs(D) if x + 1 not in D])
    rules[f"adj_empty_outer[{mode}]"] = mk(lambda D, n: [x for x in pairs(D) if x - 1 not in D and x + 3 not in D])
    rules[f"adj_empty_each[{mode}]"] = mk(lambda D, n: [x for x in pairs(D) if (x - 1 not in D or x + 1 not in D) and (x + 1 not in D or x + 3 not in D)])
    rules[f"merge_valid[{mode}]"] = mk(lambda D, n: [x for x in pairs(D) if x + 1 not in D and realized(n - 1, merge(D, x))])
    rules[f"merge_valid_notight[{mode}]"] = mk(lambda D, n: [x for x in pairs(D) if x + 1 not in D and realized(n - 1, merge(D, x)) and not tight(merge(D, x))])
def closest(D, n):
    P = pairs(D)
    if not P: return []
    b = min(abs(x + 1) for x in P); return [x for x in P if abs(x + 1) == b]
rules["closest_mid[any]"] = lambda D, n: (closest(D, n), "any")
rules["closest_mid[all]"] = lambda D, n: (closest(D, n), "all")
rules["leftmost"] = lambda D, n: (pairs(D)[:1], "all")
rules["rightmost"] = lambda D, n: (pairs(D)[-1:], "all")
rules["any_pair"] = lambda D, n: (pairs(D), "any")
rules["all_pairs"] = lambda D, n: (pairs(D), "all")

for target in ("W2", "Wok", "We"):
    print(f"-- target set = {target}")
    for name, f in rules.items():
        tot = ok = 0; first = None
        for n in range(3, NMAX + 1):
            for D, r in sorted(data[n].items()):
                if tight(D) or not r["flags"] & 1: continue
                W = set(xs(r[target], n))
                P, mode = f(D, n)
                good = bool(P) and (any(x in W for x in P) if mode == "any" else all(x in W for x in P))
                tot += 1; ok += good
                if not good and first is None: first = (n, D, P, sorted(W))
        print(f"  {name:28s} {ok}/{tot} ({100*ok/tot:.1f}%) first fail: {first}")

# merge validity facts
print("\n== merge D' = D\\{x,x+2} u {x+1} facts (pairs with x+1 empty), no-tight-cut D with 2-block ==")
st = dict(pairs=0, valid=0, inW=0, valid_inW=0, valid_notW=0, inW_notvalid=0, inWm=0, Wm_notvalid=0, valid_notight=0)
ex = {}
for n in range(3, NMAX + 1):
    for D, r in sorted(data[n].items()):
        if tight(D): continue
        W = set(xs(r["W2"], n)); Wm = set(xs(r["Wm"], n))
        for x in pairs(D):
            if x + 1 in D: continue
            Dp = merge(D, x); v = realized(n - 1, Dp)
            st["pairs"] += 1; st["valid"] += v; st["inW"] += x in W; st["inWm"] += x in Wm
            st["valid_notight"] += v and not tight(Dp)
            if v and x in W: st["valid_inW"] += 1
            if v and x not in W: st["valid_notW"] += 1; ex.setdefault("valid_notW", (n, D, x))
            if not v and x in W: st["inW_notvalid"] += 1; ex.setdefault("inW_notvalid", (n, D, x))
            if x in Wm and not v: st["Wm_notvalid"] += 1
print(st); print(ex)
# pairs in W with centre occupied
c_occ = c_tot = 0
for n in range(3, NMAX + 1):
    for D, r in data[n].items():
        if tight(D): continue
        for x in xs(r["W2"], n):
            c_tot += 1; c_occ += (x + 1 in D)
print(f"2-block pairs (D,x) with centre x+1 occupied: {c_occ}/{c_tot}")
