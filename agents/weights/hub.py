"""Common states: for each slack s and class K, the least b such that some state lies in N_0^b(t) for every t of the class, and those states.
  python3 hub.py S"""
import sys, numpy as np
from maya import Maya, dval
for s in range(2, int(sys.argv[1]) + 1):
    Mo = Maya(s); L = Mo.states(s); ix = {t: i for i, t in enumerate(L)}; m = len(L)
    T = np.zeros((m, m), dtype=np.float32)
    for t in L:
        for u in Mo.succ(t, 0): T[ix[t], ix[u]] = 1
    K = np.array([dval(Mo, t, 2 * s + 6)[1] for t in L]); P = np.eye(m, dtype=np.float32); done = set()
    for b in range(0, 3 * s + 4):                        # b = 0: a class with one state is its own common successor
        if b: P = (P @ T > 0).astype(np.float32)
        for k in sorted(set(K)):
            if k in done or k < 0: continue
            rows = np.where(K == k)[0]; common = np.where(P[rows].all(axis=0))[0]
            if len(common):
                done.add(k); print(f"s {s} class K = {k:2d} ({len(rows)} states): common successor first at b = {b}: {len(common)} states: {' '.join(Mo.name(L[i]) for i in common[:10])}", flush=True)
