import itertools, sys
from collections import defaultdict

def witnesses_by_D(n):
    W = defaultdict(list)
    for p in itertools.permutations(range(n)):
        ds = [p[i]-i for i in range(n)]
        if len(set(ds)) == n:
            W[frozenset(ds)].append(p)
    return W

def realizable_on_board(rows, cols, D):
    # rows, cols: lists; D: set of diagonals; need bijection rows->cols using each d once
    D = sorted(D)
    def rec(i, usedc, usedd):
        if i == len(rows): return True
        r = rows[i]
        for c in cols:
            if c in usedc: continue
            d = c - r
            if d in D and d not in usedd:
                if rec(i+1, usedc|{c}, usedd|{d}): return True
        return False
    return rec(0, frozenset(), frozenset())

# 1. families
print("pm{1..a}:", [realizable_on_board(list(range(2*a)), list(range(2*a)), set(range(1,a+1))|set(range(-a,0))) for a in range(1,7)])
for k in range(3,7):
    N = 2*k-2
    res = []
    for m in range(1,k+1):
        D = set(range(-k,k+1)) - {0,m,-m}
        res.append((m, realizable_on_board(list(range(N)), list(range(N)), D)))
    print("k",k,"N",N,res)

# 2. repair radius
def repair_radius(n):
    W = witnesses_by_D(n)
    worst = 0
    for D, wl in W.items():
        Ds = sorted(D)
        for a, b in zip(Ds, Ds[1:]):
            if b - a == 3:
                D2 = (D - {a, b}) | {a+1, b-1}
                wl2 = W.get(frozenset(D2), [])
                assert wl2, "unreachable?"
                # row of stone on diagonal d: rowmap[d]
                rm2 = [{p[i]-i: i for i in range(n)} for p in wl2]
                for p in wl:
                    rm = {p[i]-i: i for i in range(n)}
                    best = min(sum(1 for d in D if d not in (a, b) and rm[d] != r2[d]) for r2 in rm2)
                    worst = max(worst, best)
    return worst

for n in range(4, int(sys.argv[1]) + 1):
    print("n", n, "max repair radius", repair_radius(n))
