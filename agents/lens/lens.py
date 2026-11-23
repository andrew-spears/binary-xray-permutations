"""Two tournaments instead of two permutations.
a = rows, b = a + d = columns (0-based).  Relaxation: a and b are score vectors of tournaments
(lattice points of the permutohedron P_n).  A solution is a point where both are vertices,
i.e. where |a|^2 + |b|^2 is maximal.  Question: does hill climbing on |a|^2 + |b|^2 by unit
exchanges a -> a + e_i - e_j (inside both polytopes) get stuck at a non-solution?
usage: python3 lens.py n
"""
import sys, itertools
from math import comb

def valid_sets(n):
    out = []
    def rec(k, last, tot, D):
        if k == n:
            if tot == 0: out.append(tuple(D))
            return
        for d in range(last + 1, n):
            # Landau: sum_{i<=k} (d_i + n - i) >= C(k,2)
            t = tot + d
            s = t + sum(n - i for i in range(1, k + 2))
            if s < comb(k + 1, 2): continue
            rec(k + 1, d, t, D + [d])
    rec(0, -n, 0, [])
    return out

def in_P(a):
    s = sorted(a); t = 0
    for k, x in enumerate(s):
        t += x
        if t < k * (k + 1) // 2: return False
    return True

def lattice(n, d):
    """all a in P_n with a + d in P_n"""
    tot = comb(n, 2); out = []
    def rec(k, a, rem):
        if k == n:
            if rem == 0 and in_P(a) and in_P([a[i] + d[i] for i in range(n)]): out.append(tuple(a))
            return
        lo = max(0, -d[k]); hi = min(n - 1, n - 1 - d[k], rem)
        for x in range(lo, hi + 1):
            rec(k + 1, a + [x], rem - x)
    rec(0, [], tot)
    return out

def val(a, d): return sum(x * x + (x + y) * (x + y) for x, y in zip(a, d))

def main():
    n = int(sys.argv[1])
    top = 2 * sum(i * i for i in range(n))
    bad = 0; nD = 0; worst = None
    for d in valid_sets(n):
        nD += 1
        L = set(lattice(n, d))
        stuck = []
        for a in L:
            v = val(a, d)
            if v == top: continue
            better = False
            for i in range(n):
                for j in range(n):
                    if i == j: continue
                    c = list(a); c[i] += 1; c[j] -= 1; c = tuple(c)
                    if c in L and val(c, d) > v: better = True; break
                if better: break
            if not better: stuck.append(a)
        if stuck:
            bad += 1
            if worst is None or len(stuck) > worst[2]: worst = (d, len(L), len(stuck), stuck[:3])
    print(f"n = {n}: {nD} valid sets; sets with a strict local maximum that is not a solution: {bad}")
    if worst: print("  example:", worst)
main()
