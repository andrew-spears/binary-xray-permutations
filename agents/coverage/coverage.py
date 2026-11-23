"""Coverage table of known constructions over valid no-tight-cut D, n <= NMAX, up to mirror.
Usage: python3 coverage.py [NMAX]  -> prints table, writes uncovered_<n>.txt
"""
import sys, pickle
from itertools import combinations
from common import *

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 12

valid = {n: enum_valid(n) for n in range(1, NMAX + 1)}
validset = {n: set(v) for n, v in valid.items()}

# witness-based base constructions
aff_small, aff_wide, invol, band = {}, {}, {}, {}
for n in range(1, NMAX + 1):
    s1 = {}
    for M, a, b, p in affine_perms(n, sorted({n, n + 1, 2 * n + 1})):
        s1.setdefault(diags(p), (M, a, b, p))
    s2 = dict(s1)
    for M, a, b, p in affine_perms(n, range(n, 3 * n + 2)):
        s2.setdefault(diags(p), (M, a, b, p))
    aff_small[n], aff_wide[n] = s1, s2
    band[n] = {D for D in band_sets(n) if D in validset[n] and find_witness(D, n)}
    invol[n] = set()
    for D in valid[n]:
        if all(-d in D for d in D) and find_witness(D, n, involution=True):
            invol[n].add(D)


def fixed_ok(D, n):
    return 0 in D and is_valid([d for d in D if d != 0], n - 1)


def dsum_splits(D, n):
    for n1 in range(1, n // 2 + 1):
        for D1 in combinations(D, n1):
            if sum(D1) != 0:
                continue
            D2 = tuple(d for d in D if d not in D1)
            if is_valid(D1, n1) and is_valid(D2, n - n1):
                yield D1, D2


def base_witness(D, n):
    return D in invol[n] or D in aff_wide[n] or D in band[n]


memo = {}


def solved(D, n):
    key = (D, n)
    if key in memo:
        return memo[key]
    memo[key] = False
    r = False
    if n == 1:
        r = True
    else:
        tc = tight_cuts(D, n)
        if tc:
            k = tc[0]
            lo = tuple(d + (n - k) for d in D[:k])
            hi = tuple(d - k for d in D[k:])
            r = solved(lo, k) and solved(hi, n - k)
        else:
            r = base_witness(D, n)
            if not r and fixed_ok(D, n):
                r = solved(tuple(d for d in D if d != 0), n - 1)
            if not r:
                for D1, D2 in dsum_splits(D, n):
                    if solved(D1, len(D1)) and solved(D2, len(D2)):
                        r = True
                        break
    memo[key] = r
    return r


cols = ["n", "#D", "fixpt", "dsum", "invol", "aff{n,n+1,2n+1}", "aff M<=3n+1", "band", "union", "recursive", "uncov"]
print(" | ".join(cols))
for n in range(2, NMAX + 1):
    reps = sorted({canon(D) for D in valid[n] if not tight_cuts(D, n)})
    def cov(pred):
        # a mirror class is covered if D or -D satisfies pred
        return sum(1 for D in reps if pred(D) or pred(tuple(sorted(-d for d in D))))
    c_fix = cov(lambda D: fixed_ok(D, n))
    c_ds = cov(lambda D: next(dsum_splits(D, n), None) is not None)
    c_inv = cov(lambda D: D in invol[n])
    c_a1 = cov(lambda D: D in aff_small[n])
    c_a2 = cov(lambda D: D in aff_wide[n])
    c_b = cov(lambda D: D in band[n])
    c_u = cov(lambda D: fixed_ok(D, n) or next(dsum_splits(D, n), None) is not None
              or D in invol[n] or D in aff_wide[n] or D in band[n])
    unc = [D for D in reps if not (solved(D, n) or solved(tuple(sorted(-d for d in D)), n))]
    print(" | ".join(map(str, [n, len(reps), c_fix, c_ds, c_inv, c_a1, c_a2, c_b, c_u, len(reps) - len(unc), len(unc)])), flush=True)
    with open(f"uncovered_{n}.txt", "w") as f:
        for D in unc:
            f.write(f"{list(D)}  s={scores(D, n)}\n")
