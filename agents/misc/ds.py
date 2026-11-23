import itertools
from math import comb
def scoreseqs(n):
    out=[]; tot=n*(n-1)//2
    def rec(k,mn,s,acc):
        if k==n:
            if s==tot: out.append(tuple(acc))
            return
        for v in range(mn,n):
            ns=s+v
            if ns<comb(k+1,2): continue
            if ns+v*(n-k-1)>tot: break
            rec(k+1,v,ns,acc+[v])
    rec(0,0,0,[]); return out
def toD(s): n=len(s); return frozenset(s[k]+(k+1)-n for k in range(n))
def tight(s):
    t=0
    for k in range(1,len(s)):
        t+=s[k-1]
        if t==comb(k,2): return True
    return False
VALID={n:{toD(s) for s in scoreseqs(n)} for n in range(1,13)}
for n in range(4,12):
    loose=[toD(s) for s in scoreseqs(n) if not tight(s)]
    hits=[]; nonband=[]
    for D in loose:
        Dl=sorted(D); found=None
        for n1 in range(1,n//2+1):
            for D1 in itertools.combinations(Dl,n1):
                D1=frozenset(D1); D2=D-D1
                if D1 in VALID[n1] and D2 in VALID[n-n1]: found=(sorted(D1),sorted(D2)); break
            if found: break
        if found:
            hits.append(D)
            if Dl!=list(range(Dl[0],Dl[-1]+1)) and not (0 not in D and Dl==[x for x in range(-max(Dl),max(Dl)+1) if x]):
                nonband.append((Dl,found))
    print(n,len(loose),len(hits),f"{len(hits)/len(loose):.2f}","nonband:",len(nonband), nonband[:2])
print("--- excluding the 1x1 {0} block")
for n in range(4,12):
    loose=[toD(s) for s in scoreseqs(n) if not tight(s)]
    c=0; ex=None; zero=sum(1 for D in loose if 0 in D)
    for D in loose:
        Dl=sorted(D); ok=False
        for n1 in range(2,n//2+1):
            for D1 in itertools.combinations(Dl,n1):
                D1=frozenset(D1)
                if D1 in VALID[n1] and (D-D1) in VALID[n-n1]: ok=(sorted(D1),sorted(D-D1)); break
            if ok: break
        if ok:
            c+=1
            if ex is None and Dl!=list(range(Dl[0],Dl[-1]+1)): ex=(Dl,ok)
    print(n,len(loose),"contain 0:",zero,"split w/ blocks>=2:",c,ex)
