import itertools
from nearP import Psol, moves, three_cycles
from exlib import valid, wits, Pn
def chain(pieces, slides):
    """pieces top to bottom, skew stacked; slides[j] = how far the lower piece's top column moves right past the upper piece at cut j"""
    k=len(pieces); sizes=[len(p) for p in pieces]
    # column order as list of (piece, rank): bottom piece leftmost
    order=[]
    for j in reversed(range(k)):
        order+=[(j,r) for r in range(1,sizes[j]+1)]
    for j,s in enumerate(slides):           # cut between piece j (upper) and j+1 (lower)
        if s<0:
            up=(j,1); i=order.index(up)
            for _ in range(-s):
                if i==0 or order[i-1][0]!=j+1: return None
                order[i],order[i-1]=order[i-1],order[i]; i-=1
            continue
        lo=(j+1,sizes[j+1]); i=order.index(lo)
        for _ in range(s):
            if i+1>=len(order): return None
            nxt=order[i+1]
            if nxt[0]!=j: return None
            order[i],order[i+1]=order[i+1],order[i]; i+=1
    col={pr:c+1 for c,pr in enumerate(order)}
    perm=[]
    for j,p in enumerate(pieces): perm+=[col[(j,c)] for c in p]
    return tuple(perm)
def comps(n,parts):
    if parts==1:
        if n in Psol: yield (n,)
        return
    for a in range(1,n):
        if a in Psol:
            for rest in comps(n-a,parts-1): yield (a,)+rest
def find(D,maxparts=4,S=(1,2)):
    n=len(D);res=[]
    for k in range(2,maxparts+1):
        for c in comps(n,k):
            for pcs in itertools.product(*[Psol[a] for a in c]):
                for sl in itertools.product(S,repeat=k-1):
                    p=chain(pcs,sl)
                    if p and tuple(sorted(p[i]-i-1 for i in range(n)))==tuple(D): res.append((k,pcs,sl,p))
        if res: return res
    return res
if __name__=="__main__":
    for D in [(-6,-4,-3,-2,2,3,4,6),(-7,-6,-3,-2,-1,3,4,5,7),(-7,-5,-4,-3,0,3,4,5,7),(-8,-7,-5,-2,-1,0,4,5,6,8),(-8,-6,-5,-4,-1,1,4,5,6,8)]:
        r=find(D,5,(-3,-2,-1,1,2,3)); print(D,len(wits(D)),"->",r[:2] if r else "none")
