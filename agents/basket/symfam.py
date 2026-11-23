import itertools, json
import recursive as R
from recursive import decompose
from exlib import valid, wits
from skel import maxblocks
allw={}
for n in range(3,10):
    for D in itertools.combinations(range(-n+1,n),n):
        if valid(D,notight=False): allw[D]=wits(D)
simple=lambda p: len(p)>=4 and not maxblocks(p)
inv=lambda p: all(p[p[i]-1]==i+1 for i in range(len(p)))
cs=lambda p: all(p[len(p)-1-i]==len(p)+1-p[i] for i in range(len(p)))
binary=lambda p: len({p[i]-i for i in range(len(p))})==len(p)
F={p for W in allw.values() for p in W if simple(p) and (inv(p) or cs(p))}
R.FR=F; R.buildable.cache_clear()
out={}
for D,W in allw.items():
    if any(R.buildable(p) for p in W): continue
    fixes={}
    for p in W:
        f,bl=decompose(p)
        if f in ((1,2),(2,1)) or f in F: continue
        if all(R.buildable(b) for b in bl):  # only the top frame is missing
            fixes.setdefault(f,p)
    out.setdefault(len(D),[]).append({"D":list(D),"W":len(W),"fixes":[{"f":list(f),"w":list(p),"bin":binary(f),"sym":inv(f) or cs(f)} for f,p in fixes.items()]})
for n,L in out.items():
    print(n,len(L))
    if n==8:
        for x in L: print(" ",x["D"],"W",x["W"],[(tuple(z["f"]),z["bin"]) for z in x["fixes"]])
json.dump(out,open("symfam_miss.json","w"))
print("frames in family per size",{k:sum(1 for f in F if len(f)==k) for k in range(4,10)})
