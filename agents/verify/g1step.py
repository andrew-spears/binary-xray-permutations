# Part 1: does the G1 instance left after placing d_n in row 1 (column 1+d_n) pass G1's test?
# Re-indexing: rows 2..n -> 1..m (m=n-1); columns keep labels {1..n}\{c}, c=1+d_n; new diagonal = col - newrow = d+1.
# So t_k = (d_k+1) + m - k = s_k.  General choice: delete diagonal d=D[j] (d>=0) at row 1, col 1+d.
import sys
from math import comb
def valid_Ds(n):
    out=[]; D=[]
    def rec(k, lo, ps):
        if k==n:
            if ps==comb(n,2): out.append(tuple(D))
            return
        for d in range(lo, n):
            s=d+n-(k+1); p=ps+s
            if p<comb(k+1,2): continue
            if p>comb(n,2): break
            D.append(d); rec(k+1,d+1,p); D.pop()
    rec(0,-(n-1),0); return out
def tight(D,n):
    ps=0
    for k in range(1,n):
        ps+=D[k-1]+n-k
        if ps==comb(k,2): return True
    return False
def g1_ok(Dp, c):  # Dp: diagonals of the m-row board (col labels 1..m+1 minus c), sorted
    m=len(Dp); ps=0
    for k in range(1,m+1):
        ps+=Dp[k-1]+m-k
        need=comb(k,2)+max(0,k+1-c)
        if ps<need: return False,k
    return ps==comb(m,2)+max(0,m+1-c), m
def place(D, j):  # put diagonal D[j] in row 1
    d=D[j]; n=len(D)
    if d<0: return None
    rest=[x+1 for i,x in enumerate(D) if i!=j]
    return g1_ok(rest, 1+d)
N=int(sys.argv[1]) if len(sys.argv)>1 else 12
for n in range(2,N+1):
    Ds=valid_Ds(n); fail=[]; failNT=[]; anyfail=[]
    for D in Ds:
        ok,k=place(D,n-1)
        if not ok:
            fail.append((D,k))
            if not tight(D,n): failNT.append((D,k))
            if not any((r:=place(D,j)) and r[0] for j in range(n)): anyfail.append(D)
    print(n, "valid",len(Ds),"largest-fails",len(fail),"(no-tight-cut",len(failNT),")",
          "no row-1 choice works:",len(anyfail), "smallest:", fail[:3])
