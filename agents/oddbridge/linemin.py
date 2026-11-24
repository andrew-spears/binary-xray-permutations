"""Smallest failures of LINE.  python3 linemin.py LEN S1MAX SMAX C : all middles of length <= LEN, s1 <= S1MAX, slacks <= SMAX, letters in [-C, C]."""
import sys
N0 = sys.argv[1:]; sys.argv[1] = "none"
exec(open("linerand.py").read().split('if sys.argv[1] == "fam"')[0])
LEN, S1MAX, SMAX, C = map(int, N0)
fails = []; tot = 0
def rec(s1, m, s):
    global tot
    if len(m) >= 3 and m[-1] <= -2:
        tot += 1
        if not LINE(s1, m)[0]: fails.append((s1 + len(m) + s, s1, m, s))
    if len(m) == LEN: return
    for e in range(max(-s, m[-1] - 1, -C), min(C, SMAX - s) + 1): rec(s1, m + (e,), s + e)
for s1 in range(S1MAX + 1):
    for h in range(2, C + 1): rec(s1, (h,), s1 + h)
fails.sort()
print("middles:", tot, " failures:", len(fails))
for f in fails[:25]: print("  n =", f[0], " s1 =", f[1], " m =", *f[2], " s2 =", f[3])
