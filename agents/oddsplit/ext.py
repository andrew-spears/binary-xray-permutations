"""Extreme-term criteria for odd splits.   Usage: python3 ext.py n [uni|all] [nt] [v]     (nt: only words without a tight cut)
For a set S of stones: S-word w_j = e_k + 2 #(S^c before k), S^c-word (read backwards) w'_j = -e_k + 2 #(S after k).
theta(w) = rows of lengths w_j, row j starting in column j.  rho = row lengths, kappa = column lengths (sorted).
Proved odd states (coefficient exactly 1): (lam|gam) with lam + gam = rho(theta_S)  [row type]  or lam' + gam' = kappa(theta_S) [column type];
for S^c the state must be the conjugate.  Criteria for a common one:
  RC: rho_1 = kappa_2      CR: kappa_1 = rho_2
  RR: lam + gam = rho_1, lam u gam = rho_2'      CC: mu + nu = kappa_1, mu u nu = kappa_2'
"""
import sys, itertools
def words(n, uni):
    out = []
    def rec(w, s, down):
        k = len(w)
        if k == n:
            if s == 0: out.append(tuple(w))
            return
        lo = (w[-1] - 1) if w else 0
        for e in range(max(lo, -s), 2 * n):
            if s + e > (n - k - 1) * (n - k) // 2 + (n-k-1)*max(e,0): continue
            if uni and down and e > 0: continue
            if k and s == 0 and not uni: pass
            w.append(e); rec(w, s + e, down or e < 0); w.pop()
    rec([], 0, False); return out
def shape(w):
    rho = sorted([x for x in w if x > 0], reverse=True)
    col = {}
    for i, x in enumerate(w):
        for j in range(i, i + x): col[j] = col.get(j, 0) + 1
    return tuple(rho), tuple(sorted(col.values(), reverse=True))
def conj(p): return tuple(sum(1 for x in p if x > i) for i in range(p[0])) if p else ()
def splits(rho, tau):
    """is there lam u gam = rho with lam + gam = tau"""
    if sum(rho) != sum(tau): return False
    m = len(rho)
    if len(tau) > m or 2 * len(tau) < m: return False
    for mask in range(1 << m):
        lam = [rho[i] for i in range(m) if mask >> i & 1]; gam = [rho[i] for i in range(m) if not mask >> i & 1]
        if len(lam) < len(gam): continue
        gam += [0] * (len(lam) - len(gam))
        if tuple(a + b for a, b in zip(lam, gam)) == tau: return True
    return False
def parts(e, S):
    n = len(e); a = 0; w1 = []
    for k in range(n):
        if S >> k & 1: w1.append(e[k] + 2 * a)
        else: a += 1
    b = 0; w2 = []
    for k in range(n - 1, -1, -1):
        if S >> k & 1: b += 1
        else: w2.append(-e[k] + 2 * b)
    return w1, w2
def crit(e, S):
    w1, w2 = parts(e, S)
    if min(w1) < 0 or min(w2) < 0: return ""
    r1, k1 = shape(w1); r2, k2 = shape(w2); c = ""
    if r1 == k2: c += "RC "
    if k1 == r2: c += "CR "
    if splits(conj(r2), r1): c += "RR "
    if splits(conj(k2), k1): c += "CC "
    return c
if __name__ == "__main__":
    n = int(sys.argv[1]); uni = len(sys.argv) > 2 and sys.argv[2] == "uni"; v = 'v' in sys.argv
    nt = "nt" in sys.argv; W = words(n, uni); bad = 0; cnt = {}; tot = 0
    for e in W:
        if not any(e): continue
        if nt and any(sum(e[:k]) == 0 for k in range(1, n)): continue
        tot += 1; got = set()
        for S in range(1, (1 << n) - 1):
            c = crit(e, S)
            got |= set(c.split())
        for g in got: cnt[g] = cnt.get(g, 0) + 1
        if not got:
            bad += 1
            if v: print("  none:", e)
    print(f"n = {n} ({'unimodal' if uni else 'all valid'}): {tot} nonzero words; no extreme split: {bad}; words with each type: {cnt}")
