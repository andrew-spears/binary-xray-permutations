"""Part C: type C_n as a board problem.  rho = (n, ..., 1).  A target is m_1 > ... > m_n >= 1 (distinct positive integers),
even sum, m_1 + ... + m_k <= k(2n - k + 1) for all k.  A solution: permutation sigma and signs with multiset
{ |i + eps_i sigma(i)| } = {m}.   (Type A = all signs +, read along anti-diagonals, with rho = (n..1): sums i + sigma(i).)
Usage: python3 ctype.py n"""
import sys, itertools
def targets(n):
    out = []
    def rec(k, m, s):
        if k == n:
            if s % 2 == 0: out.append(tuple(m))
            return
        hi = (m[-1] - 1) if m else 2 * n
        for v in range(hi, 0, -1):
            if s + v <= (k + 1) * (2 * n - k): rec(k + 1, m + [v], s + v)
    rec(0, [], 0); return out
def solutions(n, m, limit=None, plus_only=False):
    """all (sigma, signs): row i (1..n) gets value sigma(i) and sign; reads i + sigma(i) or |i - sigma(i)|"""
    need = set(m); sols = []
    def rec(i, usedv, got, acc):
        if limit and len(sols) >= limit: return
        if i == 0: sols.append(tuple(acc)); return
        for v in range(1, n + 1):
            if usedv >> v & 1: continue
            for sg in ((1,) if plus_only else (1, -1)):
                t = abs(i + sg * v)
                if t in need and t not in got:
                    got.add(t); acc.append((i, sg * v)); rec(i - 1, usedv | 1 << v, got, acc); acc.pop(); got.discard(t)
    rec(n, 0, set(), []); return sols
if __name__ == "__main__":
    n = int(sys.argv[1]); T = targets(n); bad = 0; mn = 10**9; arg = None
    for m in T:
        c = len(solutions(n, m))
        if c == 0: bad += 1; print("NO SOLUTION", m)
        if c < mn: mn, arg = c, m
    print(f"C_{n}: {len(T)} targets, {bad} without solution, least number of solutions {mn} at {arg}")
