"""Which valid D fail the sorted list (right endpoints in order of value), its mirror (left endpoints in order of value), both?"""
import sys
from lib import *
for n in range(5, int(sys.argv[1]) + 1):
    V = valid_sets(n)
    fr = [D for D in V if decode(D) is None]
    fl = [D for D in V if decode(tuple(sorted(-x for x in D))) is None]
    both = sorted(set(fr) & set(fl))
    print(n, len(V), "fail sorted-right", len(fr), "fail sorted-left", len(fl), "fail both", len(both))
    for D in both[:int(sys.argv[2])]: print("    ", D, [D[i] - (2 * i - n + 1) for i in range(n)])
