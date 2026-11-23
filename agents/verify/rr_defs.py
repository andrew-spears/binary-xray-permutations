# Part 3: repair radius R(n) under several definitions. Brute force over all perms.
import itertools, sys
import numpy as np
from math import comb
from collections import defaultdict
def tight(D,n):
    ps=0
    for k in range(1,n):
        ps+=D[k-1]+n-k
        if ps==comb(k,2): return True
    return False
GAP3=int(sys.argv[2]) if len(sys.argv)>2 else 0
def run(n):
    W=defaultdict(list)
    for p in itertools.permutations(range(n)):
        ds=[p[i]-i for i in range(n)]
        if len(set(ds))==n: W[tuple(sorted(ds))].append(p)
    # row-of-diagonal arrays indexed by mark d+(n-1)
    R={}
    for D,wl in W.items():
        a=np.full((len(wl),2*n-1),-1)
        for j,p in enumerate(wl):
            for i in range(n): a[j,p[i]-i+n-1]=i
        R[D]=a
    res=defaultdict(int)
    for D in W:
        Dset=set(D)
        for a,b in [(x,y) for x in D for y in D if y-x>=3]:
            if (a+1 in Dset) or (b-1 in Dset) or any(z not in Dset for z in range(a+2,b-1)): continue
            gap="g3" if b-a==3 else "glong"
            if GAP3 and gap!="g3": continue
            D2=tuple(sorted(set(D)-{a,b}|{a+1,b-1}))
            nt=(not tight(D,n), not tight(D2,n))
            fixed=[d+n-1 for d in D if d not in (a,b)]
            for direction,(X,Y,mv) in (("in",(R[D],R[D2],[(a,a+1),(b,b-1)])),("out",(R[D2],R[D],[(a+1,a),(b-1,b)]))):
                # mismatch over fixed stones: |X| x |Y|
                A=(X[:,None,fixed]!=Y[None,:,fixed]).sum(2)
                # moving stone kept row (stone slid along its row)
                MR=sum((X[:,None,u+n-1]!=Y[None,:,v+n-1]).astype(int) for u,v in mv)
                # moving stone kept column: col = row+d
                MC=sum(((X[:,None,u+n-1]+u)!=(Y[None,:,v+n-1]+v)).astype(int) for u,v in mv)
                metrics={"A_fixed_pts":A, "B_rows(=A+2)":A+2, "C_A+movers_row":A+MR, "C'_A+movers_col":A+MC}
                for scope,ok in (("all",True),("ntc_both",nt[0] and nt[1]),("ntc_src",(nt[0] if direction=="in" else nt[1])),("ntc_either",nt[0] or nt[1])):
                    if not ok: continue
                    for mname,M in metrics.items():
                        v=int(M.min(1).max())          # any witness pi
                        k1=(scope,direction,mname,"anyπ"); res[k1]=max(res[k1],v)
                        k2=(scope,"both",mname,"anyπ"); res[k2]=max(res[k2],v)
                        v0=int(M[0].min())             # pi restricted to lexicographically first witness
                        k3=(scope,direction,mname,"firstπ"); res[k3]=max(res[k3],v0)
                        vb=int(M.min())                # best pi (min over pi too)
                        k4=(scope,direction,mname,"bestπ"); res[k4]=max(res[k4],vb)
    return res
N=int(sys.argv[1])
allres={n:run(n) for n in range(4,N+1)}
keys=sorted(set().union(*[r.keys() for r in allres.values()]))
for k in keys:
    print(" | ".join(k).ljust(55), [allres[n].get(k,"-") for n in range(4,N+1)], flush=True)
