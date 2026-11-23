# other canonical candidates: Havel-Hakimi greedy variants and round (rotational) tournaments
import sys, itertools; sys.path.insert(0,'/home/claude/agents/tourn')
from tourn import *
from collections import defaultdict
def hh(s, pick, lose_to):
    n=len(s); r=list(s); alive=list(range(n)); b=[0]*n
    while alive:
        m=len(alive)
        v=(max if pick=='max' else min)(alive, key=lambda u:(r[u],u))
        others=[u for u in alive if u!=v]
        # v loses to m-1-r[v] others: chosen as largest or smallest residual
        others.sort(key=lambda u:(r[u],u), reverse=(lose_to=='largest'))
        L=set(others[:m-1-r[v]])
        if len(L)!=m-1-r[v]: return None
        for u in others:
            if u in L: b[u]|=1<<v; r[u]-=1
            else: b[v]|=1<<u
        alive.remove(v)
        if any(r[u]<0 for u in alive): return None
    T=tuple(b); return T if svec(T)==tuple(s) else None
def rounds(s):
    n=len(s); out=set()
    for perm in set(itertools.permutations(range(1,n))):
        cyc=(0,)+perm; b=[0]*n
        for k,v in enumerate(cyc):
            for t in range(1,s[v]+1): b[v]|=1<<cyc[(k+t)%n]
        T=tuple(b)
        if all(not(T[x]>>y&1 and T[y]>>x&1) for x in range(n) for y in range(n)) and svec(T)==s: out.add(canon_ties(T,s))
    return out
n=int(sys.argv[1])
by=defaultdict(list)
for p in witnesses(n): by[scores_of(p)].append(p)
res=defaultdict(int); seqs=valid_seqs(n)
for s in seqs:
    img=set(canon_ties(gamma(p),s) for p in by[s])
    line=[str(s)]
    for pick in ('max','min'):
        for lt in ('largest','smallest'):
            T=hh(s,pick,lt); ok = T is not None and canon_ties(T,s) in img
            res[(pick,lt)]+=ok; line.append(f"hh{pick[1]}{lt[0]}:{'-' if T is None else int(ok)}")
    if n<=8:
        R=rounds(s); a=len(R&img); res['round_exists']+=bool(R); res['round_acc']+=bool(a); line.append(f"round {len(R)}/{a}")
    print(' '.join(line))
print("n",n,"seqs",len(seqs),dict(res))
