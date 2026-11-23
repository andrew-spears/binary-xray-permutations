"""F(1^a) and F(1^a 0) against the theorems of REPORT2 section 1 (states from ./fx -d).   python3 ones0.py A"""
import sys, subprocess
from fx import partitions, conj
def beta(l, n): return {(l[i] if i < len(l) else 0) + n - i for i in range(n)}
def F(word):
    out = subprocess.run(["./fx", "-d"] + [str(e) for e in word], capture_output=True, text=True).stdout.split()
    return {tuple(() if p == "-" else tuple(int(a) for a in p.split(",")) for p in t.split("|")) for t in out}
def states(s): return [(l, m) for a in range(s + 1) for l in partitions(a) for m in partitions(s - a)]
odd = lambda A: sum(a % 2 for a in A)
def E1(n):          # (lam | lam'), |lam| = n/2, empty 2-core
    return {(l, conj(l)) for l in partitions(n // 2) if 2 * odd(beta(l, n)) == n} if n % 4 == 0 else set()
def E0(a):          # (2nu2 | 2kappa2), |nu| + |kappa| = a/4, beta(nu) and a - beta(kappa) (a/2 beads each) meet in one point
    if a % 4: return set()
    m = a // 4; out = set(); blow = lambda v: tuple(2 * x for x in v for _ in (0, 1))
    for i in range(m + 1):
        for nu in partitions(i):
            for ka in partitions(m - i):
                if len(beta(nu, 2 * m) & {a - b for b in beta(ka, 2 * m)}) == 1: out.add((blow(nu), blow(ka)))
    return out
for a in range(1, int(sys.argv[1]) + 1):
    S = states(a)
    P = {t for t in S if odd(beta(t[0], a)) + odd(beta(t[1], a)) == a}
    Q = {t for t in S if abs(odd(beta(t[0], a + 1)) + odd(beta(t[1], a + 1)) - a - 1) == 1}
    f1 = F((1,) * a); f0 = F((1,) * a + (0,))
    print(f"a {a:2d}: F(1^a) = P - E: {f1 == P - E1(a)} (|P| {len(P)}, |E| {len(E1(a))});   F(1^a 0) = Q - E0: {f0 == Q - E0(a)} (|Q| {len(Q)}, |E0| {len(E0(a))})", flush=True)
