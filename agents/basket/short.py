import grammar as g, itertools
from exlib import Ds, wits, Pn
from nearP import three_cycles
def run(N,maxs):
    G={1:{(1,)}}
    for n in range(2,N+1):
        S={tuple(range(n,0,-1))}
        if n==2:S|={(2,1)}
        if n==3:S|={(1,3,2),(2,1,3)}
        if n>=4:S|=set(wits(Pn(n)))
        for a in range(1,n):
            b=n-a
            ws=["B"*b+"T"*a]+["B"*(b-1)+"T"*s+"B"+"T"*(a-s) for s in range(1,min(a,maxs)+1)]+["B"*(b-s)+"T"+"B"*s+"T"*(a-1) for s in range(1,min(b,maxs)+1)]
            for t in G[a]:
                for bb in G[b]:
                    for w in ws:
                        p=g.build(t,bb,w)
                        if g.ok(p):S.add(p)
        for k in range(2,n):
            for f in G[k]:
                for sz in g.compositions(n,k):
                    for bl in itertools.product(*[G[m] for m in sz]):
                        p=g.inflate(f,bl)
                        if g.ok(p):S.add(p)
        G[n]=S
    return G
G=run(9,2)
for n in range(6,10):
    P=three_cycles(Pn(n)); by={}
    for D in Ds(n):
        if tuple(sorted(-x for x in D))<D: continue
        L=three_cycles(D)-P; c=any(w in G[n] for w in wits(D))
        x=by.setdefault(L,[0,0]); x[0]+=c; x[1]+=1
    print(n,"|G|",len(G[n]),"covered/total by layer:",{L:tuple(v) for L,v in sorted(by.items())},flush=True)
print("misses:")
for n in range(6,10):
    P=three_cycles(Pn(n))
    for D in Ds(n):
        if tuple(sorted(-x for x in D))<D: continue
        if not any(w in G[n] for w in wits(D)): print(n,"layer",three_cycles(D)-P,D,"W",len(wits(D)),wits(D)[:3])
