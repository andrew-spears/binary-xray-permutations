import pickle,sys
from machine import partitions, realize
from shape import dom, conj
B=int(sys.argv[1]); sets=pickle.load(open(f"alive{B}.pkl","rb"))
def nu(st,k=None):
    k=k or (B+3)
    R=realize(st[0],k);C=realize(st[1],k)
    U=sorted([2*r-1 for r in R]+[2*c for c in C])
    return tuple(sorted([x-i-1 for i,x in enumerate(U) if x-i-1>0],reverse=True))
def allpairs(s): return {(a,b) for i in range(s+1) for a in partitions(i) for b in partitions(s-i)}
st={"down":0,"up":0,"interval":0}; ex=None
for S,s in sets:
    A=allpairs(s); N={nu(x):x for x in A}; SN={nu(x) for x in S}
    down=all(m in SN for a in SN for m in N if dom(m,a))
    up=all(m in SN for a in SN for m in N if dom(a,m))
    inter=all(m in SN for a in SN for c in SN for m in N if dom(a,m) and dom(m,c))
    st["down"]+=down; st["up"]+=up; st["interval"]+=inter
    if not inter and ex is None: ex=(s,sorted(SN),sorted(set(N)-SN))
print(len(sets),st); print(ex)
