import itertools
from exlib import valid, wits, Pn
def scores(D): n=len(D);return [d+n-1-k for k,d in enumerate(sorted(D))]
def three_cycles(D):
    from math import comb
    n=len(D); return comb(n,3)-sum(comb(s,2) for s in scores(D))
def moves(D):
    S=set(D);out=set()
    for a in D:
        for b in D:
            if b-a>=3 and a+1 not in S and b-1 not in S and all(x in S for x in range(a+2,b-1)):
                out.add(tuple(sorted(S-{a,b}|{a+1,b-1})))
    return out
Psol={n:[tuple(w) for w in wits(Pn(n))] for n in range(4,9)}
Psol[3]=[(1,3,2),(2,1,3)]; Psol[2]=[(2,1)]; Psol[1]=[(1,)]
def build(t,bb,w):
    Tc=[i+1 for i,ch in enumerate(w) if ch=="T"]; Bc=[i+1 for i,ch in enumerate(w) if ch=="B"]
    return tuple(Tc[c-1] for c in t)+tuple(Bc[c-1] for c in bb)
def Pspl(D):
    n=len(D);best=None
    for a in range(2,n-1):
        b=n-a
        if a not in Psol or b not in Psol: continue
        for pos in itertools.combinations(range(n),a):
            w=["B"]*n
            for i in pos: w[i]="T"
            w="".join(w); cr=sum(1 for i in range(n) for j in range(i+1,n) if w[i]=="T" and w[j]=="B")
            for t in Psol[a]:
                for bb in Psol[b]:
                    p=build(t,bb,w)
                    if tuple(sorted(p[i]-i-1 for i in range(n)))==tuple(D):
                        if best is None or cr<best[0]: best=(cr,t,bb,w,p)
    return best
if __name__=="__main__":
 for n in (8,9,10):
      P=Pn(n); lvl1=[D for D in moves(P) if valid(D)]
      lvl2=set()
      for D in lvl1: lvl2|={E for E in moves(D) if valid(E)}
      print(f"n={n}: P has {three_cycles(P)} three-cycles")
      for name,L in (("P + 1 move",sorted(lvl1)),("P + 2 moves",sorted(lvl2))):
          for D in L:
              if tuple(sorted(-x for x in D))<D: continue
              sp=Pspl(D)
              print(f"   {name}: {D} W={len(wits(D))}", "P-splice: crossings %d, %s over %s, %s -> %s"%sp if sp else "no P-over-P splice")
