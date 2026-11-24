"""Does every valid arrangement have a solution avoiding a given length-4 pattern (default 2143 = vexillary)?
Board: sigma(row) = column, d = column - row.  A solution avoids 2143 exactly when its 'above-and-right' order is an
interval order (no 2 + 2).   usage: python3 vex.py n [pattern]"""
import sys, itertools
from iv import words
sys.setrecursionlimit(10000)
def solve(D, pat):
    n = len(D); Ds = set(D); s = []; usedc = [False] * n
    def bad(v):
        # does appending value v create the pattern with v as its last letter?
        m = len(s)
        for i, j, k in itertools.combinations(range(m), 3):
            t = (s[i], s[j], s[k], v)
            if tuple(sum(y < x for y in t) for x in t) == pat: return True
        return False
    def bad2143(v):
        k = -1
        for i in range(len(s) - 1, -1, -1):
            if s[i] > v: k = i; break
        if k < 2: return False
        mx = -1
        for i in range(k):
            x = s[i]
            if x < v:
                if x < mx: return True
                if x > mx: mx = x
        return False
    chk = bad2143 if pat == (1, 0, 3, 2) else bad
    def rec(r):
        if r == n: return True
        for c in range(n):
            if usedc[c] or (c - r) not in Ds or chk(c): continue
            usedc[c] = True; Ds.discard(c - r); s.append(c)
            if rec(r + 1): return True
            s.pop(); Ds.add(c - r); usedc[c] = False
        return False
    return list(s) if rec(0) else None
if __name__ == "__main__":
    n = int(sys.argv[1]); pat = tuple(int(x) - 1 for x in (sys.argv[2] if len(sys.argv) > 2 else "2143"))
    W = words(n); bad = []
    for w in W:
        D = tuple(w[k] + 2 * (k + 1) - n - 1 for k in range(n))
        if solve(D, pat) is None: bad.append(w)
    print(f"n = {n}: {len(W)} words; without a solution avoiding {''.join(str(x + 1) for x in pat)}: {len(bad)}", bad[:5], flush=True)
