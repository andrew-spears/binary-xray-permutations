"""Which valid arrangements have a solution avoiding a pattern of length 3?
usage: python3 classes.py n"""
import sys, itertools
from iv import words
def avoiders(n, pat):
    """generate permutations of 0..n-1 avoiding pat (tuple of 0,1,2) by insertion of the last position"""
    out = []
    def ok(p):
        m = len(p); z = p[-1]
        for i in range(m - 1):
            for j in range(i + 1, m - 1):
                t = (p[i], p[j], z); s = sorted(t)
                if tuple(s.index(x) for x in t) == pat: return False
        return True
    def rec(p, used):
        if len(p) == n: out.append(tuple(p)); return
        for v in range(n):
            if not used[v]:
                p.append(v)
                if ok(p):
                    used[v] = True; rec(p, used); used[v] = False
                p.pop()
    rec([], [False] * n)
    return out
N = int(sys.argv[1])
for n in range(3, N + 1):
    valid = set()
    for w in words(n): valid.add(tuple(w[k] + 2 * (k + 1) - n - 1 for k in range(n)))
    line = f"n = {n}: {len(valid)} valid;"
    for pat in [(2, 1, 0), (0, 1, 2), (0, 2, 1), (1, 2, 0)]:
        got = set()
        for p in avoiders(n, pat):
            D = tuple(sorted(p[i] - i for i in range(n)))
            if len(set(D)) == n: got.add(D)
        assert got <= valid, (pat, sorted(got - valid)[:3])
        miss = sorted(valid - got)
        line += f"  avoid {''.join(str(x + 1) for x in pat)}: {len(got)}" + (f" (first missing {miss[0]})" if miss else " ALL")
    print(line)
