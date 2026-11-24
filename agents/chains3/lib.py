# Shared helpers.  Convention of agents/patterns: rows and columns 0-based, stone (i, c) on line i + c,
# word e: the sorted lines are e_j + 2j (j = 0..n-1).  Chains are increasing.
import subprocess, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
def words(n, notight=False):
    out = []
    def rec(w, s):
        if len(w) == n:
            if s == 0: out.append(tuple(w))
            return
        lo = w[-1] - 1 if w else 0
        for e in range(max(lo, -s), n - len(w)):
            if notight and s + e == 0 and len(w) < n - 1: continue
            rec(w + [e], s + e)
    rec([], 0); return out
def lines(e): return [x + 2 * j for j, x in enumerate(e)]
def word_of(L):
    L = sorted(L); return tuple(x - 2 * j for j, x in enumerate(L))
def sols(e, w=3, cap=10**9):
    out = subprocess.run([os.path.join(HERE, "sol3"), str(w), str(cap)] + [str(x) for x in e], capture_output=True, text=True).stdout
    return [tuple(int(x) for x in l.split()) for l in out.splitlines()]
def width(pi):
    import bisect
    t = []                                  # longest decreasing subsequence
    for c in pi:
        j = bisect.bisect_left(t, -c)
        if j == len(t): t.append(-c)
        else: t[j] = -c
    return len(t)
def chains(pi):
    tops = []; col = []                     # first-fit (patience): optimal chain cover
    for c in pi:
        best = None
        for j, t in enumerate(tops):
            if t < c and (best is None or t > tops[best]): best = j
        if best is None: tops.append(c); col.append(len(tops) - 1)
        else: tops[best] = c; col.append(best)
    return col
def blocks(pi):
    """maximal runs of neighbouring rows going to neighbouring columns: list of (row0, col0, length)"""
    out = []; i = 0; n = len(pi)
    while i < n:
        j = i
        while j + 1 < n and pi[j + 1] == pi[j] + 1: j += 1
        out.append((i, pi[i], j - i + 1)); i = j + 1
    return out
def fmt(pi): return " | ".join(" ".join(str(pi[i] + 1) for i in range(r, r + l)) for r, c, l in blocks(pi))
def valid(e):
    s = 0
    for j, x in enumerate(e):
        if j and x < e[j - 1] - 1: return False
        s += x
        if s < 0: return False
    return s == 0 and (not e or e[0] >= 0)
def check(e, pi, w=3):
    n = len(e); return sorted(pi) == list(range(n)) and sorted(i + pi[i] for i in range(n)) == lines(e) and width(pi) <= w
