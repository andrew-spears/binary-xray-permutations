"""Check that the automaton's alphabet rule generates exactly the valid no-tight-cut D.
Counts words e_1..e_n with e_1 >= 0, e_{k+1} >= e_k - 1, inner slacks >= 1, final slack 0, max slack <= B
and compares with a direct enumeration of valid no-tight-cut D (for B >= n^2/8 they must agree).
Usage: python3 check_words.py nmax"""
import sys
from functools import lru_cache
from math import comb
from check_walks import valid_Ds
def count_words(n, B):
    @lru_cache(None)
    def f(k, e, sig):
        if k == n: return 1 if sig == 0 else 0
        lo = 0 if e is None else e - 1
        tot = 0
        for e2 in range(max(lo, -sig), B - sig + 1):
            s2 = sig + e2
            if s2 == 0 and k + 1 < n: continue
            tot += f(k + 1, e2, s2)
        return tot
    return f(0, None, 0)
for n in range(2, int(sys.argv[1]) + 1):
    direct = 0
    for D in valid_Ds(n):
        s = [D[k] + n - (k+1) for k in range(n)]
        if all(sum(s[:k]) > comb(k, 2) for k in range(1, n)): direct += 1
    print(n, "no-tight-cut valid D:", direct, " words (B = n^2/8):", count_words(n, n * n // 8), " words (B = n^2/8 - 1):", count_words(n, n * n // 8 - 1))
