import grammar as g, itertools, sys
from exlib import Ds, wits, Pn
def count_distinct(n):
    return sum(1 for p in itertools.permutations(range(1,n+1)) if g.ok(p))
def run(N,useP=True,stack=True,widen=True,slides=True):
    G={1:{(1,)}}
    for n in range(2,N+1):
        S={tuple(range(n,0,-1))}
        if useP:
            if n==2:S|={(2,1)}
            if n==3:S|={(1,3,2),(2,1,3)}
            if n>=4:S|=set(wits(Pn(n)))
        if stack:
          for a in range(1,n):
            b=n-a
            for t in G[a]:
                for bb in G[b]:
                    ws=["B"*b+"T"*a]
                    if slides:
                        ws+=["B"*(b-1)+"T"*s+"B"+"T"*(a-s) for s in range(1,a+1)]
                        ws+=["B"*(b-s)+"T"+"B"*s+"T"*(a-1) for s in range(1,b+1)]
                    for w in ws:
                        p=g.build(t,bb,w)
                        if g.ok(p):S.add(p)
        if widen:
          for k in range(2,n):
            for f in G[k]:
                for sz in g.compositions(n,k):
                    for bl in itertools.product(*[G[m] for m in sz]):
                        p=g.inflate(f,bl)
                        if g.ok(p):S.add(p)
        G[n]=S
    return G
def cover(G,n):
    m=0;t=0
    for D in Ds(n):
        if tuple(sorted(-x for x in D))<D: continue
        t+=1
        if not any(w in G[n] for w in wits(D)): m+=1
    return m,t
N=8
print("distinct-diagonal perms:",[count_distinct(n) for n in range(4,N+1)])
for name,kw in [("full",{}),("no P pieces",dict(useP=False)),("no widening",dict(widen=False)),("no slides",dict(slides=False)),("no stacking",dict(stack=False))]:
    G=run(N,**kw); print(name,"|G|",[len(G[n]) for n in range(4,N+1)],"missed",[cover(G,n) for n in range(6,N+1)],flush=True)
