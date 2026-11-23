import sys, functools
from machine import step, partitions
B=int(sys.argv[1])
@functools.lru_cache(None)
def T(st,e): return tuple(step(st,e,k=B+4,n=4*B+20).keys())
def trans(S,e): 
    out=set()
    for st in S: out|=set(T(st,e))
    return frozenset(out)
start=(frozenset({((),())}),0,None)
seen={start};todo=[start];sets=set()
while todo:
    S,s,last=todo.pop()
    lo=-s if last is None else max(-s,last-1)
    for e in range(lo,B-s+1):
        S2=trans(S,e); s2=s+e
        if not S2: print("EMPTY",S,s,e); continue
        x=(S2,s2,e)
        if x not in seen: seen.add(x);todo.append(x);sets.add((S2,s2))
print("situations",len(seen),"distinct alive sets",len(sets))
import pickle; pickle.dump(sets,open(f"alive{B}.pkl","wb"))
