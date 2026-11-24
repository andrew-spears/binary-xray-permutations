"""Smallest failures of BRIDGE-ODD among steep middles.  python3 oddmin.py LEN S1MAX SMAX C NMAX"""
import sys
MYA = sys.argv[1:]; sys.argv[1:] = ["0", "3", "3", "2", "0"]
src = open("oddrand.py").read().split("COUNT, LEN, SMAX, C, SEED")[0]
exec(src)
LEN, S1MAX, SMAX, C, NMAX = map(int, MYA)
fails = []; tot = 0
def rec(s1, m, s):
    global tot
    if len(m) >= 3 and m[-1] <= -2 and s1 + len(m) + s <= NMAX:
        tot += 1
        if not ODD(s1, m): fails.append((s1 + len(m) + s, s1, m, s)); print("  fail: n =", s1 + len(m) + s, " s1 =", s1, " m =", *m, " s2 =", s, flush=True)
    if len(m) == LEN: return
    for e in range(max(-s, m[-1] - 1, -C), min(C, SMAX - s) + 1): rec(s1, m + (e,), s + e)
for s1 in range(S1MAX + 1):
    for h in range(2, C + 1): rec(s1, (h,), s1 + h)
print("middles with n <=", NMAX, ":", tot, " BRIDGE-ODD failures:", len(fails), " smallest:", min(fails) if fails else None)
