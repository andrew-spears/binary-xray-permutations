import pickle,sys,io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from twosided import allpairs
from machine import partitions
B=int(sys.argv[1]); sets=pickle.load(open(f"alive{B}.pkl","rb"))
L=lambda p:len(p); W=lambda p:p[0] if p else 0
odd=lambda p:sum(x%2 for x in p)
def core2(p):  # 2-core size via sign of content parity count
    a=sum(1 for i,x in enumerate(p) for j in range(x) if (j-i)%2==0); b=sum(p)-a
    return a-b
feats={"box+sizes+odd parts":lambda st:(W(st[0]),L(st[0]),W(st[1]),L(st[1]),sum(st[0]),odd(st[0]),odd(st[1])),
       "box+sizes+2-core":lambda st:(W(st[0]),L(st[0]),W(st[1]),L(st[1]),sum(st[0]),core2(st[0]),core2(st[1])),
       "full diagrams, sizes only":lambda st:(sum(st[0]),)}
for name,f in feats.items():
    det=0;ex=None
    for S,s in sets:
        g={}
        for st in allpairs(s): g.setdefault(f(st),[]).append(st)
        bad=[(k,v) for k,v in g.items() if 0<sum(x in S for x in v)<len(v)]
        det+=not bad
        if bad and ex is None: k,v=bad[0]; ex=(s,[x for x in v if x in S][0],[x for x in v if x not in S][0])
    print(f"{name}: determine alive/dead in {det}/{len(sets)}", "e.g. slack %s alive %s dead %s"%ex if ex else "")
