import itertools
def scores(D):
    n=len(D);D=sorted(D);return [D[k]+n-1-k for k in range(n)]
def valid(D, notight=True):
    n=len(D);s=scores(D);p=0
    for k in range(n):
        p+=s[k]
        if p<k*(k+1)//2: return False
        if notight and k<n-1 and p==k*(k+1)//2: return False
    return p==n*(n-1)//2
def wits(D):
    n=len(D);S=set(D);out=[]
    def rec(i,used,ds,p):
        if i==n: out.append(tuple(x+1 for x in p));return
        for c in range(n):
            if c in used: continue
            d=c-i
            if d in S and d not in ds:
                used.add(c);ds.add(d);p.append(c);rec(i+1,used,ds,p);p.pop();used.discard(c);ds.discard(d)
    rec(0,set(),set(),[]);return out
def Ds(n,notight=True):
    for D in itertools.combinations(range(-n+1,n),n):
        if valid(D,notight): yield D
def Pn(n): return tuple(sorted({n-2,-(n-2)}|{d for d in range(-(n-3),n-2) if (d-(n-1))%2==0}))
