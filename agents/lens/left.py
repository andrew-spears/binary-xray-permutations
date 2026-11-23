"""What is left after the proved families: words without a tight cut whose middle m (first letter >= 2 .. last letter <= -2)
is not of the form {0,1,2}*{0,-1,-2}* (Theorem H).  Tally by (max letter, min letter) of m and by number of sign-hills.
usage: python3 left.py n"""
import sys, re
from collections import Counter
n = int(sys.argv[1])
tot = 0; left = Counter(); shape = Counter(); nleft = 0
def rec(w, s):
    global tot, nleft
    k = len(w)
    if k == n:
        if s != 0: return
        tot += 1
        hi = [i for i, e in enumerate(w) if e >= 2]; lo = [i for i, e in enumerate(w) if e <= -2]
        if not hi or not lo or hi[0] > lo[-1]: return
        m = w[hi[0]:lo[-1] + 1]
        # Theorem H: m = a b, a in {0,1,2}*, b in {0,-1,-2}*
        j = 0
        while j < len(m) and 0 <= m[j] <= 2: j += 1
        if all(-2 <= e <= 0 for e in m[j:]): return
        nleft += 1
        left[(max(m), min(m))] += 1
        # hills: number of maximal blocks of letters >= 2 separated by a letter <= -2
        sig = "".join("H" if e >= 2 else "L" if e <= -2 else "" for e in m)
        shape[len(re.findall("H+", sig))] += 1
        return
    lo = -(n) if k == 0 else w[-1] - 1
    for e in range(max(lo, -s + (0 if k == n - 1 else 1)), n - k):
        if k == 0 and e < 0: continue
        # remaining letters can bring the slack back to 0: crude bound
        rec(w + (e,), s + e)
rec((), 0)
print(f"n = {n}: words without tight cut {tot}; not covered by 0', H: {nleft}")
print(" by (max, min) of the middle:", sorted(left.items(), key=lambda t: -t[1])[:14])
print(" by number of high blocks:", sorted(shape.items()))
