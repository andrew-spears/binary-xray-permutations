import itertools, json
from exlib import valid, wits, Pn
from skel import skeleton, maxblocks
chosen=[(1,2),(2,4,1,3),(4,2,5,1,3),(2,5,3,1,4),(3,1,5,2,4),(4,6,2,5,1,3),(5,2,6,4,1,3),(3,6,2,5,1,4),(5,7,3,6,1,4,2),(6,3,7,5,1,4,2)]
best={}
for n in range(4,10):
    for D in itertools.combinations(range(-n+1,n),n):
        if not valid(D) or D==Pn(n) or tuple(sorted(-x for x in D))<D: continue
        for p in wits(D):
            s=skeleton(p)
            if s in chosen and s not in best and s!=p:
                mx=maxblocks(p) if s!="linear" else []
                # block rectangles
                bl=[(a+1,b+1,min(p[a:b+1]),max(p[a:b+1])) for a,b in mx]
                best[s]=(D,p,bl)
for s in chosen:
    if s in best: print(s, best[s])
json.dump({",".join(map(str,s)):[list(best[s][0]),list(best[s][1]),best[s][2]] for s in chosen if s in best},open("frame_ex.json","w"))
