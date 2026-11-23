import grammar as g, sys
from exlib import Ds, wits
def run(N,neg=True,pos=True,maxs=99):
    G={1:{(1,)}}
    for n in range(2,N+1):
        S=set()
        for a in range(1,n):
            b=n-a
            ws=["B"*b+"T"*a]
            if pos: ws+=["B"*(b-1)+"T"*s+"B"+"T"*(a-s) for s in range(1,min(a,maxs)+1)]
            if neg: ws+=["B"*(b-s)+"T"+"B"*s+"T"*(a-1) for s in range(1,min(b,maxs)+1)]
            for t in G[a]:
                for bb in G[b]:
                    for w in ws:
                        p=g.build(t,bb,w)
                        if g.ok(p):S.add(p)
        G[n]=S
    return G
def cover(G,n):
    miss=[];t=0
    for D in Ds(n):
        if tuple(sorted(-x for x in D))<D: continue
        t+=1
        if not any(w in G[n] for w in wits(D)): miss.append(D)
    return len(miss),t,miss[:3]
if __name__=='__main__':
 N=int(sys.argv[1])
 for name,kw in [("both slides",{}),("bottom-right slides only",dict(neg=False)),("slide<=2",dict(maxs=2)),("slide<=1",dict(maxs=1))]:
    G=run(N,**kw); print(name,[len(G[n]) for n in range(4,N+1)],[cover(G,n)[:2] for n in range(6,N+1)],flush=True)
