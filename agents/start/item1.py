"""Item 1: for every Landau D on n x n (n<=N), certify the parity test passes.
Certificate: an integral placement (its row parities give a; the placement is a 0/1 point of the
restricted LP).  For n <= NLP also run an independent search over all a (counts filter + LP),
not using the placement, and record how many a pass.
Usage: python3 item1.py N NLP"""
import sys, itertools, time
from common import landau_D, tight_cut, placement, parity_test

N, NLP = int(sys.argv[1]), int(sys.argv[2])
for n in range(1, N + 1):
    t0 = time.time()
    Ds = landau_D(n)
    nt = sum(tight_cut(n, D) for D in Ds)
    fails = []
    for D in Ds:
        p = placement(n, D)
        if p is None: fails.append(D); continue
        a = {d: p[d] % 2 for d in D}
        assert parity_test(n, D, a), (D, p)
    line = f"n={n} Landau D={len(Ds)} (tight-cut {nt}) placement-certified={len(Ds)-len(fails)} fails={fails[:3]}"
    if n <= NLP:
        nopass = 0; minfrac = 1.0; hist = []
        for D in Ds:
            if D > tuple(-d for d in reversed(D)): continue  # mirror reduction
            good = 0; tot = 0
            for bits in itertools.product((0, 1), repeat=n):
                a = dict(zip(D, bits))
                if parity_test(n, D, a): good += 1
            if good == 0: nopass += 1
            hist.append(good)
        line += f" | indep. LP search (mod mirror, {len(hist)} D): no-pass={nopass}, min #good a={min(hist)}"
    print(line, f"[{time.time()-t0:.1f}s]", flush=True)
