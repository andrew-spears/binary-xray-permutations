"""LP check of the failures listed by `ALLFAIL=1 ./twice n n > fails_n.txt`.
Usage: python3 lp_fails.py n"""
import sys
from lp_multiset import lp_ok
n = int(sys.argv[1]); gap = []; tot = 0
for line in open(f"fails_{n}.txt"):
    if not line.startswith("FAIL"): continue
    b = tuple(int(x) for x in line.split("=")[1].split()); tot += 1
    if lp_ok(b, n): gap.append(b)
print(n, "majorized multisets with no permutation:", tot, "| of these LP-feasible:", len(gap), gap[:5])
