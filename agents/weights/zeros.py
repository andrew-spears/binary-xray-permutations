"""F(1^a 0^b) against the parity-count set Q (states from ./fx -d).   python3 zeros.py A B"""
import sys
from ones0 import *
def Q(S, n, z, p):
    out = set()
    for t in S:
        oR = odd(beta(t[0], n)); oC = odd(beta(t[1], n))
        if abs(oR + oC - n) <= z and (oR + oC - n - z) % 2 == 0 and abs(oR - oC) <= p and (oR - oC - p) % 2 == 0: out.add(t)
    return out
nm = lambda t: "|".join("".join(map(str, p)) or "-" for p in t)
if __name__ == "__main__":
    for a in range(1, int(sys.argv[1]) + 1):
        S = states(a); row = []
        for b in range(1, int(sys.argv[2]) + 1):
            f = F((1,) * a + (0,) * b); q = Q(S, a + b, b, a); assert f <= q
            row.append(f"0^{b}: {len(q) - len(f)} of {len(q)}" + (" (Q = all)" if len(q) == len(S) else ""))
        print(f"1^{a:2d}: missing  " + "   ".join(row), flush=True)
