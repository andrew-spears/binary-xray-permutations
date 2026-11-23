"""Item 3 test: does an RR-split survive inserting a letter 0 (the step x y -> x 0 y)?
For every valid word e of length n without a tight cut and every place where a 0 can be inserted, ask whether some RR-split S of e
gives an RR-split of the longer word when the new stone is put in S or in S^c.   Usage: python3 transfer.py n"""
import sys
from ext import words, parts, shape, conj, splits
def rr(e, S):
    if S == 0 or S == (1 << len(e)) - 1: return False
    w1, w2 = parts(e, S)
    if min(w1) < 0 or min(w2) < 0: return False
    return splits(conj(shape(w2)[0]), shape(w1)[0])
n = int(sys.argv[1]); tot = keep = has = 0; ex = []; ns = n0 = n1 = ne = 0; pk = pkeep = 0
for e in words(n, False):
    if not any(e) or any(sum(e[:k]) == 0 for k in range(1, n)): continue
    good = [S for S in range(1, (1 << n) - 1) if rr(e, S)]
    for i in range(1, n):
        if e[i - 1] > 1 or e[i] < -1: continue
        f = e[:i] + (0,) + e[i:]; tot += 1; ok = False
        for S in good:
            lo = S & ((1 << i) - 1); hi = S >> i
            a = rr(f, lo | hi << (i + 1)); b = rr(f, lo | 1 << i | hi << (i + 1))
            ns += 1; n0 += a; n1 += b; ne += a or b; ok = ok or a or b
        keep += ok
        if not ok and len(ex) < 3: ex.append((e, i))
# PEAK: a letter 0 at position i replaced by (1, 0, -1); S of the short word away from i, any choice on the three new stones
for e in words(n, False):
    if not any(e) or any(sum(e[:k]) == 0 for k in range(1, n)): continue
    good = {S for S in range(1, (1 << n) - 1) if rr(e, S)}
    for i in range(n):
        if e[i] != 0: continue
        f = e[:i] + (1, 0, -1) + e[i + 1:]; pk += 1; ok = False
        for S in good:
            lo = S & ((1 << i) - 1); hi = S >> (i + 1)
            if any(rr(f, lo | t << i | hi << (i + 3)) for t in range(8)): ok = True; break
        pkeep += ok
print(f"n = {n}: PEAK steps 0 -> (1,0,-1): {pk}; some RR-split of the short word extends: {pkeep}")
print(f"n = {n}: pairs (insertion, RR-split S): {ns}; extends with the new stone in S^c: {n0}, in S: {n1}, either: {ne}")
print(f"n = {n}: {tot} insertions of a 0 into words without a tight cut; some RR-split of the short word extends: {keep}; examples where none does: {ex}")
