"""ROW-BRIDGE: does the middle m carry a one-line hole pattern to a one-line hole pattern?  python3 rows.py N
start in {(s1|-), (-|s1)} (all the slack in one row / one column), end in {(s2|-), (-|s2)}."""
import sys
N = int(sys.argv[1]); sys.argv[1] = "0"
exec(open("oddbridge.py").read().split('if sys.argv[1] == "pairs"')[0])
def line(s): return [((s,), ()), ((), (s,)), ((1,) * s, ()), ((), (1,) * s)] if s else [E]
for n in range(5, N + 1):
    seen = set(); cnt = {}; none = []
    for w in words(n):
        t = split(w)
        if t is None or t in seen: continue
        seen.add(t); s1, m, s2 = t; hit = set()
        for a, u in enumerate(line(s1)):
            F = frozenset([u])
            for e in m: F = frozenset(v for x in F for k, v in l1.succs(x, e))
            for b, v in enumerate(line(s2)):
                if v in F: hit.add((a, b))
        for k in hit: cnt[k] = cnt.get(k, 0) + 1
        if not hit: none.append(t)
    print(f"n = {n}: triples {len(seen)}; no line-to-line walk: {len(none)}", none[:3], " by (start, end):", sorted(cnt.items()))
