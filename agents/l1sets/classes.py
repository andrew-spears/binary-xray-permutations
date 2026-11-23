"""Which words (letters -1, 0, +1, no '+ -') give the same reachable set?  Usage: python3 classes.py B K s"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "interface"))
from rewrite import machine
from collections import defaultdict
B, K, s0 = map(int, sys.argv[1:4]); step, start = machine(B)
cls = defaultdict(list)
def go(S, s, last, w):
    if s == s0 and w: cls[S].append(w)
    if len(w) == K: return
    for e, ch in ((-1, "-"), (0, "0"), (1, "+")):
        if s + e < 0 or s + e > B - 1 or (last == 1 and e == -1): continue
        go(step(S, e), s + e, e, w + ch)
go(frozenset([start]), 0, None, "")
for S, ws in sorted(cls.items(), key=lambda t: len(t[0])):
    print(len(S), len(ws), " ".join(ws[:int(sys.argv[4]) if len(sys.argv) > 4 else 14]))
