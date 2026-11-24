"""The machine on pairs of Maya diagrams (moving frame), any start state.
A state (lam | mu) is a pair of bit masks: bit k + W of M(lam) is set iff k = lam_i - i for some i >= 1 (all k < -W set, none >= W).
Letter e: choose a hole i of M(lam) and a hole j of M(mu) with i + j = e, fill both, shift both diagrams down by 1
(= REPORT2 (LAST): r = n + 1 + i, c = n + 1 + j, r + c = 2n + 2 + e for stone n + 1).   Slack changes by e."""
import sys, numpy as np
from functools import lru_cache
def parts(n, m=None):
    m = n if m is None else m
    if n == 0: yield (); return
    for a in range(min(n, m), 0, -1):
        for p in parts(n - a, a): yield (a,) + p
class Maya:
    def __init__(self, smax):
        self.W = W = smax + 3; self.full = (1 << W) - 1
    def mask(self, lam):
        W = self.W; m = 0
        for i in range(1, W + 1):
            k = (lam[i - 1] if i <= len(lam) else 0) - i; m |= 1 << (k + W)
        return m
    def part(self, m):
        W = self.W; ks = [k for k in range(W - 1, -W - 1, -1) if m >> (k + W) & 1]
        return tuple(k + i for i, k in enumerate(ks, 1) if k + i > 0)
    def states(self, s):
        return [(self.mask(a), self.mask(b)) for k in range(s + 1) for a in parts(k) for b in parts(s - k)]
    def succ(self, t, e):
        W = self.W; M, N = t; out = []
        for i in range(-W, W):
            j = e - i
            if -W <= j < W and not M >> (i + W) & 1 and not N >> (j + W) & 1:
                out.append(((M | 1 << (i + W)) >> 1, (N | 1 << (j + W)) >> 1))
        return out
    def name(self, t): return "|".join("".join(map(str, self.part(m))) or "-" for m in t)
    def odd(self, m, par):            # number of beads lam_i - i (i <= 2W) of the same parity as par ... row r = lam_i - i + n + 1
        return sum(1 for k in range(-self.W, self.W) if m >> (k + self.W) & 1 and (k + par) % 2 == 0)
    def K(self, t, n):                # #odd(R) - #odd(C) with n stones (depends on n mod 2 only)
        return self.odd(t[0], n) - self.odd(t[1], n)
def dval(Mo, t, n):
    """D = #odd(R) - #even(C) for the n-stone picture (n >= slack): rows r = k + n + 1 over beads k >= -n."""
    W = Mo.W; R = [k + n + 1 for k in range(-min(n, W), W) if t[0] >> (k + W) & 1] + list(range(1, n - W + 1))
    C = [k + n + 1 for k in range(-min(n, W), W) if t[1] >> (k + W) & 1] + list(range(1, n - W + 1))
    assert len(R) == n and len(C) == n
    return sum(r % 2 for r in R) - sum(1 - c % 2 for c in C), sum(r % 2 for r in R) - sum(c % 2 for c in C)
if __name__ == "__main__":      # self-test against fx.py
    import fx
    Mo = Maya(8)
    for w in [(1, 1, 0, 1), (2, 1, 0, -1, 0), (3, 2, 0, 0, 1, -1), (1, 0, 1, 1, 1, 0, 0)]:
        S = {(Mo.mask(()), Mo.mask(()))}
        for e in w: S = {u for t in S for u in Mo.succ(t, e)}
        a = {(Mo.part(m), Mo.part(n)) for m, n in S}; b = {(fx.lam(R), fx.lam(C)) for R, C in fx.F(w)}
        assert a == b, w
        print(w, len(a), "ok")
