"""Slack-only families for |e| <= c inside a class of states: at most d advanced lines in total (rows + columns).
Usage: python3 letters_Fclass.py c Bmax"""
import sys
from invariant import analyse
c = int(sys.argv[1]); Bmax = int(sys.argv[2])
for B in range(4, Bmax + 1):
    res = []
    for d in range(1, 6):
        adv = lambda m: bin(m >> B).count("1")
        nodes, I, fails, allst = analyse(B, 0, upd=lambda h, e, s: (1 - c,), cap=c, keep=lambda r, cm: adv(r) + adv(cm) <= d)
        res.append(f"d={d}: " + ("ok " + ",".join(str(len(I[s])) for s in sorted(nodes) if s[0]) if not fails else "FAILS"))
        if not fails: break
    print(f"c={c} B={B}:", "; ".join(res), flush=True)
