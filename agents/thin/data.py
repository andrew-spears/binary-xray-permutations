"""Step 1: forced states (in every accepting family) and greedy-minimal accepting families for slack bound B.
Usage: python3 data.py B [show]"""
import sys, random
from thin import *
B = int(sys.argv[1]); m = M(B); n = len(m.states); show = len(sys.argv) > 2
forced = [i for i in range(1, n) if not m.accepts(m.full ^ (1 << i))]
print(f"B = {B}: {n} states; forced: {len(forced)}:", " ".join(m.name(i) for i in forced))
def greedy(order):
    T = m.full
    for i in order:
        if i and m.accepts(T ^ (1 << i)): T ^= 1 << i
    return T
key = {"fewest parts kept": lambda i: -(len(m.states[i][0]) + len(m.states[i][1])),
       "balanced kept": lambda i: -abs(sum(m.states[i][0]) - sum(m.states[i][1])),
       "unbalanced kept": lambda i: abs(sum(m.states[i][0]) - sum(m.states[i][1])),
       "small first part kept": lambda i: -max(m.states[i][0] + m.states[i][1], default=0),
       "high slack deleted first": lambda i: -m.slack[i], "low slack deleted first": lambda i: m.slack[i]}
res = {}
for k, f in key.items(): res[k] = greedy(sorted(range(n), key=lambda i: (f(i), i)))
random.seed(1)
for r in range(3):
    o = list(range(n)); random.shuffle(o); res[f"random {r}"] = greedy(o)
allT = 0
for k, T in res.items():
    per = [sum(1 for i in range(n) if T >> i & 1 and m.slack[i] == s) for s in range(B + 1)]
    print(f"  {k:26s} size {bin(T).count('1'):4d}  per slack {per}")
    if show: print("      ", " ".join(m.name(i) for i in range(n) if T >> i & 1))
    allT |= T
print("  per slack, all states:", [sum(1 for i in range(n) if m.slack[i] == s) for s in range(B + 1)])
