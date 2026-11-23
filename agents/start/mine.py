"""Precompute, for every Landau D (n <= N), the set of all parity vectors a (bits in sorted-D order)
that pass the parity test. Saved to good_n{n}.pkl.  Count filter: within odd d's exactly half have a=1;
within even d's exactly ceil(E/2) have a=1 (derived from row/col parity counts).
Usage: python3 mine.py N"""
import sys, itertools, pickle, time
from common import landau_D, parity_test

N = int(sys.argv[1])
for n in range(1, N + 1):
    t0 = time.time()
    out = {}
    for D in landau_D(n):
        good = []
        for bits in itertools.product((0, 1), repeat=n):
            a = dict(zip(D, bits))
            if parity_test(n, D, a): good.append(bits)
        out[D] = good
    pickle.dump(out, open(f"/home/claude/agents/start/good_n{n}.pkl", "wb"))
    print(n, len(out), "min good", min(len(g) for g in out.values()), f"{time.time()-t0:.1f}s", flush=True)
