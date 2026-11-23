# compare upset counts (strict-score pairs only, tie-invariant) of accepted vs all tournaments, n<=7
import sys; sys.path.insert(0,'/home/claude/agents/tourn')
from tourn import *
from collections import defaultdict, Counter
n=int(sys.argv[1])
pairs=[(x,y) for x in range(n) for y in range(x+1,n)]
def ups(T,s): return sum(1 for x,y in pairs if s[x]<s[y] and T[x]>>y&1)
allc=defaultdict(Counter)
for m in range(1<<len(pairs)):
    b=[0]*n
    for k,(x,y) in enumerate(pairs):
        if m>>k&1: b[x]|=1<<y
        else: b[y]|=1<<x
    T=tuple(b); s=svec(T)
    if list(s)!=sorted(s): continue
    allc[s][ups(T,s)]+=1
by=defaultdict(list)
for p in witnesses(n): by[scores_of(p)].append(p)
for s in valid_seqs(n):
    acc=Counter()
    clo=set()
    for p in by[s]:
        T=gamma(p)
        for q in tie_perms(s): clo.add(relabel(T,q))
    for T in clo: acc[ups(T,s)]+=1
    print(s,"all:",dict(sorted(allc[s].items())),"acc:",dict(sorted(acc.items())))
