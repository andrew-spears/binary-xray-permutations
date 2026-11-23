import sys, itertools
from exlib import valid, wits
def diags(p): return [p[i]-i-1 for i in range(len(p))]
def binary(p): d=diags(p); return len(set(d))==len(d)
def expand1(p,i,beta):
    w=len(beta); v=p[i]; q=[]
    for r,c in enumerate(p):
        if r==i: q.extend(v+b-1 for b in beta)
        else: q.append(c+(w-1 if c>v else 0))
    return tuple(q)
WITH12=False
def run(NMAX, loose=False, allw=False, verbose=True, comp=False):
    basket=[(2,1),(1,2)] if WITH12 else [(2,1)]; R={1:{(1,)}}; out={}
    for n in range(2,NMAX+1):
        Rn=set()
        for k in range(1,n):
            for beta in [b for b in basket if len(b)==n-k+1]:
                for p in R[k]:
                    for i in range(k):
                        q=expand1(p,i,beta)
                        if loose or binary(q): Rn.add(q)
        covered={tuple(sorted(diags(q))) for q in Rn if binary(q)}
        allD=[D for D in itertools.combinations(range(-n+1,n),n) if valid(D,notight=False)]
        missed=[D for D in allD if D not in covered]
        out[n]=[]
        for D in missed:
            W=sorted(wits(D)); add=W if allw else W[:1]
            basket.extend(add); Rn.update(add); out[n].append((D,len(W),add))
        R[n]=Rn
        if comp: basket.extend(q for q in Rn if binary(q) and q not in basket)
        if verbose:
            print(f"n={n}: reached valid witnesses {sum(binary(q) for q in Rn)}, primes {len(missed)}")
            for D,W,add in out[n]: print("   ",D,"W =",W, "added", len(add))
    return out
if __name__=="__main__":
    for loose in (False,True):
        for allw in (False,True):
            print(f"=== intermediates {'any' if loose else 'valid'}, prime adds {'all witnesses' if allw else 'one witness'}")
            run(6,loose,allw)
