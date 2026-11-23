import itertools, json
from functools import lru_cache
from exlib import valid, wits, Pn
from skel import maxblocks
def norm(seq):
    o=sorted(seq); return tuple(o.index(v)+1 for v in seq)
def decompose(p):
    n=len(p)
    for k in range(1,n):
        if set(p[:k])==set(range(1,k+1)): return (1,2),[norm(p[:k]),norm(p[k:])]
        if set(p[:k])==set(range(n-k+1,n+1)): return (2,1),[norm(p[:k]),norm(p[k:])]
    mx=maxblocks(p); segs=sorted(mx+[(i,i) for i in range(n) if not any(a<=i<=b for a,b in mx)])
    reps=[min(p[a:b+1]) for a,b in segs]; frame=norm(reps)
    return frame,[norm(p[a:b+1]) for a,b in segs]
FR=None
@lru_cache(None)
def buildable(p):
    if len(p)==1: return True
    f,bl=decompose(p)
    if f not in FR and f not in {(1,2),(2,1)}: return False
    return all(buildable(b) for b in bl)
def run(frames, NMAX=9):
    global FR; FR=set(map(tuple,frames)); buildable.cache_clear()
    res={}
    for n in range(4,NMAX+1):
        reach=[];miss=[];blk={"point":0,"built from set":0,"needs new frame":0}
        for D in itertools.combinations(range(-n+1,n),n):
            if not valid(D) or tuple(sorted(-x for x in D))<D: continue
            W=wits(D)
            ok=[p for p in W if buildable(p)]
            if ok: reach.append((D,len(W),ok[0]))
            else: miss.append((D,len(W),sorted(W)[0]))
            # block stats over witnesses whose top frame is in set
            for p in W:
                f,bl=decompose(p)
                if f in FR or f in {(1,2),(2,1)}:
                    if f==p: continue
                    for b in bl:
                        blk["point" if len(b)==1 else ("built from set" if buildable(b) else "needs new frame")]+=1
        res[n]=dict(reach=reach,miss=miss,blk=blk)
    return res
if __name__=="__main__":
    frames=[(1,2),(2,4,1,3),(4,2,5,1,3),(4,6,2,5,1,3),(5,2,6,4,1,3),(2,5,3,1,4),(5,7,3,6,1,4,2),(3,6,2,5,1,4),(6,3,7,5,1,4,2),(5,7,2,6,4,1,3),(5,7,2,4,6,1,3),(6,8,4,7,2,5,1,3),(3,1,5,2,4),(5,1,3,6,4,2),(3,6,1,4,2,5),(2,6,3,5,1,4),(5,2,6,3,1,4),(7,5,8,2,6,4,1,3),(5,2,4,6,1,3),(6,2,5,7,4,1,3),(5,7,3,1,6,4,2),(7,4,8,6,2,5,1,3),(6,8,3,7,5,1,4,2)]
    r=run(frames)
    for n,v in r.items(): print(n,"reached",len(v["reach"]),"missed",len(v["miss"]),v["blk"], [m[0] for m in v["miss"]][:8])
