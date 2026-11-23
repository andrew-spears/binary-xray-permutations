import pickle,sys
from machine import partitions
if __name__=="__main__":
  pass
B=int(sys.argv[1]) if __name__=="__main__" else 0
if __name__=="__main__": sets=pickle.load(open(f"alive{B}.pkl","rb"))
def conj(p):
    return tuple(sum(1 for x in p if x>i) for i in range(p[0])) if p else ()
def dom(a,b): # a dominated by b (same size)
    sa=sb=0
    for i in range(max(len(a),len(b))):
        sa+=a[i] if i<len(a) else 0; sb+=b[i] if i<len(b) else 0
        if sa>sb: return False
    return True
def allpairs(s): return {(a,b) for i in range(s+1) for a in partitions(i) for b in partitions(s-i)}
if __name__=='__main__':
    stats={"swap":0,"conj":0,"downdom":0,"updom":0,"full":0}
    fails={}
    for S,s in sets:
        A=allpairs(s)
        if S==A: stats["full"]+=1
        t={"swap":all((b,a) in S for a,b in S),
           "conj":all((conj(a),conj(b)) in S for a,b in S),
           "downdom":all((a2,b2) in S for a,b in S for a2,b2 in A if sum(a2)==sum(a) and dom(a2,a) and dom(b2,b)),
           "updom":all((a2,b2) in S for a,b in S for a2,b2 in A if sum(a2)==sum(a) and dom(a,a2) and dom(b,b2))}
        for k,v in t.items():
            if v: stats[k]+=1
            elif k not in fails: fails[k]=(s,sorted(S),sorted(A-S))
    print(len(sets),stats)
    for k,v in fails.items(): print(k,"fails e.g. slack",v[0],"\n alive",v[1][:12],"\n missing",v[2][:12])
