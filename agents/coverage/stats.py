"""Compare simple statistics of uncovered vs all no-tight-cut D. Usage: python3 stats.py n"""
import sys
from common import *
n=int(sys.argv[1])
allD=sorted({canon(D) for D in enum_valid(n) if not tight_cuts(D,n)})
unc=[tuple(eval(l.split('  ')[0])) for l in open(f'uncovered_{n}.txt')]
def st(L,name):
    N=len(L); f=lambda p: f"{sum(map(p,L))/N:.2f}"
    var=lambda D: sum((s-(n-1)/2)**2 for s in scores(D,n))/n
    print(name,N,"s1=1:",f(lambda D: scores(D,n)[0]==1 or scores(tuple(sorted(-d for d in D)),n)[0]==1),
      "0inD:",f(lambda D:0 in D),"symm:",f(lambda D: set(D)==set(-d for d in D)),
      "#|d|<=n/4:",f"{sum(sum(abs(d)<=n/4 for d in D) for D in L)/N:.2f}",
      "score var:",f"{sum(map(var,L))/N:.2f}", "max|d|=n-2:",f(lambda D:max(map(abs,D))==n-2),
      "one parity>=n-2:",f(lambda D: max(sum(d%2==0 for d in D),sum(d%2 for d in D))>=n-2))
st(allD,'all '); st(unc,'unc ')
cov=[D for D in allD if D not in set(unc)]; st(cov,'cov ')
