import itertools, sys, json
from collections import defaultdict
from exlib import valid, wits
PATS = [(2,1),(1,3,2),(2,1,3),(3,2,1)]   # block patterns (1-indexed local perms)
def expand(sig, marks):
    """sig: tuple 1-indexed perm; marks: dict row(0-idx)->pattern. returns big perm"""
    m=len(sig); w=[len(marks[i]) if i in marks else 1 for i in range(m)]
    rowstart=[sum(w[:i]) for i in range(m)]
    colw={sig[i]:w[i] for i in range(m)}
    colstart={}; c=0
    for col in range(1,m+1): colstart[col]=c; c+=colw[col]
    big=[0]*sum(w)
    for i in range(m):
        pat=marks.get(i,(1,))
        for k,v in enumerate(pat): big[rowstart[i]+k]=colstart[sig[i]]+v
    return tuple(big)
def diags(p): return tuple(sorted(p[i]-i-1 for i in range(len(p))))
if __name__!="__main__": raise SystemExit
NMAX=int(sys.argv[1])
res=defaultdict(list)   # big D -> list of (D', marking, status)
for m in range(2,NMAX):
    for Dp in itertools.combinations(range(-m+1,m),m):
        if not valid(Dp,notight=False): continue
        W=wits(Dp)
        for k in range(1,m+1):
            for S in itertools.combinations(Dp,k):
                for pats in itertools.product(PATS,repeat=k):
                    n=m+sum(len(p)-1 for p in pats)
                    if n>NMAX: continue
                    mk=dict(zip(S,pats))
                    outs=set(); bad=0
                    for s in W:
                        marks={i:mk[s[i]-i-1] for i in range(m) if s[i]-i-1 in mk}
                        big=expand(s,marks); D=diags(big)
                        if len(set(D))<n: bad+=1
                        else: outs.add(D)
                    for D in outs:
                        if not valid(D): continue
                        status="robust" if (bad==0 and len(outs)==1) else ("collide" if bad else "split")
                        res[D].append((Dp,tuple((d,p) for d,p in mk.items()),status,len(W),bad,len(outs)))
import pickle; pickle.dump(dict(res),open(f"res_{NMAX}.pkl","wb"))
# summary per n
from exlib import Ds, Pn
for n in range(4,NMAX+1):
    tot=rob=anyx=0; norob=[]
    for D in Ds(n):
        if tuple(sorted(-x for x in D))<D: continue
        tot+=1; L=res.get(D,[])
        if L: anyx+=1
        if any(x[2]=="robust" for x in L): rob+=1
        else: norob.append((D, "no shrinkable block" if not L else "only non-robust"))
    print(n,"D",tot,"some expansion",anyx,"robust",rob, "examples w/o robust:",norob[:6])
