"""Min over witnesses of #distinct anti-diagonals i+pi(i) (lines of slope -1). Usage: python3 antidiag.py n"""
import sys
from collections import Counter
from common import *
n=int(sys.argv[1]); cnt=Counter(); ex={}
for line in open(f"uncovered_{n}.txt"):
    D=sorted(eval(line.split("  ")[0])); best=[n+1,None]; p=[0]*n
    def rec(i,uD,uC,S):
        if len(S)>=best[0]: return
        if i==n: best[0],best[1]=len(S),tuple(p); return
        for j,d in enumerate(D):
            if uD>>j&1: continue
            c=i+1+d
            if 1<=c<=n and not uC>>c&1:
                p[i]=c; rec(i+1,uD|1<<j,uC|1<<c,S|{2*(i+1)+d})
    rec(0,0,0,frozenset()); cnt[best[0]]+=1; ex.setdefault(best[0],[]).append((D,best[1]))
print(n,dict(sorted(cnt.items())))
for k in sorted(ex):
    for D,w in ex[k][:2]: print(" ",k,D,w,[i+1+w[i] for i in range(n)])
