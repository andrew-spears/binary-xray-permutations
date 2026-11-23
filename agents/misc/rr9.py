import itertools, sys
from collections import defaultdict
n=int(sys.argv[1])
W=defaultdict(list)
for p in itertools.permutations(range(n)):
    ds=[p[i]-i for i in range(n)]
    if len(set(ds))==n: W[frozenset(ds)].append(tuple(ds.index(d) if False else 0 for d in ()) or p)
v1=0; ex=None
for D,wl in W.items():
    Ds=sorted(D)
    for a,b in zip(Ds,Ds[1:]):
        if b-a!=3: continue
        D2=(D-{a,b})|{a+1,b-1}; wl2=W[frozenset(D2)]
        others=[d for d in Ds if d not in(a,b)]
        # row vector of non-moving stones
        def rows(p): 
            inv={p[i]-i:i for i in range(n)}; return tuple(inv[d] for d in others)
        R2=list({rows(q) for q in wl2})
        for p in wl:
            r=rows(p)
            best=min(sum(x!=y for x,y in zip(r,q)) for q in R2)
            if best>v1: v1=best; ex=(Ds,a,b,p)
print(n,v1,ex)
