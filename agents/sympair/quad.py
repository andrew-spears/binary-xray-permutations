# Even n=2m, parity-failing L (#even(L) odd). Test: {1..2m} = pairs with differences L\{p,q}
# plus one "quad" {x, x+p, x+q, x+p+q} (a 4-cycle x->x+p->x+p+q->x+q->x of pi, diagonals p,q,-p,-q).
import itertools, sys
from sym import landau

def quadpair(L,N):
    L=list(L)
    for p,q in itertools.combinations(L,2):
        if (p+q)%2==0: continue
        rest=[l for l in L if l!=p and l!=q]
        for x in range(1,N-p-q+1):
            used=[False]*(N+2)
            for y in (x,x+p,x+q,x+p+q): used[y]=True
            if solve(rest,used,N): return (p,q,x)
    return None

def solve(rest,used,N):
    rem=set(rest)
    def rec():
        pp=1
        while pp<=N and used[pp]: pp+=1
        if pp>N: return True
        for l in sorted(rem,reverse=True):
            qq=pp+l
            if qq<=N and not used[qq]:
                used[pp]=used[qq]=True; rem.discard(l)
                if rec(): return True
                rem.add(l); used[pp]=used[qq]=False
        return False
    return rec()

M=int(sys.argv[1])
for m in range(2,M+1):
    n=2*m; cnt=0; bad=[]
    for L in itertools.combinations(range(1,n),m):
        if not landau(L,n): continue
        if sum(1 for l in L if l%2==0)%2==0: continue
        cnt+=1
        if not quadpair(L,n): bad.append(L)
    print(f"n={n}: parity-failing valid L={cnt}, no quad+pairing={len(bad)}",bad[:6],flush=True)
