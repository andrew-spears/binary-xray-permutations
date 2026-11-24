"""Peak lowering.  peak(x) = largest slack along the prefix x.  For a prefix x ending at slack s with last letter l,
is there a prefix x' ending at the same (s, l) with F(x') inside F(x) and a lower peak?  If F(x') is inside F(x)
then x'y solvable implies xy solvable, so x' is the harder beginning.
For every reachable set F at (s, l) (all prefixes with slacks <= B) this prints the smallest peak P such that F
contains F(x') for some x' with peak <= P, as  P - s  (0 = dominated by a prefix that never rises above its end).
Usage: python3 lowpeak.py B"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "interface"))
from rewrite import machine
def minpeaks(B):
    step, start = machine(B)
    peak = {(frozenset([start]), 0, None): 0}
    for P in range(0, B + 1):
        todo = list(peak)
        while todo:
            S, s, last = todo.pop()
            for e in range(0 if last is None else max(-s, last - 1), P - s + 1):
                x = (step(S, e), s + e, e)
                if x not in peak: peak[x] = P; todo.append(x)
    return peak
if __name__ == "__main__":
    B = int(sys.argv[1]); peak = minpeaks(B)
    by = {}
    for (S, s, l), p in peak.items():
        if l is not None: by.setdefault((s, l), []).append((p, S))
    worst = {}; examples = {}
    for (s, l), fam in by.items():
        fam.sort(key=lambda a: a[0])
        w = 0
        for p, S in fam:
            d = min(p2 for p2, S2 in fam if p2 <= p and S2 <= S)
            w = max(w, d - s)
        worst[(s, l)] = w
    ls = sorted({l for s, l in worst})
    print(f"B = {B}: rows = end slack s, columns = last letter {ls[0]}..{ls[-1]}; entry = worst (needed peak - s); '.' = no prefix")
    for s in range(0, B + 1):
        print(f"{s:3d}  " + " ".join(f"{worst[(s, l)]:2d}" if (s, l) in worst else " ." for l in ls))
