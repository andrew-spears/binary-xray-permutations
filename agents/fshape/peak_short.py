"""PEAK, ZERO on SHORT prefixes with LARGE slack (outside the range of the slack automaton, which stops at 14).
All legal prefixes x of length <= K with letters <= L (no slack bound).  Usage: python3 peak_short.py K L"""
import sys
from core import *
K, L = int(sys.argv[1]), int(sys.argv[2])
n = {"PEAK": [0, 0], "ZERO": [0, 0]}; maxs = 0; shown = 0
def test(name, x, Fxs, u, v):
    global shown
    c = len(v) - len(u); S, T = Fxs, Fxs
    for t in sums(x + u)[len(x):]: S = step(S, t)
    for t in sums(x + v)[len(x):]: T = step(T, t)
    bad = [a for a in S if (sh(a[0], c), sh(a[1], c)) not in T]
    n[name][0] += 1; n[name][1] += bool(bad)
    if bad and shown < 12: shown += 1; print(f"{name} fails after {x} (slack {sum(x)}): {len(bad)} of {len(S)} states, e.g. rows {bits(bad[0][0])} cols {bits(bad[0][1])}", flush=True)
def rec(x, s, Fxs):
    global maxs
    if x:
        maxs = max(maxs, s)
        if x[-1] <= 1: test("PEAK", x, Fxs, (0,), (1, 0, -1))
        if x[-1] <= 0 and s >= 1: test("ZERO", x, Fxs, (-1,), (0, -1))
    if len(x) == K: return
    for e in range(0 if not x else max(-s, x[-1] - 1), L + 1):
        rec(x + (e,), s + e, step(Fxs, 2 * (len(x) + 1) + e))
rec((), 0, {(0, 0)})
print(f"K = {K}, L = {L}: max slack {maxs}; PEAK tested {n['PEAK'][0]} prefixes, fails {n['PEAK'][1]}; ZERO tested {n['ZERO'][0]}, fails {n['ZERO'][1]}")
