import itertools, sys
from collections import defaultdict
def run(n):
    W = defaultdict(list)
    for p in itertools.permutations(range(n)):
        ds=[p[i]-i for i in range(n)]
        if len(set(ds))==n: W[frozenset(ds)].append(p)
    v1=v2=v3=0; ex=None
    for D,wl in W.items():
        Ds=sorted(D)
        for a,b in zip(Ds,Ds[1:]):
            if b-a!=3: continue
            D2=(D-{a,b})|{a+1,b-1}; wl2=W[frozenset(D2)]
            r2=[{p[i]-i:i for i in range(n)} for p in wl2]
            for p in wl:
                rm={p[i]-i:i for i in range(n)}
                b1=min(sum(rm[d]!=q[d] for d in D if d not in(a,b)) for q in r2)
                b3=min(sum(rm[d]!=q[d] for d in D if d not in(a,b))+(rm[a]!=q[a+1])+(rm[b]!=q[b-1]) for q in r2)
                b2=min(sum(p[i]!=q[i] for i in range(n)) for q in wl2)
                if b1>v1: v1=b1; ex=(sorted(D),a,b,p)
                v2=max(v2,b2); v3=max(v3,b3)
    return v1,v2,v3,ex
for n in range(4,int(sys.argv[1])+1): print(n, run(n))
