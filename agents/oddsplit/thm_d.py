"""Theorem D (REPORT3): w = x m valid, x a prefix with letters <= 1 and slack s >= 1, kappa a stone of m, letters of m before kappa in {0,1,2}, after kappa in {0,-1,-2}.
tau = e_k (before kappa), e_k + 2 (after kappa);  z0, z1 = number of tau equal to 0, 1.   If z0 <= s and (s, z0) != (5, 3) the word is solvable by a one-stone relative split:
  state H: x takes the hook ((z0+1, 1^(s-z0-1)) | -)         (z0 <= s - 1; central iff s even or z0 even)
  state P: x takes ((1^(s-z0)) | (z0))                        (central iff z0 even or s - z0 even)
  kappa on (lowest row not used by x, the (z0+z1+1)-th column not used by x); the other stones of m are a chain.
Checks for every valid word of length n and every such (x, kappa): the state is in G(s) (in_G of ../l2sets), x can take it (brute force), kappa is on its diagonal,
the other stones of m form a chain and their number of placements is odd (brute force).   Usage: python3 thm_d.py nmax"""
import sys
from ext import words
from rel import in_G, conj, chain
from check_rows_lib import count
def rule(e, p, kap):
    """p = length of x, kap = position of kappa (1-based).  Returns None if the hypothesis fails, else (RX, CX, cell, name)"""
    n = len(e); s = sum(e[:p])
    if s < 1 or any(a > 1 for a in e[:p]): return None
    if any(a not in (0, 1, 2) for a in e[p:kap - 1]) or any(a not in (0, -1, -2) for a in e[kap:]): return None
    tau = list(e[p:kap - 1]) + [a + 2 for a in e[kap:]]; z0 = tau.count(0); z1 = tau.count(1)
    if z0 > s or (s, z0) == (5, 3): return None                       # (5, 3): the state P is in the thin family A(5)
    if z0 <= s - 1 and (s % 2 == 0 or z0 % 2 == 0): lam, gam, name = (z0 + 1,) + (1,) * (s - z0 - 1), (), "H"
    else: lam, gam, name = (1,) * (s - z0), ((z0,) if z0 else ()), "P"
    if len(lam) > p or len(gam) > p: return None                      # the state needs that many stones in x (never binding: counted in the output)
    RX = sorted((lam[i] if i < len(lam) else 0) + p - i for i in range(p)); CX = sorted((gam[i] if i < len(gam) else 0) + p - i for i in range(p))
    rows = [a for a in range(1, n + 1) if a not in RX]; cols = [a for a in range(1, n + 1) if a not in CX]
    return RX, CX, (rows[0], cols[z0 + z1]), name, (lam, gam)
if __name__ == "__main__":
    for n in range(4, int(sys.argv[1]) + 1):
        cases = bad = nfit = 0; wordsD = set(); kinds = {"H": 0, "P": 0}
        for e in words(n, False):
            d = [2 * (k + 1) + e[k] for k in range(n)]
            for p in range(1, n):
                if e[p - 1] > 1: break
                for kap in range(p + 1, n + 1):
                    if sum(e[:p]) >= 1 and all(a in (0, 1, 2) for a in e[p:kap - 1]) and all(a in (0, -1, -2) for a in e[kap:]):
                        tau = list(e[p:kap - 1]) + [a + 2 for a in e[kap:]]
                        if tau.count(0) > sum(e[:p]) or (sum(e[:p]), tau.count(0)) == (5, 3): continue
                        res = rule(e, p, kap)
                        if res is None: nfit += 1; continue
                        RX, CX, (r, c), name, st = res; cases += 1; wordsD.add(e); kinds[name] += 1
                        RT = [a for a in range(1, n + 1) if a not in RX and a != r]; CT = [a for a in range(1, n + 1) if a not in CX and a != c]
                        DT = [d[k] for k in range(p, n) if k != kap - 1]
                        ok = in_G((st[0], conj(st[1]))) and r + c == d[kap - 1] and c in CT + [c] and chain(DT, RT, CT) \
                             and count(d[:p], RX, CX) > 0 and count(DT, RT, CT) % 2 == 1
                        if not ok:
                            bad += 1
                            if bad <= 5: print("  FAIL", e, "p =", p, "kappa =", kap, name, st, in_G((st[0], conj(st[1]))), r + c == d[kap - 1], chain(DT, RT, CT))
        print(f"n = {n}: {cases} cases (x, kappa) in {len(wordsD)} words; states H/P: {kinds['H']}/{kinds['P']}; state does not fit x: {nfit}; failures: {bad}")
