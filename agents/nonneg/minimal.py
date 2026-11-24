"""For each (end slack s, last letter l): the inclusion-minimal reachable sets F(x), and a shortest / lowest-peak
word for each.  Usage: python3 minimal.py B [smax]"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "interface"))
from rewrite import machine
def explore(B):
    step, start = machine(B)
    word = {(frozenset([start]), 0, None): ()}
    for P in range(0, B + 1):                 # peak by peak, breadth first inside a peak: lowest peak, then shortest
        layer = list(word)
        while layer:
            nxt = []
            for S, s, last in layer:
                w = word[(S, s, last)]
                for e in range(0 if last is None else max(-s, last - 1), P - s + 1):
                    x = (step(S, e), s + e, e)
                    if x not in word: word[x] = w + (e,); nxt.append(x)
            layer = nxt
    return word
if __name__ == "__main__":
    B = int(sys.argv[1]); smax = int(sys.argv[2]) if len(sys.argv) > 2 else B
    word = explore(B); by = {}
    for (S, s, l), w in word.items():
        if l is not None: by.setdefault((s, l), []).append((S, w))
    for (s, l) in sorted(by):
        if s > smax or s == 0 or l < 0: continue
        fam = by[(s, l)]
        mins = [(S, w) for S, w in fam if not any(S2 < S for S2, _ in fam)]
        print(f"slack {s} last {l}: {len(fam)} sets, {len(mins)} minimal:", "  ".join("".join(str(e) if e >= 0 else "m" + str(-e) for e in w) for _, w in sorted(mins, key=lambda a: (len(a[1]), a[1]))[:8]))
