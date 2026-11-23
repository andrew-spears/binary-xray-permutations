# Q2 for class "total holes <= T" (T=1: square + G1 + transpose G1), and per-stuck diagnostics
import sys, time
from core import *
T, M = int(sys.argv[1]), int(sys.argv[2])
def boards(m):
    for R in side_sets(m, 'k%d' % T):
        for C in side_sets(m, 'k%d' % T):
            if len(holes(R)) + len(holes(C)) <= T: yield R, C
def inX(R, C): return len(holes(R)) + len(holes(C)) <= T
for m in range(2, M + 1):
    t = time.time(); n = fail = 0; ex = []; byshape = {}
    for R, C in boards(m):
        for D in achievable(R, C):
            n += 1
            good = any(inX(*apply(R, C, D, r, c)[:2]) and is_ok(*apply(R, C, D, r, c))
                       for _, r, c in peels(R, C, D))
            if not good:
                fail += 1; key = (tuple(holes(R)), tuple(holes(C)))
                byshape[key] = byshape.get(key, 0) + 1
                if len(ex) < 2: ex.append((R, C, sorted(D)))
    print(f"m={m} achievable={n} stuck={fail} byshape(rowholes,colholes)={byshape} ex={ex} {time.time()-t:.1f}s", flush=True)
