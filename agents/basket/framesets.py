import itertools
import recursive as R
from exlib import valid, wits, Pn
from skel import maxblocks
def simple(p): return len(p)>=4 and not maxblocks(p)
allw={}
for n in range(3,10):
    for D in itertools.combinations(range(-n+1,n),n):
        if valid(D,notight=False): allw[D]=wits(D)
Pw=set()
for n in range(4,10): Pw|=set(map(tuple,wits(Pn(n))))
simpw={p for W in allw.values() for p in W if simple(p)}
def test(F,label):
    R.FR=set(F); R.buildable.cache_clear()
    miss={}
    for D,W in allw.items():
        if not any(R.buildable(p) for p in W): miss.setdefault(len(D),[]).append(D)
    print(label,"frames",len(F),"missed per n",{n:len(v) for n,v in sorted(miss.items())})
    return miss
m=test(Pw,"P_k solutions only")
print("  n=7 missed:",m.get(7))
m=test(simpw,"all block-free witnesses (valid simple frames)")
print("  missed:",{n:v[:4] for n,v in m.items()})
# stats for counting
for n in range(5,10):
    Ws=[len(W) for D,W in allw.items() if len(D)==n]
    A=len(Ws);S=sum(Ws);S2=sum(w*w for w in Ws)
    print(n,"arrangements",A,"witnesses",S,"max W",max(Ws),"min W",min(Ws),"(ΣW)^2/ΣW^2 =",round(S*S/S2,1))
