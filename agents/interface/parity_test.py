"""How much of the reachable set F(x) is explained by parity?  (T9: describe the reachable / alive sets.)
Reflected coordinates: stone j sits at (r, c) with r + c = 2j + e_j.  A stone with even sum has r, c of equal parity
(class OO or EE), with odd sum opposite parity (OE or EO).  For a state (R, C) after a prefix with z even and p odd letters:
     #OO = (|R odd| + |C odd| - p) / 2,   #EE = z - #OO,   #OE = (p + |R odd| - |C odd|) / 2,   #EO = p - #OE.
(P)  all four are non-negative integers.                                                     [necessary, proved]
(S)  some split of the stones into the four classes with these sizes passes, in each class, the sum test
     'the j smallest sums of the class >= the j smallest rows + the j smallest columns of the right parity', and the
     same with largest and <=.  (The rows of one parity are shared by two classes, so there is no equality at the end.)
                                                                                             [necessary, proved]
For every legal prefix x with at most K letters and slacks <= B this prints |all states|, |(P)|, |(S)|, |F(x)| summed over
prefixes, and the first prefixes where (S) is not exact.
Usage: python3 parity_test.py B K [l1]"""
import sys
from itertools import combinations
from rewrite import machine
def rows_of(mask, k, B):
    return [r for r in range(1, k - B + 1)] + [k + 1 + i - B for i in range(2 * B + 1) if mask >> i & 1 and k + 1 + i - B >= max(1, k - B + 1)]
def sumtest(R, C, T):
    """T sorted sums of one class; R, C all used rows / columns of the right parity (the class uses len(T) of each)"""
    m = len(T)
    if m > len(R) or m > len(C): return False
    a = b = 0
    for i in range(m):
        a += T[i] - R[i] - C[i]; b += T[m - 1 - i] - R[len(R) - 1 - i] - C[len(C) - 1 - i]
        if a < 0 or b > 0: return False
    return True
def S_ok(R, C, sums):
    Ro = [r for r in R if r & 1]; Re = [r for r in R if not r & 1]; Co = [c for c in C if c & 1]; Ce = [c for c in C if not c & 1]
    ev = [t for t in sums if not t & 1]; od = [t for t in sums if t & 1]
    p, z = len(od), len(ev)
    if (len(Ro) + len(Co) - p) % 2: return 0
    a = (len(Ro) + len(Co) - p) // 2; b = z - a; c = (p + len(Ro) - len(Co)) // 2; d = p - c
    if min(a, b, c, d) < 0: return 0
    okE = False
    for A in combinations(range(z), a):
        As = set(A)
        if sumtest(Ro, Co, [ev[i] for i in A]) and sumtest(Re, Ce, [ev[i] for i in range(z) if i not in As]): okE = True; break
    if not okE: return 1
    for A in combinations(range(p), c):
        As = set(A)
        if sumtest(Ro, Ce, [od[i] for i in A]) and sumtest(Re, Co, [od[i] for i in range(p) if i not in As]): return 2
    return 1
if __name__ == "__main__":
    B, K = int(sys.argv[1]), int(sys.argv[2]); l1 = len(sys.argv) > 3
    step, start = machine(B)
    # all masks (window patterns) by slack: closure under single steps
    seen = {start}; todo = [start]
    def slack(st): return sum(sum(i for i in range(2 * B + 2) if m >> i & 1) - B * (B - 1) // 2 for m in st)
    while todo:
        a = todo.pop()
        for e in range(-B, B + 1):
            for b in step(frozenset([a]), e):
                if b not in seen and slack(b) <= B: seen.add(b); todo.append(b)
    bysl = {}
    for a in seen: bysl.setdefault(slack(a), []).append(a)
    tot = [0, 0, 0, 0]; shown = 0; nw = 0
    stack = [((), frozenset([start]), 0)]
    while stack:
        w, F, s = stack.pop(); k = len(w)
        if k:
            nw += 1; sums = [2 * (j + 1) + e for j, e in enumerate(w)]
            for st in bysl.get(s, []):
                low = (1 << max(0, B - k)) - 1          # window positions that are rows <= 0 must be 'used'
                if st[0] & low != low or st[1] & low != low: continue
                v = S_ok(rows_of(st[0], k, B), rows_of(st[1], k, B), sums)
                tot[0] += 1; tot[1] += v >= 1; tot[2] += v == 2; tot[3] += st in F
                if st in F and v < 2: print("BUG: reachable state fails a necessary test", w, st); sys.exit(1)
                if v == 2 and st not in F and shown < 6:
                    shown += 1; print(f"  passes (S) but not reachable: word {w}, rows {rows_of(st[0], k, B)}, cols {rows_of(st[1], k, B)}")
        if k == K: continue
        lo = 0 if not w else max(-s, w[-1] - 1)
        for e in range(lo, B - s + 1):
            if l1 and abs(e) > 1: continue
            stack.append((w + (e,), step(F, e), s + e))
    print(f"B = {B}, prefixes of length <= {K}{' (letters -1,0,1)' if l1 else ''}: {nw} prefixes; states {tot[0]}, pass (P) {tot[1]}, pass (S) {tot[2]}, reachable {tot[3]}")
