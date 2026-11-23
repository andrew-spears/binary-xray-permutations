# Part 2: explicit witness of P_n and witness count.
import sys
def PnD(n): return sorted({n-2,2-n}|{d for d in range(3-n,n-2) if (d-(n-1))%2==0})
def wit(n):  # 1-indexed pi
    p={}
    p[2]=n
    for i in range(1,n+1):
        if i%2==1 and i<=n-2: p[i]=n-1-i
        if i%2==0 and i>=4:  p[i]=n+3-i
    last = n-1 if n%2==0 else n
    p[last] = 1 if n%2==0 else 2
    return [p[i] for i in range(1,n+1)]
def rot(p): n=len(p); return [n+1-p[n-1-i] for i in range(n)]
def inv(p):
    q=[0]*len(p)
    for i,v in enumerate(p): q[v-1]=i+1
    return q
def partner(p): return inv(p) if len(p)%2==0 else rot(p)
given={4:"2413/3142",5:"35142/42513",6:"462513/536142",7:"5736142/6472513",8:"68472513/75836142"}
for n in range(4,31):
    p=wit(n); assert sorted(p)==list(range(1,n+1)),n
    assert sorted(p[i]-(i+1) for i in range(n))==PnD(n),n
    assert (rot(p)==p) if n%2==0 else (inv(p)==p)
    q=partner(p); assert sorted(q[i]-(i+1) for i in range(n))==PnD(n)
    if n in given: assert "".join(map(str,p))+"/"+"".join(map(str,q))==given[n],(n,p,q)
print("formula OK for n=4..30, matches listed pairs n=4..8")
def count(D,n):
    Ds=set(D); cnt=0
    def rec(r,usedc,usedd):
        nonlocal cnt
        if r>n: cnt+=1; return
        for d in Ds-usedd:
            c=r+d
            if 1<=c<=n and c not in usedc:
                usedc.add(c); usedd.add(d); rec(r+1,usedc,usedd); usedc.discard(c); usedd.discard(d)
    rec(1,set(),set()); return cnt
for n in range(4,int(sys.argv[1])+1): print(n, "W(P_n) =", count(PnD(n),n), flush=True)
