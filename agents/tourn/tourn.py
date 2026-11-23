# gamma/delta of Davis-Schroeder. Tournaments as tuple beats[v] = bitmask of vertices v beats.
import sys, itertools
from functools import lru_cache
from collections import defaultdict

def witnesses(n):
    out=[]; phi=[0]*n
    def rec(i, usedc, useds):
        if i==n: out.append(tuple(phi)); return
        for v in range(n):
            if usedc>>v&1 or useds>>(i+v)&1: continue
            phi[i]=v; rec(i+1, usedc|1<<v, useds|1<<(i+v))
    rec(0,0,0); return out

def scores_of(phi):
    n=len(phi); c=sorted(i+phi[i] for i in range(n)); return tuple(c[j]-j for j in range(n))

def gamma(phi):
    """gamma(phi), vertices relabelled by rank of i+phi(i) (= score order)."""
    n=len(phi); order=sorted(range(n), key=lambda i:i+phi[i]); rk={v:r for r,v in enumerate(order)}
    beats=[0]*n
    for x in range(n):
        for y in range(n):
            if x==y: continue
            dom = x>y and phi[x]>phi[y]
            inv = (x-y)*(phi[x]-phi[y])<0
            if dom or (inv and x+phi[x] < y+phi[y]): beats[rk[x]] |= 1<<rk[y]
    return tuple(beats)

def svec(T): return tuple(bin(b).count('1') for b in T)

def valid_seqs(n):
    res=[]
    def rec(seq, tot):
        k=len(seq)
        if k==n:
            if tot==n*(n-1)//2: res.append(tuple(seq))
            return
        lo = seq[-1] if seq else 0
        for v in range(lo, n):
            t=tot+v; kk=k+1
            if t < kk*(kk-1)//2: continue
            if kk<n and t==kk*(kk-1)//2: continue  # tight cut
            if kk==n and t!=n*(n-1)//2: continue
            rec(seq+[v], t)
    rec([],0); return res

def count_tourn(s):
    """number of labelled tournaments with vertex j having score s[j]."""
    n=len(s)
    @lru_cache(None)
    def f(rem):
        # rem: residual scores of remaining vertices (tuple); peel vertex 0
        m=len(rem)
        if m==0: return 1
        r0=rem[0]; rest=rem[1:]
        tot=0
        for S in itertools.combinations(range(m-1), r0):  # vertices vertex0 beats
            Sset=set(S); new=[]
            ok=True
            for k in range(m-1):
                v=rest[k]-(0 if k in Sset else 1)
                if v<0 or v>m-2: ok=False;break
                new.append(v)
            if ok: tot+=f(tuple(new))
        return tot
    return f(tuple(s))

def tie_classes(s):
    cls=defaultdict(list)
    for j,v in enumerate(s): cls[v].append(j)
    return [c for c in cls.values()]

def relabel(T, p):  # p: old->new
    n=len(T); nb=[0]*n
    for x in range(n):
        b=T[x]; m=0
        for y in range(n):
            if b>>y&1: m|=1<<p[y]
        nb[p[x]]=m
    return tuple(nb)

def tie_perms(s):
    cls=tie_classes(s); n=len(s)
    for combo in itertools.product(*[itertools.permutations(c) for c in cls]):
        p=list(range(n))
        for c,pc in zip(cls,combo):
            for a,b in zip(c,pc): p[a]=b
        yield p

def canon_ties(T, s):
    return min(relabel(T,p) for p in tie_perms(s))

# ---------- direct delta (independent of gamma), for validation ----------
def delta(T):
    """Return phi (as list) if some tie-consistent T' makes T+T' have a TTD, else None. Vertices assumed score-sorted."""
    n=len(T); s=svec(T)
    for p in tie_perms(s):
        # T' = order where vertex x has rank p[x]
        w=[[0]*n for _ in range(n)]
        for x in range(n):
            for y in range(n):
                if x!=y: w[x][y]=(T[x]>>y&1)+(1 if p[x]>p[y] else 0)
        # find linear orders R1,R2 (as rank arrays) with [r1x>r1y]+[r2x>r2y]=w[x][y]
        # choose R1 by DFS as linear extension (build from bottom), R2 forced.
        r1=[None]*n
        res=_dfs(n,w,r1,0,0)
        if res is not None:
            r1,r2=res
            # vertex x: R1 rank r1[x], R2 rank r2[x]. phi(r1[x]) = r2[x]
            phi=[0]*n
            for x in range(n): phi[r1[x]]=r2[x]
            return phi
    return None

def _dfs(n,w,r1,placed,k):
    if k==n:
        # R2: x>y iff w==2 or (w==1 and r1[x]<r1[y])
        gt=[[ (w[x][y]==2) or (w[x][y]==1 and r1[x]<r1[y]) for y in range(n)] for x in range(n)]
        r2=[sum(gt[x][y] for y in range(n) if y!=x) for x in range(n)]
        if sorted(r2)!=list(range(n)): return None
        for x in range(n):
            for y in range(n):
                if x!=y and gt[x][y]!=(r2[x]>r2[y]): return None
        return r1[:],r2
    for x in range(n):
        if placed>>x&1: continue
        # x placed at rank k in R1 (above all placed): need no unplaced y with w[y][x]==2 (y above x in both)
        if any(not(placed>>y&1) and y!=x and w[x][y]==2 for y in range(n)): continue
        # placed y below x in R1: need w[x][y]>=1
        if any(placed>>y&1 and w[x][y]==0 for y in range(n)): continue
        r1[x]=k
        res=_dfs(n,w,r1,placed|1<<x,k+1)
        if res: return res
        r1[x]=None
    return None
