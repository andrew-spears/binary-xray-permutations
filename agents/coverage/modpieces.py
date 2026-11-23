"""Min #pieces where a piece = contiguous run with constant step mod M (M=0 means plain AP).
Usage: python3 modpieces.py n M"""
import sys
from collections import Counter
from common import *
n=int(sys.argv[1]); M=int(sys.argv[2])
eq=(lambda x,y: x==y) if M==0 else (lambda x,y:(x-y)%M==0)
cnt=Counter(); ex={}
for line in open(f"uncovered_{n}.txt"):
    D=sorted(eval(line.split("  ")[0])); best=[n+1,None]; p=[0]*n
    def rec(i,uD,uC,pc,pl,st):
        if pc>=best[0]: return
        if i==n: best[0],best[1]=pc,tuple(p); return
        for j,d in enumerate(D):
            if uD>>j&1: continue
            c=i+1+d
            if 1<=c<=n and not uC>>c&1:
                p[i]=c
                if i==0: a=(1,1,None)
                elif pl==1: a=(pc,2,c-p[i-1])
                elif eq(c-p[i-1],st): a=(pc,pl+1,st)
                else: a=(pc+1,1,None)
                rec(i+1,uD|1<<j,uC|1<<c,*a)
    rec(0,0,0,0,0,None); cnt[best[0]]+=1; ex.setdefault(best[0],[]).append((D,best[1]))
print(n,M,dict(sorted(cnt.items())))
for k in sorted(ex):
    for D,w in ex[k][:2]: print(" ",k,D,w)
