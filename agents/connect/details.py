# details.py: small-n cross-check of conn.c and explicit examples (pure Python, n<=8).
import itertools, sys
def wits(n):
    W={}
    for p in itertools.permutations(range(n)):
        d=frozenset(p[i]-i for i in range(n))
        if len(d)==n: W.setdefault(d,[]).append(p)
    return W
def notight(D,n):
    s=sorted(D); t=0
    for k in range(1,n):
        t+=s[k-1]+n-k
        if t==k*(k-1)//2: return False
    return True
def single(a,b):
    S=[r for r in range(len(a)) if a[r]!=b[r]]
    inv={c:r for r,c in enumerate(a)}; x=S[0]; L=0
    while True:
        x=inv[b[x]]; L+=1
        if x==S[0]: break
    return L==len(S)
def comps(ws,k,var):
    par=list(range(len(ws)))
    def f(x):
        while par[x]!=x: x=par[x]
        return x
    for i in range(len(ws)):
        for j in range(i+1,len(ws)):
            h=sum(a!=b for a,b in zip(ws[i],ws[j]))
            if h<=k and (var=='R' or single(ws[i],ws[j])): par[f(i)]=f(j)
    g={}
    for i in range(len(ws)): g.setdefault(f(i),[]).append(ws[i])
    return list(g.values())
ham=lambda a,b:sum(x!=y for x,y in zip(a,b))
fmt=lambda p:''.join(str(c+1) for c in p)
for n in range(4,int(sys.argv[1])+1):
    W=wits(n)
    for k in (3,4):
        for var in ('C','R'):
            bad=[(sorted(D),len(comps(ws,k,var))) for D,ws in W.items() if notight(D,n) and sorted(-x for x in D)<=sorted(D) and len(comps(ws,k,var))>1]
            print(n,var,k,'#disc',len(bad),'maxcomp',max([b[1] for b in bad],default=1))
    # swap-ready check + component-level failure examples (k=3)
    for D,ws in W.items():
        Ds=sorted(D)
        for a in range(-(n-1),n-3):
            if a in D and a+3 in D and a+1 not in D and a+2 not in D:
                D2=(D-{a,a+3})|{a+1,a+2}; w2=W[D2]
                r=[min(ham(p,q) for q in w2) for p in ws]
                assert min(r)==2
                for k in (3,4):
                    for c in comps(ws,k,'C'):
                        rc=min(min(ham(p,q) for q in w2) for p in c)
                        if rc>2 and n<=6: print('  n',n,'k',k,'D',Ds,'move',a,a+3,'component',[fmt(p) for p in c],'best r in comp',rc)
    print(n,'all moves have min r = 2: OK')
