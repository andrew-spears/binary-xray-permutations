"""Independent check of online_fixed_n.py, written in board coordinates.
Adversary: reveals d_1 < d_2 < ... one at a time; a prefix is legal iff it is a prefix of some valid D of size n
(valid D enumerated directly from Landau).  Placer: puts a point on the revealed diagonal in a free row and column.
Placer wins if all n points get placed.   Usage: python3 online_check.py nmax"""
import sys
from functools import lru_cache
from check_walks import valid_Ds
sys.setrecursionlimit(10000)
def play(n):
    nxt = {}
    for D in valid_Ds(n):
        for k in range(n): nxt.setdefault(D[:k], set()).add(D[k])
    @lru_cache(None)
    def win(prefix, R, C):
        if len(prefix) == n: return True
        for d in sorted(nxt[prefix]):
            if not any(not (R >> r & 1) and 1 <= r + d <= n and not (C >> (r + d) & 1)
                       and win(prefix + (d,), R | 1 << r, C | 1 << (r + d)) for r in range(1, n + 1)):
                return False
        return True
    return win((), 0, 0)
for n in range(2, int(sys.argv[1]) + 1):
    print(n, "Placer wins online" if play(n) else "Placer LOSES online", flush=True)
