import minimal as m, grammar as g, pickle
from exlib import Ds,wits,Pn
from nearP import three_cycles
G=m.run(9)
def split(p):
    n=len(p)
    for a in range(1,n):
        b=n-a; top=p[:a]; bot=p[a:]
        w="".join("T" if c in set(top) else "B" for c in range(1,n+1))
        st=lambda xs: tuple(sorted(xs).index(x)+1 for x in xs)
        t,bb=st(top),st(bot)
        if t not in G[a] or bb not in G[b]: continue
        if w=="B"*b+"T"*a: return (a,0,t,bb)
        for s in range(1,a+1):
            if w=="B"*(b-1)+"T"*s+"B"+"T"*(a-s): return (a,s,t,bb)
        for s in range(1,b+1):
            if w=="B"*(b-s)+"T"+"B"*s+"T"*(a-1): return (a,-s,t,bb)
def tree(p,ind=""):
    if len(p)==1: return
    a,s,t,bb=split(p); print(f"{ind}{''.join(map(str,p))}  D={sorted(g.dg(p))}  = top {''.join(map(str,t))} over bottom {''.join(map(str,bb))}, slide {s:+d}")
    tree(t,ind+"   "); tree(bb,ind+"   ")
for k in (5,6,7):
    W=[w for w in wits(Pn(k)) if w in G[k]]; print("P",k,"witnesses",wits(Pn(k)),"in G",W); tree(W[0]); print()
# a layer-3 example at n=9
P=three_cycles(Pn(9))
for D in Ds(9):
    if three_cycles(D)-P==3:
        W=[w for w in wits(D) if w in G[9]]
        if len(wits(D))<=8: print("layer3",D,"W",len(wits(D))); tree(W[0]); print(); break
