import itertools
import recursive as R
from exlib import valid, wits, Pn
from skel import maxblocks
allw={}
for n in range(3,10):
    for D in itertools.combinations(range(-n+1,n),n):
        if valid(D,notight=False): allw[D]=wits(D)
def simple(p): return len(p)>=4 and not maxblocks(p)
inv=lambda p: all(p[p[i]-1]==i+1 for i in range(len(p)))
cs=lambda p: all(p[len(p)-1-i]==len(p)+1-p[i] for i in range(len(p)))
bf=[(D,p) for D,W in allw.items() for p in W if simple(p)]
def test(F,label):
    R.FR=set(F); R.buildable.cache_clear(); miss={}
    for D,W in allw.items():
        if not any(R.buildable(p) for p in W): miss.setdefault(len(D),[]).append(D)
    sizes={}
    for f in F: sizes[len(f)]=sizes.get(len(f),0)+1
    print(f"{label}: frames per size {dict(sorted(sizes.items()))}; missed per n {{{', '.join(f'{n}: {len(v)}' for n,v in sorted(miss.items()))}}}")
test({p for D,p in bf if inv(p) or cs(p)},"block-free solutions that are involutions or half-turn symmetric")
test({p for D,p in bf if len(allw[D])<=4},"block-free solutions of arrangements with at most 4 witnesses")
test({p for D,p in bf if len(allw[D])<=2},"block-free solutions of arrangements with at most 2 witnesses")
test({p for D,p in bf if all(simple(q) for q in allw[D])},"solutions of arrangements all of whose solutions are block-free")
