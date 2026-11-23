import itertools,sys
def part(X):
    X=sorted(X); return tuple(sorted([x-i-1 for i,x in enumerate(X) if x-i-1>0],reverse=True))
def partitions(s,mx=None):
    if s==0: yield (); return
    if mx is None: mx=s
    for p in range(min(s,mx),0,-1):
        for q in partitions(s-p,p): yield (p,)+q
def realize(p,k):  # set of size k with partition p
    parts=sorted(list(p)+[0]*(k-len(p)))
    return {i+1+parts[i] for i in range(k)}
def step(st,e,k=20,n=200):
    R,C=realize(st[0],k),realize(st[1],k); t=2*(k+1)+e; out={}
    for r in range(1,n+1):
        c=t-r
        if 1<=c<=n and r not in R and c not in C:
            out.setdefault((part(R|{r}),part(C|{c})),[]).append((r-(k+1),c-(k+1)))
    return out
if __name__=='__main__':
    B=int(sys.argv[1])
    states=[(a,b) for s in range(B+1) for i in range(s+1) for a in partitions(i) for b in partitions(s-i)]
    print(len(states),"states")
    def name(st): return f"rows{list(st[0]) or '∅'} cols{list(st[1]) or '∅'}"
    for st in states:
        s=sum(st[0])+sum(st[1])
        for e in range(-s, B-s+1):
            o=step(st,e)
            print(name(st),"shift",f"{e:+d}","->",{name(k):v for k,v in o.items()} or "STUCK")
