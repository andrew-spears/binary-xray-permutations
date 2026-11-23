# Grammar G (row->column permutations, all pieces must have distinct diagonals):
#  base: P_k solutions (k>=4), 1, 21, 132, 213, and anti-diagonals k..1
#  stack: top piece over bottom piece, one column displaced (bottom's rightmost slid right by s, or top's leftmost slid left by s); s=0 is plain skew stack
#  widen: frame in G with each point replaced by a block in G
import itertools, sys, pickle
from exlib import valid, wits, Pn
def dg(p): return [p[i]-i-1 for i in range(len(p))]
def ok(p): d=dg(p); return len(set(d))==len(d)
def build(t,bb,w):
    Tc=[i+1 for i,ch in enumerate(w) if ch=="T"]; Bc=[i+1 for i,ch in enumerate(w) if ch=="B"]
    return tuple(Tc[c-1] for c in t)+tuple(Bc[c-1] for c in bb)
def inflate(f,blocks):
    # f row->col, blocks[i] placed at point (i, f[i])
    k=len(f); sz=[len(b) for b in blocks]
    rowoff=[sum(sz[:i]) for i in range(k)]
    colsz={f[i]:sz[i] for i in range(k)}
    coloff={c:sum(colsz[x] for x in range(1,c)) for c in range(1,k+1)}
    p=[0]*sum(sz)
    for i in range(k):
        for r,c in enumerate(blocks[i]): p[rowoff[i]+r]=coloff[f[i]]+c
    return tuple(p)
def compositions(n,k):
    for cuts in itertools.combinations(range(1,n),k-1):
        b=(0,)+cuts+(n,); yield [b[i+1]-b[i] for i in range(k)]
def gen(N):
    G={1:{(1,)}}
    base={2:{(2,1)},3:{(1,3,2),(2,1,3),(3,2,1)}}
    for n in range(2,N+1):
        S=set(base.get(n,set())); S.add(tuple(range(n,0,-1)))
        if n>=4: S|=set(wits(Pn(n)))
        for a in range(1,n):
            b=n-a
            for t in G[a]:
                for bb in G[b]:
                    words=["B"*b+"T"*a]
                    words+=["B"*(b-1)+"T"*s+"B"+"T"*(a-s) for s in range(1,a+1)]
                    words+=["B"*(b-s)+"T"+"B"*s+"T"*(a-1) for s in range(1,b+1)]
                    for w in words:
                        p=build(t,bb,w)
                        if ok(p): S.add(p)
        for k in range(2,n):
            for f in G[k]:
                for sz in compositions(n,k):
                    for bl in itertools.product(*[G[m] for m in sz]):
                        p=inflate(f,bl)
                        if ok(p): S.add(p)
        G[n]=S; print(n,len(S),file=sys.stderr,flush=True)
    return G
if __name__=="__main__":
    N=int(sys.argv[1]); G=gen(N); pickle.dump(G,open(f"G{N}.pkl","wb"))
