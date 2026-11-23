import sys, itertools
from exlib import valid, wits
def diags(p): return [p[i]-i-1 for i in range(len(p))]
def binary(p): d=diags(p); return len(set(d))==len(d)
def expand1(p, i, beta):
    """replace point in row i (0-idx) of p by block beta"""
    w=len(beta); v=p[i]
    q=[]
    for r,c in enumerate(p):
        if r==i: q.extend(v+b-1 for b in beta)
        else: q.append(c+(w-1 if c>v else 0))
    return tuple(q)
NMAX=int(sys.argv[1]); ALL=len(sys.argv)>2
basket=[(2,1)]; primes={}
R={1:{(1,)}}
for n in range(2,NMAX+1):
    Rn=set()
    for k in range(1,n):
        w=n-k+1
        for beta in [b for b in basket if len(b)==w]:
            for p in R[k]:
                for i in range(k):
                    q=expand1(p,i,beta)
                    if binary(q): Rn.add(q)
    R[n]=Rn
    covered={tuple(sorted(diags(q))) for q in Rn}
    allD=[D for D in itertools.combinations(range(-n+1,n),n) if valid(D,notight=False)]
    missed=[D for D in allD if D not in covered]
    newp=[]
    for D in missed:
        W=sorted(wits(D)); newp.append((D,W[0],len(W)))
        basket.append(W[0]); Rn.add(tuple(W[0]))
    if ALL: basket.extend(q for q in Rn if q not in basket)
    primes[n]=newp
    nt=sum(1 for D in allD if valid(D))
    ntm=sum(1 for D in missed if valid(D))
    print(f"n={n}: valid D {len(allD)} (no tight cut {nt}); reached witnesses {len(Rn)}; covered D {len(covered)}; missed {len(missed)} (no tight cut {ntm})")
    for D,p,W in newp: print("   prime",D,"chosen",p,"of",W,"witnesses","(tight cut)" if not valid(D) else "")
