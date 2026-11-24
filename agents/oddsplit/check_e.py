"""Independent check: every S that ext.crit calls an E-split is an odd split by brute force (output of ./dump n).
Usage: ./dump 8 > /tmp/os_8.txt; python3 check_e.py /tmp/os_8.txt"""
import sys
from ext import crit
nw = ne = bad = 0
for line in open(sys.argv[1]):
    a, b = line.split("|"); e = tuple(map(int, a.split())); ok = {int(t.split(":")[0]) for t in b.split()}; n = len(e); nw += 1
    for S in range(1, (1 << n) - 1):
        if crit(e, S):
            ne += 1
            if S not in ok: bad += 1
print(f"{nw} words, {ne} E-splits (word, S), not odd by brute force: {bad}")
