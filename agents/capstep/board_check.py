"""Is q_S (peeled polynomial) equal to c * per of a single Toeplitz board with holes?
Checks all R,C subsets of [n] of size n-|S| using diagonals D\\S. usage: python3 board_check.py n D S"""
import sys, itertools
from steplib import poly, restrict
n=int(sys.argv[1]); D=[int(v) for v in sys.argv[2].split(',')]; S=[int(v) for v in sys.argv[3].split(',')]
P=poly(D,n); Si={D.index(s) for s in S}
E,C,rem=restrict(P,Si,n); Dr=[D[k] for k in rem]
target={tuple(e):c for e,c in zip(E.tolist(),C.tolist())}
m=n-len(S); found=0
for R in itertools.combinations(range(n),m):
  for Cc in itertools.combinations(range(n),m):
    tab={}
    for p in itertools.permutations(Cc):
      e=[0]*len(Dr); ok=True
      for r,c in zip(R,p):
        if c-r in Dr: e[Dr.index(c-r)]+=1
        else: ok=False;break
      if ok: tab[tuple(e)]=tab.get(tuple(e),0)+1
    if tab and set(tab)==set(target):
      rat={target[k]/tab[k] for k in tab}
      if len(rat)==1: found+=1; print('single board R',R,'C',Cc,'scale',rat)
print('target',target,'single-board matches:',found)
