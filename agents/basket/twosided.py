import pickle,sys
from machine import partitions
from shape2 import nu
B=int(sys.argv[1]) if len(sys.argv)>1 else 6; sets=pickle.load(open(f"alive{B}.pkl","rb"))
def allpairs(s): return {(a,b) for i in range(s+1) for a in partitions(i) for b in partitions(s-i)}
L=lambda p:len(p); W=lambda p:p[0] if p else 0
feats={
 "box per diagram": lambda st:(W(st[0]),L(st[0]),W(st[1]),L(st[1])),
 "box + sizes": lambda st:(W(st[0]),L(st[0]),W(st[1]),L(st[1]),sum(st[0])),
 "interleaved box": lambda st:(W(nu(st)),L(nu(st))),
 "interleaved box + durfee": lambda st:(W(nu(st)),L(nu(st)),sum(1 for i,x in enumerate(nu(st)) if x>i)),
}
for name,f in feats.items():
    det=0;boxok=0;ex=None
    for S,s in sets:
        A=allpairs(s); val={}
        clash=False
        for st in A:
            k=f(st); v=st in S
            if k in val and val[k]!=v: clash=True
            val[k]=v
        det+= not clash
        if clash and ex is None:
            k0=[k for k in val][0]
            # find clashing pair
            g={}
            for st in A: g.setdefault(f(st),[]).append(st)
            for k,v in g.items():
                al=[x for x in v if x in S]; de=[x for x in v if x not in S]
                if al and de: ex=(s,k,al[0],de[0]);break
        # box test (only for 4-feature version): alive iff all features <= max over alive
        if name=="box per diagram":
            mx=[max(f(x)[i] for x in S) for i in range(4)]
            boxok+= all((st in S)==all(f(st)[i]<=mx[i] for i in range(4)) for st in A)
    print(f"{name}: features determine alive/dead in {det}/{len(sets)} sets", f"; box rule exact in {boxok}" if name=="box per diagram" else "", "\n   e.g. slack %s, same features %s: alive %s, dead %s"%ex if ex else "")
