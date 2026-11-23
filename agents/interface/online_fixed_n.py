"""Online placement game at fixed n (Placer knows n but not the future diagonals).
Adversary reveals the diagonals in increasing order; any prefix that extends to a valid D of
size n is legal.  Placer must place each stone on arrival.  Usage: python3 online_fixed_n.py nmax"""
import sys
from functools import lru_cache
sys.setrecursionlimit(100000)
def play(n):
    @lru_cache(None)
    def feas(m, e, sig):
        # can a word continue for m more letters after last letter e with slack sig, ending at 0?
        if m == 0: return sig == 0
        lo = -10**9 if e is None else e - 1
        for e2 in range(max(lo, -sig), n):
            if sig + e2 > m * m: break
            if feas(m - 1, e2, sig + e2): return True
        return False
    @lru_cache(None)
    def win(k, e, sig, R, C):
        if k == n: return True
        lo = -10**9 if e is None else e - 1
        for e2 in range(max(lo, -sig, -k), n - k):
            if not feas(n - k - 1, e2, sig + e2): continue
            ok = False
            for u in range(-k, n - k):
                r = k + 1 + u; c = k + 1 + e2 - u
                if c < 1 or c > n or (R >> r & 1) or (C >> c & 1): continue
                if win(k + 1, e2, sig + e2, R | 1 << r, C | 1 << c): ok = True; break
            if not ok: return False
        return True
    return win(0, None, 0, 0, 0)
for n in range(2, int(sys.argv[1]) + 1):
    print(n, "Placer wins online" if play(n) else "Placer LOSES online", flush=True)
