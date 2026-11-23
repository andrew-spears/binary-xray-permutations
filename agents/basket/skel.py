from exlib import wits
def maxblocks(p):
    n=len(p); iv=[(i,j) for i in range(n) for j in range(i+1,n) if max(p[i:j+1])-min(p[i:j+1])==j-i and j-i<n-1]
    mx=[b for b in iv if not any(c!=b and c[0]<=b[0] and b[1]<=c[1] for c in iv)]
    return mx
def skeleton(p):
    """shrink maximal proper intervals (if they overlap, perm is 12..k or k..1 type: return None)"""
    mx=maxblocks(p)
    rows=[];used=set()
    for b in mx:
        if any(r in used for r in range(b[0],b[1]+1)): return "linear"
        used.update(range(b[0],b[1]+1))
    segs=sorted(mx+[(i,i) for i in range(len(p)) if i not in used])
    reps=[min(p[a:b+1]) for a,b in segs]
    order=sorted(reps); return tuple(order.index(v)+1 for v in reps)
def binary(q): return len({q[i]-i for i in range(len(q))})==len(q)
if __name__=="__main__":
    import sys
    D=tuple(int(x) for x in sys.argv[1].split(","))
    from collections import Counter
    c=Counter()
    for p in wits(D):
        s=skeleton(p)
        c[("simple" if s==p else ("linear" if s=="linear" else f"frame {s} {'binary' if binary(s) else 'repeats a diagonal'}"))]+=1
    for k,v in c.most_common(): print(v,k)
