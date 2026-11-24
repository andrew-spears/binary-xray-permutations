"""Test: for every nonnegative-letter prefix x, the states (-|sorted letters of x) and (-|conjugate of the sorted column
lengths of theta(x)) have an odd number of placements.  Also the family  k..1 0^j -1..-k  via look-alike check of PAR.
Usage: python3 extreme.py LEN SLACK"""
import sys
from parity import words
from par_lib import odd_states, conj
LEN, S = int(sys.argv[1]), int(sys.argv[2]); n = bad = 0
for x in words(LEN, S, False):
    if sum(x) == 0: continue
    rows = tuple(sorted((e for e in x if e), reverse=True))
    width = max(k + e for k, e in enumerate(x, 1))
    cols = tuple(sorted((c for c in (sum(1 for k, e in enumerate(x, 1) if k <= j < k + e) for j in range(1, width + 1)) if c), reverse=True))
    O = odd_states(x); n += 1
    if ((), rows) not in O or ((), conj(cols)) not in O: bad += 1; print("FAIL", x)
print(f"{n} prefixes (letters >= 0, length <= {LEN}, slack <= {S}): extreme states not odd for {bad}")
