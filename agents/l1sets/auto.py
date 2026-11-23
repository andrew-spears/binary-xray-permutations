"""The automaton of reachable sets for L1 prefixes inside slack <= S.  Node = distinct (F(x), slack); label: slack, Gamma = set of a + b on F,
ex = states of the 2-core saturation missing from F.  Prints each node with its three successors.
  python3 auto.py S"""
import sys
from cores import *
if __name__ == "__main__":
    nodes = sorted(seen, key=lambda k: (k[1], len(seen[k]), seen[k])); num = {k: i for i, k in enumerate(nodes)}
    for k in nodes:
        F, s = k; T, Pi = sat(F, s); G = sorted({a + b for a, b in Pi}); miss = T & ~F
        nx = []
        for e in (1, 0, -1):
            nx.append(f"{e:+d}->" + (str(num[step(F, s, e), s + e]) if 0 <= s + e <= S else "."))
        print(f"node {num[k]:3d}: s {s:2d} Gamma {G} |F| {bin(F).count('1')} ex[{bin(miss).count('1')}] {names(miss, s)[:70]} | {' '.join(nx)} | x = {''.join('+0-'[1 - e] for e in seen[k])}")
