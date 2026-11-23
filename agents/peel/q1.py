import sys, time
from core import *
rk, ck, M = sys.argv[1], sys.argv[2], int(sys.argv[3])
for m in range(1, M + 1):
    t = time.time(); nb = nD = nfail = 0; first = None
    for R in side_sets(m, rk):
        for C in side_sets(m, ck):
            nb += 1; A = achievable(R, C)
            for D in all_sumtest_D(R, C):
                nD += 1
                if D not in A:
                    nfail += 1
                    if first is None: first = (R, C, sorted(D))
    print(f"m={m} boards={nb} sumtestD={nD} fail={nfail} first={first} {time.time()-t:.1f}s", flush=True)
