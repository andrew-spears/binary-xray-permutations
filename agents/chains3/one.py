# Is every word of G (valid, no letter >= 2 before a letter <= -2) solved by two chains plus ONE stone?
# Complete search (sol3.cpp, all solutions with at most three chains).   Usage: python3 one.py n [pm1]
# With pm1: only the words with letters in {-1, 0, 1}.
import sys
from lib import *
import two
from extra import extras
def pm1(n):
    out = []
    def rec(w, s):
        if len(w) == n:
            if s == 0: out.append(tuple(w))
            return
        for x in (1, 0, -1):
            if (w and x < w[-1] - 1) or s + x < 0 or s + x > n - len(w) - 1: continue
            rec(w + [x], s + x)
    rec([], 0); return out
n = int(sys.argv[1]); tot = two_ok = 0; none = []; only = len(sys.argv) > 2
for e in (pm1(n) if only else words(n)):
    hi = hl = False
    for x in e:
        if x >= 2: hi = True
        if x <= -2 and hi: hl = True
    if hl: continue
    tot += 1
    if two.accepts(e): two_ok += 1; continue
    if not extras(e): none.append(e)
print("n %d  words%s: %d  two chains: %d  two chains + one stone: %d  neither: %d" % (n, " with letters in -1,0,1" if only else " of G", tot, two_ok, tot - two_ok - len(none), len(none)))
for e in none: print("   ", " ".join(map(str, e)), "  tight cut" if any(sum(e[:t]) == 0 for t in range(1, n)) else "", "  letters in -1,0,1" if max(map(abs, e)) <= 1 else "")
