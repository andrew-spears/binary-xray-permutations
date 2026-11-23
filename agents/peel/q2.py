# Q2: closure of a class under B-preserving peels (with true achievability)
import sys, time
from core import *
rk, ck, M = sys.argv[1], sys.argv[2], int(sys.argv[3])
for m in range(2, M + 1):
    t = time.time(); n = fail = 0; ex = []
    for R in side_sets(m, rk):
        for C in side_sets(m, ck):
            for D in achievable(R, C):
                n += 1
                good = False
                for nm, r, c in peels(R, C, D):
                    R2, C2, D2 = apply(R, C, D, r, c)
                    if in_side(R2, rk) and in_side(C2, ck) and is_ok(R2, C2, D2):
                        good = True; break
                if not good:
                    fail += 1
                    if len(ex) < 3: ex.append((R, C, sorted(D)))
    print(f"m={m} achievable={n} stuck={fail} ex={ex} {time.time()-t:.1f}s", flush=True)
