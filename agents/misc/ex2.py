import itertools
from math import comb
def wit(rows,cols,D):
    out=[]
    for p in itertools.permutations(cols):
        if sorted(c-r for r,c in zip(rows,p))==sorted(D): out.append(p)
    return out
def landau(D):
    n=len(D); s=[d+n-k for k,d in enumerate(sorted(D),1)]; return s
# tight-cut example n=5
for D in itertools.combinations(range(-4,5),5):
    if sum(D)!=0: continue
    s=landau(D); ps=[sum(s[:k]) for k in range(1,6)]
    if all(ps[k-1]>=comb(k,2) for k in range(1,6)) and ps[4]==10:
        tight=[k for k in range(1,5) if ps[k-1]==comb(k,2)]
        if tight==[2]: print("tight@2",D,s,wit(range(1,6),range(1,6),D)[:2])
print("peel ex", wit([1,2,3,4],[1,3,4,5],[-2,0,2,3]))
print("g1 rest", wit([2,3,4],[1,2,4],[-2,-1,1]))
print("f2", wit(range(1,7),range(1,7),[-4,-3,-1,1,3,4]))
print("start 2413 parity rows")
