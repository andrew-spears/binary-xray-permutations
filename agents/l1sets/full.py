"""All(s) = every interface state of slack s (every pair of diagrams with s boxes in total).
(1) Is step_e(All(s)) = All(s + e) for e in {-1, 0, +1}?   (2) Which prefixes with letters -1, 0, +1 reach all of All(s)?
Usage: python3 full.py B K"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "interface"))
from sets import allstates
from rewrite import machine
from collections import defaultdict
B, K = int(sys.argv[1]), int(sys.argv[2]); step, start = machine(B); lvl = allstates(B, step, start)
for s in range(B):
    row = []
    for e in (-1, 0, 1):
        if 0 <= s + e < B: row.append(f"{'-0+'[e + 1]}: {len(lvl[s + e] - step(frozenset(lvl[s]), e))} missed")
    print(f"slack {s}: {len(lvl[s])} states; states of slack s+e with no predecessor by e:", ", ".join(row))
tot = defaultdict(int); notfull = defaultdict(list); seen = set()
def red(w):                      # the word after its last return to height <= 1 is what matters (tested below)
    return w
layer = [(frozenset([start]), 0, None, "")]
while layer:
    nxt = []
    for S, s, last, w in layer:
        if len(w) == K: continue
        for e, ch in ((-1, "-"), (0, "0"), (1, "+")):
            if s + e < 0 or s + e > B - 1 or (last == 1 and e == -1): continue
            S2 = step(S, e); w2 = w + ch; tot[s + e] += 1
            if len(S2) < len(lvl[s + e]): notfull[s + e].append(w2)
            nxt.append((S2, s + e, e, w2))
    layer = nxt
import re
def h_at(w, i): return sum({"+": 1, "0": 0, "-": -1}[c] for c in w[:i])
for s in sorted(tot):
    tails = defaultdict(int)
    for w in notfull[s]:
        h = 0; cut = 0
        for i, ch in enumerate(w):
            h += {"+": 1, "0": 0, "-": -1}[ch]
            if h <= 1 and ch != "+": cut = i + 1          # last time at height <= 1 on a 0 or -
        tails[("+" if cut and h_at(w, cut) == 1 else "") + w[cut:]] += 1 if False else 1
    print(f"slack {s}: {tot[s]} prefixes of length <= {K}, {len(notfull[s])} do not reach every state; their tails after the last 0 or - at height <= 1:",
          " ".join(sorted(tails, key=lambda t: (len(t), t))[:40]))
