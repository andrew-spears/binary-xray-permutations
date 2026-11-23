"""List every rule u -> v (|u| < |v| <= Lmax, same letter sum) that is valid at bound B (F(xu) inside F(xv) in every
situation where both are legal with slacks <= B), in the format read by ./rules.   Usage: python3 enum_rules.py B Lmax > rules.txt"""
import sys
from collections import defaultdict
sys.path.insert(0, "../interface")
from rewrite import machine
def main(B, Lmax):
    step, start = machine(B)
    s0 = (frozenset([start]), 0, None); seen = {s0}; todo = [s0]
    while todo:
        S, s, last = todo.pop()
        for e in range(0 if last is None else max(-s, last - 1), B - s + 1):
            x = (step(S, e), s + e, e)
            if x not in seen: seen.add(x); todo.append(x)
    tested = defaultdict(int); failed = set()
    for S, s, last in seen:
        ext = {}
        def rec(w, S2, s2, l2):
            ext[w] = S2
            if len(w) == Lmax: return
            for e in range(0 if l2 is None else max(-s2, l2 - 1), B - s2 + 1): rec(w + (e,), step(S2, e), s2 + e, e)
        rec((), S, s, last)
        bysum = defaultdict(list)
        for w in ext: bysum[sum(w)].append(w)
        for ws in bysum.values():
            for u in ws:
                for v in ws:
                    if len(u) < len(v) and (u, v) not in failed:
                        tested[(u, v)] += 1
                        if not ext[u] <= ext[v]: failed.add((u, v))
    rules = sorted(r for r in tested if r not in failed)
    print(f"B = {B}: {len(seen)} situations; {len(rules)} valid of {len(tested)}", file=sys.stderr)
    f = lambda w: " ".join(map(str, w))
    for u, v in rules: print(f"{f(u)}>{f(v)} : {f(u)} | {f(v)}")
if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))
