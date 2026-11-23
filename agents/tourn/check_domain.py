# exhaustive check: delta accepts T  <=>  T in tie-closure of gamma-image  (n<=6)
import sys; sys.path.insert(0,'/home/claude/agents/tourn')
from tourn import *
for n in range(2,int(sys.argv[1])+1):
    img=set(canon_ties(gamma(p),scores_of(p)) for p in witnesses(n))
    pairs=[(x,y) for x in range(n) for y in range(x+1,n)]
    tot=acc=mism=0
    for m in range(1<<len(pairs)):
        b=[0]*n
        for k,(x,y) in enumerate(pairs):
            if m>>k&1: b[x]|=1<<y
            else: b[y]|=1<<x
        T=tuple(b); s=svec(T)
        if list(s)!=sorted(s): continue
        tot+=1; d=delta(T) is not None; g=canon_ties(T,s) in img
        acc+=d; mism+=(d!=g)
    print(n,"sorted-labelled tournaments",tot,"accepted",acc,"mismatch delta vs gamma-image",mism,flush=True)
