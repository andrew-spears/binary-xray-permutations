import itertools, sys
from collections import deque
from exlib import valid
def binary(p): return len({p[i]-i for i in range(len(p))})==len(p)
def D(p): return tuple(sorted(p[i]-i-1 for i in range(len(p))))
def run(n, both):
    start=tuple(range(n,0,-1)); seen={start}; q=deque([start])
    while q:
        p=q.popleft(); pos={c:i for i,c in enumerate(p)}
        for c in range(1,n):
            i,j=pos[c],pos[c+1]          # rows of points in columns c, c+1
            if not both and i<j: continue  # only lower-left/upper-right pairs (inward moves)
            r=list(p); r[i],r[j]=c+1,c; r=tuple(r)
            if binary(r) and r not in seen: seen.add(r); q.append(r)
    reached={D(p) for p in seen}
    allD=[d for d in itertools.combinations(range(-n+1,n),n) if valid(d,notight=False)]
    miss=[d for d in allD if d not in reached]
    return len(seen), len(allD), miss
for n in range(3,int(sys.argv[1])+1):
    for both in (False,True):
        w,A,miss=run(n,both)
        print(n,"inward only" if not both else "both ways","witnesses reached",w,"arrangements",A,"missed",len(miss),miss[:3])
