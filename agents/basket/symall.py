import itertools
import recursive as R
exec(open("symfam.py").read().split("out={}")[0])
def blockfree_perms(n):
    for p in itertools.permutations(range(1,n+1)):
        if simple(p): yield p
G=set()
for n in range(4,10):
    for p in blockfree_perms(n):
        if inv(p) or cs(p): G.add(p)
print("symmetric block-free perms (any diagonals) per size",{k:sum(1 for f in G if len(f)==k) for k in range(4,10)})
R.FR=G; R.buildable.cache_clear()
miss=[D for D,W in allw.items() if not any(R.buildable(p) for p in W)]
from collections import Counter
print("missed per n",Counter(len(D) for D in miss),"no tight cut:",[D for D in miss if valid(D)])
