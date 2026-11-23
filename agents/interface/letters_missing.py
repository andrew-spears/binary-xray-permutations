"""For |e| <= c: list, per summary (sigma, last letter), each distinct reachable set by the states it MISSES,
with the suffixes of the prefixes that produce it.   Usage: python3 letters_missing.py c N [maxsigma]"""
import sys
from collections import defaultdict
sys.argv, argv = [sys.argv[0], sys.argv[1], "0"], sys.argv
import letters_dfa as L
c = int(argv[1]); N = int(argv[2]); ms = int(argv[3]) if len(argv) > 3 else 5
W = L.W = N + c + 2; L.base = base = (1 << W) - 1
from itertools import combinations
def allstates(sig):
    # all pairs of masks with total excess sig: build by brute force over partitions
    def parts(n, mx=None):
        mx = n if mx is None else mx
        if n == 0: yield (); return
        for a in range(min(n, mx), 0, -1):
            for p in parts(n - a, a): yield (a,) + p
    return {(p, q) for a in range(sig + 1) for p in parts(a) for q in parts(sig - a)}
start = (0, None, frozenset([(base, base)]))
level = {start: ""}; out = defaultdict(dict)
for k in range(N):
    nxt = {}
    for (sig, ep, S), w in level.items():
        lo = 0 if ep is None else ep - 1
        for e in range(max(lo, -c, -sig), c + 1):
            if sig + e == 0: continue
            T = L.step(S, e); key = (sig + e, e, T); w2 = w + "-0+"[e + 1] if c == 1 else w + f"{e:+d} "
            if key not in nxt: nxt[key] = w2
            out[(sig + e, e)].setdefault(T, []).append(w2)
    level = nxt
for key in sorted(out):
    if key[0] > ms: continue
    al = allstates(key[0])
    for T, ws in out[key].items():
        miss = sorted(al - {(L.part(r), L.part(cm)) for r, cm in T})
        print(key, f"missing {len(miss)}/{len(al)}:", miss if len(miss) <= 12 else "...", "| e.g.", sorted(ws, key=len)[:4])
