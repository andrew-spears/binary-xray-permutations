# Symmetric D = -D. Odd n=2m+1: L subset {1..2m}, |L|=m, Landau <=> top-K sums <= K(2m+1-K).
# Even n=2m: L subset {1..2m-1}, |L|=m, Landau <=> top-K sums <= K(2m-K).
import itertools, sys
from functools import lru_cache

def landau(L, N, strict=False):
    s=0
    for K,l in enumerate(sorted(L,reverse=True),1):
        s+=l
        b=K*(N-K)
        if s>b or (strict and s==b and K<len(L)): return False   # (strict only for K<m; K=m strict iff total not tight)
    return True

def pairings(L, N, hole=None, first_only=True):
    """partition {1..N} minus hole into pairs with differences exactly L. returns list of solutions (dict l->a)"""
    Ls=sorted(L,reverse=True); used=[False]*(N+2)
    if hole: used[hole]=True
    sols=[]
    # place by smallest free position: try each remaining l
    rem=set(L)
    def rec(assign):
        p=1
        while p<=N and used[p]: p+=1
        if p>N:
            sols.append(dict(assign)); return first_only
        for l in sorted(rem,reverse=True):
            q=p+l
            if q<=N and not used[q]:
                used[p]=used[q]=True; rem.discard(l); assign.append((l,p))
                if rec(assign): return True
                assign.pop(); rem.add(l); used[p]=used[q]=False
        return False
    rec([])
    return sols

def oddcase(m):
    N=2*m+1; out=[]
    for L in itertools.combinations(range(1,2*m+1),m):
        if not landau(L,N): continue
        holes=[f for f in range(1,N+1) if pairings(L,N,f)]
        out.append((L,holes))
    return out

if __name__=="__main__":
    M=int(sys.argv[1])
    for m in range(1,M+1):
        res=oddcase(m)
        bad=[L for L,h in res if not h]
        print(f"odd n={2*m+1}: valid symmetric L={len(res)}, no pairing={len(bad)}",bad[:5])
