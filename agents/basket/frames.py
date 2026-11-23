import itertools
from exlib import valid, wits, Pn
from skel import skeleton
need={}   # D -> set of skeletons
for n in range(4,10):
    for D in itertools.combinations(range(-n+1,n),n):
        if not valid(D) or D==Pn(n): continue
        S=set()
        for p in wits(D):
            s=skeleton(p)
            if s!=p and s!="linear": S.add(s)
        need[D]=S
# greedy hitting set, smallest frames first preference
chosen=[]; left=set(need)
while left:
    cnt={}
    for D in left:
        for s in need[D]: cnt[s]=cnt.get(s,0)+1
    best=max(cnt,key=lambda s:(cnt[s],-len(s)))
    chosen.append((best,cnt[best])); left={D for D in left if best not in need[D]}
from collections import Counter
print("frames needed:",len(chosen),"by size",sorted(Counter(len(s) for s,_ in chosen).items()))
for s,c in chosen[:25]:
    d=[s[i]-i-1 for i in range(len(s))]
    print(s,"covers",c,"binary" if len(set(d))==len(d) else "repeats a diagonal")
