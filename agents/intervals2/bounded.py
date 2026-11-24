"""Bounded slack, every n.  For a legal prefix x (letters e_1.., e_1 >= 0, e_i >= e_{i-1} - 1, all partial sums >= 0)
let F(x) = set of partitions the partition machine (../intervals/pm.py) can be in after reading x.
F(x e) depends only on F(x) and e, and the letters allowed after x depend only on the slack and the last letter.
So the pairs (F(x), last letter of x) over ALL legal prefixes whose slack never exceeds B form a finite set, computed
here by closure.  If no pair has F empty, then every valid D (any n) whose slack never exceeds B has an interval order.
usage: python3 bounded.py B        (B = 20: about 2 minutes)"""
import sys, time
sys.path.insert(0, "../intervals")
from pm import succ
def closure(B):
    ids = {(): 0}; parts = [()]; size = [0]; table = {}
    def nxt(i, e):
        key = (i, e)
        if key not in table:
            out = []
            for v in succ(parts[i], e):
                if v not in ids: ids[v] = len(parts); parts.append(v); size.append(sum(v))
                out.append(ids[v])
            table[key] = tuple(out)
        return table[key]
    start = (frozenset({0}), None)
    seen = {start: None}; stack = [start]; first = True
    while stack:
        F, e = stack.pop(); s = size[next(iter(F))]
        lo = 0 if e is None else max(e - 1, -s)
        for e2 in range(lo, B - s + 1):
            G = frozenset().union(*[nxt(i, e2) for i in F])
            if not G: return None, (F, e, e2), parts
            if (G, e2) not in seen: seen[(G, e2)] = (F, e); stack.append((G, e2))
    return seen, None, parts
if __name__ == "__main__":
    B = int(sys.argv[1]); t = time.time(); seen, bad, parts = closure(B)
    if seen is None:
        print("B =", B, ": STUCK", [parts[i] for i in bad[0]], bad[1:]); sys.exit(1)
    print(f"B = {B}: {len(seen)} pairs (F, last letter), {len({F for F, e in seen})} distinct sets F, largest has "
          f"{max(len(F) for F, e in seen)} partitions; none empty.  ({time.time() - t:.0f} s)")
    by = {}
    for F in {F for F, e in seen}:
        s = sum(parts[next(iter(F))]); by[s] = by.get(s, 0) + 1
    print("   distinct sets F by slack 0..%d:" % B, [by.get(s, 0) for s in range(B + 1)])
