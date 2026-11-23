"""Bounded letters: words with |e_k| <= c (scores within c of the transitive ones), slack <= B.
Does the summary (sigma, last L letters) carry an inductive invariant for every B once c is fixed?
Usage: python3 letters.py c Bmax [L ...]"""
import sys
from invariant import analyse
c = int(sys.argv[1]); Bmax = int(sys.argv[2]); Ls = [int(x) for x in sys.argv[3:]] or [1, 2, 3]
for L in Ls:
    for B in range(1, Bmax + 1):
        nodes, I, fails, allst = analyse(B, L, cap=c)
        frac = min((len(I[s]) / len(allst(s[0])) for s in nodes if s[0] > 0), default=1)
        print(f"c={c} L={L} B={B}: {len(nodes)} summaries, {'SUFFICES' if not fails else 'FAILS'}, min fraction {frac:.3f}", flush=True)
