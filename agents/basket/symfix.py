import json, itertools
from collections import Counter
import recursive as R
from recursive import decompose
exec(open("symfam.py").read().split("out={}")[0])
miss=json.load(open("symfam_miss.json"))
targets=[(tuple(x["D"]),x) for n in ("8","9") for x in miss[n] if x["nt"]]
tally=Counter(); minsz=Counter()
for D,x in targets:
    fx=[tuple(z["f"]) for z in x["fixes"]]
    m=min(len(f) for f in fx); minsz[(len(D),m)]+=1
    for f in fx:
        if len(f)==m: tally[f]+=1
    print(len(D),D,"W",x["W"],"smallest fix size",m,[f for f in fx if len(f)==m][:4])
print(minsz)
print("most common smallest fixes:",tally.most_common(10))
# greedy: add frames until all misses (incl tight cut ones) up to 9 are fixed
extra=[]
def missing():
    R.FR=F|set(extra); R.buildable.cache_clear()
    return [D for D,W in allw.items() if not any(R.buildable(p) for p in W)]
M=missing()
while M:
    cand=Counter()
    for D in M:
        if not valid(D): continue
        for p in allw[D]:
            f,bl=decompose(p)
            if f not in ((1,2),(2,1)) and all(R.buildable(b) for b in bl): cand[f]+=1
    f,_=max(cand.items(),key=lambda t:(t[1],-len(t[0])))
    extra.append(f); M=missing()
    print("add",f,"binary" if binary(f) else "repeats a diagonal","sym" if (inv(f) or cs(f)) else "", "-> still missing",len(M))
