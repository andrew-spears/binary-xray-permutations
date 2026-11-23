"""Coverage closure adding inflations of simple permutations (block permutation tau[B1..Bk]).
A witness tau[B1..Bk] with blocks of sizes n_1..n_k has diagonal set  U_i (D_i + off_i),
off_i = (column start of block i) - (row start of block i), D_i valid at size n_i.
Rules: base witnesses (involution / affine M<=3n+1 / band), skew split (tight cut),
direct sum (= inflation of 12, includes fixed point), plus inflation of each tau in PATTERNS.
Usage: python3 inflation.py NMAX [patterns...]   e.g. 2413 3142
"""
import sys
from itertools import combinations, permutations
from common import *

NMAX = int(sys.argv[1])
PATTERNS = [tuple(int(c) for c in s) for s in sys.argv[2:]]

def simple_perms(k):
    out = []
    for t in permutations(range(1, k + 1)):
        ok = True
        for i in range(k):
            for j in range(i + 1, k):
                if j - i + 1 in (1, k):
                    continue
                vals = t[i:j + 1]
                if max(vals) - min(vals) == j - i:
                    ok = False; break
            if not ok: break
        if ok: out.append(t)
    return out

if PATTERNS == [(0,)]:
    PATTERNS = simple_perms(4) + simple_perms(5)
elif PATTERNS == [(9,)]:
    PATTERNS = simple_perms(4)

OFF = NMAX  # bit offset for diagonals
def mask(D):
    m = 0
    for d in D: m |= 1 << (d + OFF)
    return m

def offsets(tau, sizes):
    k = len(tau)
    rs = [sum(sizes[:i]) for i in range(k)]
    # column order: block with tau value v gets columns after blocks with smaller tau value
    inv = sorted(range(k), key=lambda i: tau[i])
    cs = [0] * k; acc = 0
    for i in inv:
        cs[i] = acc; acc += sizes[i]
    return [cs[i] - rs[i] for i in range(k)]

def compositions(n, k):
    for cuts in combinations(range(1, n), k - 1):
        b = (0,) + cuts + (n,)
        yield tuple(b[i + 1] - b[i] for i in range(k))

solved = {}   # m -> list of masks of solved valid D at size m (with D tuples)
shifted = {}  # (m, off) -> list of masks

def get_shift(m, o):
    key = (m, o)
    if key not in shifted:
        shifted[key] = [mask([d + o for d in D]) for D in solved[m]]
    return shifted[key]

def inflation_hit(Dm, n, tau):
    k = len(tau)
    for sizes in compositions(n, k):
        offs = offsets(tau, sizes)
        lists = []
        for m, o in zip(sizes, offs):
            L = [x for x in get_shift(m, o) if x & ~Dm == 0]
            if not L: break
            lists.append(L)
        else:
            lists.sort(key=len)
            def rec(j, acc):
                if j == k: return acc == Dm
                for x in lists[j]:
                    if x & acc == 0 and rec(j + 1, acc | x): return True
                return False
            if rec(0, 0): return True
    return False

base_cache = {}
def base(n):
    if n not in base_cache:
        s = set()
        for M, a, b, p in affine_perms(n, range(n, 3 * n + 2)):
            s.add(diags(p))
        s |= {D for D in band_sets(n) if is_valid(D, n)}
        for D in enum_valid(n):
            if all(-d in D for d in D) and find_witness(D, n, involution=True):
                s.add(D)
        base_cache[n] = s
    return base_cache[n]

print("n | #noTight(mirror) | covered | uncovered")
for n in range(1, NMAX + 1):
    V = enum_valid(n); B = base(n); S = []; solvedset = set()
    for D in V:
        r = False
        tc = tight_cuts(D, n)
        if n == 1: r = True
        elif tc:
            k = tc[0]
            lo = tuple(d + (n - k) for d in D[:k]); hi = tuple(d - k for d in D[k:])
            r = lo in solvedsets[k] and hi in solvedsets[n - k]
        else:
            r = D in B
            Dm = mask(D)
            if not r: r = inflation_hit(Dm, n, (1, 2))
            for tau in PATTERNS:
                if r: break
                if len(tau) <= n: r = inflation_hit(Dm, n, tau)
        if r: S.append(D); solvedset.add(D)
    solved[n] = S
    solvedsets = globals().setdefault('solvedsets', {})
    solvedsets[n] = solvedset
    reps = {canon(D) for D in V if not tight_cuts(D, n)}
    cov = {canon(D) for D in solvedset if not tight_cuts(D, n)}
    print(n, "|", len(reps), "|", len(cov), "|", len(reps) - len(cov), flush=True)
    with open(f"uncovered_infl_{n}.txt", "w") as f:
        for D in sorted(reps - cov): f.write(f"{list(D)}  s={scores(D, n)}\n")
