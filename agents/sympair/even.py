# Even n=2m, D=±L, L subset {1..2m-1}, |L|=m. Landau <=> top-K(L) <= K(2m-K).
# (a) involution witness <=> perfect pairing of {1..2m} with differences L (Nordh Conj 8; needs #even(L) even)
# (b) centrosymmetric witness <=> half-board puzzle: bijection sigma of {1..m}, each i labelled
#     |sigma(i)-i| (same side, must be !=0) or 2m+1-i-sigma(i) (cross), labels = L exactly.
# (c) "folded involution" puzzle: partition L into odd singletons and opposite-parity pairs {a<b}
#     so that {l: singletons} U {b-a, a+b: pairs} = {1,3,...,2m-1}.
import itertools, sys
from sym import landau, pairings

def centro(L,m):
    Ls=set(L); usedc=[False]*(m+1)
    def rec(i,rem):
        if i>m: return True
        for j in range(1,m+1):
            if usedc[j]: continue
            for l in (abs(j-i), 2*m+1-i-j):
                if l and l in rem:
                    usedc[j]=True; rem.discard(l)
                    if rec(i+1,rem): return True
                    rem.add(l); usedc[j]=False
        return False
    return rec(1,set(L))

def folded(L,m):
    targets=set(range(1,2*m,2))
    def rec(rem,tg):
        if not rem: return not tg
        a=min(rem); r=rem-{a}
        if a%2 and a in tg:
            if rec(r,tg-{a}): return True
        for b in r:
            if (a+b)%2 and (b-a) in tg and (a+b) in tg and b-a!=a+b:
                if rec(r-{b},tg-{b-a,a+b}): return True
        return False
    return rec(frozenset(L),frozenset(targets))

M=int(sys.argv[1])
for m in range(1,M+1):
    n=2*m; cnt=0; noinv=0; noinv_par=0; nocen=0; nofold=0; ex=[]
    for L in itertools.combinations(range(1,n),m):
        if not landau(L,n): continue
        cnt+=1
        par=sum(1 for l in L if l%2==0)%2==0
        inv=bool(pairings(L,n,None))
        if not inv:
            noinv+=1
            if par: noinv_par+=1; ex.append(L)
        if not centro(L,m): nocen+=1
        if not folded(L,m): nofold+=1
    print(f"n={n}: valid={cnt} no-involution={noinv} (of which parity OK: {noinv_par} {ex[:3]}) no-centro={nocen} no-folded-involution={nofold}",flush=True)
