# Two explicit families (REPORT section 4), checked with lib.check (lines and width).
#  S(k, 1) = k..1 0 -1..-k            : two blocks, two chains.
#  S(k, (k+1)/2), k = 2b+1 odd        : five blocks, three chains (the picture 6 7 8 | 4 5 | 11 12 13 | 9 10 | 1 2 3 for k = 5).
# Usage: python3 fam.py K
import sys
from lib import *
def stair(k, j): return tuple(list(range(k, 0, -1)) + [0] * j + list(range(-1, -k - 1, -1)))
K = int(sys.argv[1]); bad = 0
for k in range(1, K + 1):
    pi = list(range(k, 2 * k + 1)) + list(range(k))
    bad += not check(stair(k, 1), pi, 2)
    if k % 2:
        b = k // 2; c = b + 1
        pi = [c + b + t for t in range(b + 1)] + [c + t for t in range(b)] + [c + k + b + t for t in range(b + 1)] + [c + k + t for t in range(b)] + list(range(c))
        bad += not check(stair(k, c), pi, 3)
        if k == 5: print("k = 5:", fmt(pi))
print("k <= %d: failures %d" % (K, bad))
