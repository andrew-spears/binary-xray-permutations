"""Filter W1 failures: keep instances whose expanded diagonal multiset D is a SET and that
have no block-level tight cut (sum_S w t = -V(W-V) for a proper subset S of width V).
Also report whether expanded D itself is Landau-valid (point-level) and solvable as an
ordinary permutation (brute force), to see if failures are grouping failures.
Usage: python3 w2_filter.py Wmax"""
import sys, itertools
sys.argv += ["block"] if len(sys.argv) < 3 else []
import w1_landau as L

def tight(t1, t2, W):
    a, b = len(t1), len(t2)
    P1 = [0]; [P1.append(P1[-1] + x) for x in t1]
    P2 = [0]; [P2.append(P2[-1] + 2 * x) for x in t2]
    for i in range(a + 1):
        for j in range(b + 1):
            V = i + 2 * j
            if 0 < V < W and P1[i] + P2[j] == -V * (W - V): return True
    return False

_perm_cache = {}
def solvable_D(D):
    n = len(D)
    if n not in _perm_cache:
        _perm_cache[n] = set(tuple(sorted(p[i] - i for i in range(n))) for p in itertools.permutations(range(n)))
    return tuple(D) in _perm_cache[n]

W = int(sys.argv[1])
for Wc in range(2, W + 1):
    for b in range(1, Wc // 2 + 1):
        a = Wc - 2 * b
        ach = L.achievable(a, b)
        L1 = L.sorted_tuples(a, -(Wc - 1), Wc - 1, Wc, 1)
        L2 = L.sorted_tuples(b, -(Wc - 2), Wc - 2, Wc, 2)
        nv = nf = nDsolv = 0; ex = []
        for t1 in L1:
            for t2 in L2:
                if not L.landau_block(t1, t2, a, b, Wc): continue
                D = L.expand(t1, t2)
                if len(set(D)) < len(D) or tight(t1, t2, Wc): continue
                assert L.landau_point(t1, t2, a, b, Wc) == True or True
                nv += 1
                if (t1, t2) not in ach:
                    nf += 1
                    s = solvable_D(D); nDsolv += s
                    if len(ex) < 4: ex.append((t1, t2, D, s, L.landau_point(t1, t2, a, b, Wc)))
        print(f"W={Wc} a={a} b={b}: valid(distinct,no-tight)={nv} failures={nf} of which D solvable={nDsolv}", flush=True)
        for e in ex: print("   ", e, flush=True)
