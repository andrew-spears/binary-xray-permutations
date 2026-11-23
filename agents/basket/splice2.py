import itertools
from exlib import wits, valid, Pn
from splice import splice, D
def allwits(n):
    out=[]
    for d in itertools.combinations(range(-n+1,n),n):
        if valid(d,notight=False): out+= [tuple(w) for w in wits(d)]
    return out
def splice_top(top,bot,s):
    """mirror move: top's lowest column slides LEFT past s of bottom's highest columns"""
    a,b=len(top),len(bot)
    word="B"*(b-s)+"T"+"B"*s+"T"*(a-1)
    Tc=[i+1 for i,ch in enumerate(word) if ch=="T"]; Bc=[i+1 for i,ch in enumerate(word) if ch=="B"]
    return tuple(Tc[c-1] for c in top)+tuple(Bc[c-1] for c in bot)
W={n:allwits(n) for n in range(1,8)}
W[1]=[(1,)]; W[2]=[(2,1)]
def arr(p): return tuple(sorted(p[i]-i-1 for i in range(len(p))))
target=(-6,-5,-2,-1,2,3,4,5)
hits=[]
for a in range(1,8):
    b=8-a
    for t in W[a]:
        for bb in W[b]:
            for s in range(1,a+1):
                p,_=splice(t,bb,s)
                if tuple(D(p))==target: hits.append(("bottom slides right",a,t,bb,s,p))
            for s in range(1,b+1):
                p=splice_top(t,bb,s)
                if tuple(D(p))==target: hits.append(("top slides left",a,t,bb,s,p))
for h in hits:
    kind,a,t,bb,s,p=h
    print(kind,"top",t,arr(t),"bottom",bb,arr(bb),"slide",s,"->",p)
print(len(hits))

print("--- general shuffles, both pieces of size >= 2, at most k crossings ---")
def words(a,b):
    for pos in itertools.combinations(range(a+b),a):
        w=["B"]*(a+b)
        for i in pos: w[i]="T"
        cross=sum(1 for i in range(a+b) for j in range(i+1,a+b) if w[i]=="T" and w[j]=="B")
        yield "".join(w),cross
def build(t,bb,w):
    Tc=[i+1 for i,ch in enumerate(w) if ch=="T"]; Bc=[i+1 for i,ch in enumerate(w) if ch=="B"]
    return tuple(Tc[c-1] for c in t)+tuple(Bc[c-1] for c in bb)
res=[]
for a in range(2,7):
    b=8-a
    for w,cr in words(a,b):
        if cr==0 or cr>4: continue
        for t in W[a]:
            for bb in W[b]:
                p=build(t,bb,w)
                if tuple(D(p))==target: res.append((cr,a,t,arr(t),bb,arr(bb),w,p))
res.sort()
for r in res[:12]: print(r)
print(len(res))
