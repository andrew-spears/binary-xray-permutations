"""Class l1, NEAR-DIAGONAL FORM: every + stone is at (k, k+1) or (k+1, k), every - stone at (k-1, k) or (k, k-1)
(reflected rows; stone k has row + col = 2k + e_k); the 0 stones are free.
Counts valid words of length n with no witness of this form.   Usage: python3 form2.py n [maxdisp]
maxdisp: also require |row - k| <= maxdisp for the 0 stones."""
import sys
from form import words
def solve(w, md=None):
    n = len(w); R = [False] * (n + 2); C = [False] * (n + 2); pos = [None] * n
    order = [k for k in range(1, n + 1) if w[k - 1] != 0] + [k for k in range(1, n + 1) if w[k - 1] == 0]
    def opts(k):
        e = w[k - 1]
        if e == 1: return [(k, k + 1), (k + 1, k)]
        if e == -1: return [(k - 1, k), (k, k - 1)]
        lo, hi = (1, n) if md is None else (max(1, k - md), min(n, k + md))
        return [(r, 2 * k - r) for r in range(lo, hi + 1) if 1 <= 2 * k - r <= n]
    def rec(i):
        if i == n: return True
        k = order[i]
        for r, c in opts(k):
            if 1 <= r <= n and 1 <= c <= n and not R[r] and not C[c]:
                R[r] = C[c] = True; pos[k - 1] = (r, c)
                if rec(i + 1): return True
                R[r] = C[c] = False
        return False
    return pos if rec(0) else None
if __name__ == "__main__":
    n = int(sys.argv[1]); md = int(sys.argv[2]) if len(sys.argv) > 2 else None; tot = bad = 0
    for w in words(n):
        tot += 1
        if solve(w, md) is None:
            bad += 1
            if bad <= 5: print("  no witness of this form:", "".join("-0+"[e + 1] for e in w))
    print(f"n = {n}: {tot} valid words, {bad} without a near-diagonal witness" + (f" (zeros within {md})" if md else ""))
