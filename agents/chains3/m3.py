# The chain machine for w chains (REPORT, Theorem 1).  Stones are read in the order of their lines.
# State: two words alpha, beta over {0, 1..w}.  alpha = the row order, beta = the column order, of the stones that
# matter now: 0 = a stone already read, X = a stone of chain X not read yet ("owed") that stands before a read stone.
# Read stones standing before all owed stones in both words are dropped (equally many from the front of each word).
# Step with letter e, chain X:  in each word the new stone is the first X if there is one; otherwise it goes to the end,
# after a freely chosen block of owed stones of the other chains.  Condition:
#       e = (letters before the stone in alpha) + (letters before it in beta) - 2 (number of 0s in alpha).
# Start and end: both words empty.
import sys
from itertools import product
from lib import *
def options(al, X, w, used, room):
    """ways to put the new stone of chain X into the word al: (letters before it, new word, new 'used')"""
    if X in al:
        p = al.index(X); yield p, al[:p] + (0,) + al[p + 1:], used
        return
    for L in range(room + 1):
        for blk in product([y for y in range(1, w + 1) if y != X], repeat=L):
            u = used; ok = True
            for y in blk:                       # chains are named in the order in which they first appear
                if y > u + 1: ok = False; break
                u = max(u, y)
            if ok: yield len(al) + L, al + blk + (0,), u
def step(st, e, w, left):
    """left = stones still unread after this one"""
    al, be, used = st; m = al.count(0); out = []
    for X in range(1, min(w, used + 1) + 1):
        u0 = max(used, X)
        for pa, al2, ua in options(al, X, w, u0, left):
            pb_need = e + 2 * m - pa
            if pb_need < 0: continue
            for pb, be2, ub in options(be, X, w, ua, left):
                if pb != pb_need: continue
                if sum(max(al2.count(y), be2.count(y)) for y in range(1, w + 1)) > left: continue
                d = 0
                while d < len(al2) and d < len(be2) and al2[d] == 0 and be2[d] == 0: d += 1
                out.append(((al2[d:], be2[d:], ub), (X, al2[len(al):-1] if X not in al else None, be2[len(be):-1] if X not in be else None)))
    return out
def accepts(e, w=3):
    S = {((), (), 0)}; n = len(e); peak = 0
    for j, x in enumerate(e):
        S = {s2 for st in S for s2, _ in step(st, x, w, n - j - 1)}; peak = max(peak, len(S))
        if not S: return False, peak
    return any(s[0] == () and s[1] == () for s in S), peak
def runs(e, w=3):
    out = []; n = len(e)
    def rec(j, st, hist):
        if j == n:
            if st[0] == () and st[1] == (): out.append(hist)
            return
        for s2, mv in step(st, e[j], w, n - j - 1): rec(j + 1, s2, hist + [mv])
    rec(0, ((), (), 0), []); return out
def rebuild(run):
    """the permutation of a run: replay it with named stones"""
    words = [[], []]
    for j, (X, ba, bb) in enumerate(run):
        for wd, blk in zip(words, (ba, bb)):
            if blk is None: wd[wd.index(("owed", X))] = ("stone", j)
            else: wd.extend(("owed", y) for y in blk); wd.append(("stone", j))
    row = {s[1]: i for i, s in enumerate(words[0])}; col = {s[1]: i for i, s in enumerate(words[1])}
    pi = [None] * len(run)
    for j in row: pi[row[j]] = col[j]
    return tuple(pi), [row[j] + col[j] for j in range(len(run))]
if __name__ == "__main__":
    if sys.argv[1] == "check":          # machine = complete search, same set of solutions, every valid word
        w, N = int(sys.argv[2]), int(sys.argv[3])
        for n in range(2, N + 1):
            bad = 0; nsol = 0; W = words(n); none = 0
            for e in W:
                R = runs(e, w); P = set()
                for r in R:
                    pi, ln = rebuild(r)
                    if ln != lines(e): bad += 1
                    P.add(pi)
                S = set(map(tuple, sols(e, w))); nsol += len(S); none += not S
                if P != S or accepts(e, w)[0] != bool(S): bad += 1
            print("w %d  n %d  words %d  without a solution of width <= w: %d  solutions %d  disagreements %d" % (w, n, len(W), none, nsol, bad))
    else:
        w = int(sys.argv[1]); e = tuple(map(int, sys.argv[2:])); print(accepts(e, w))
