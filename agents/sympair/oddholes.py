import sys
from sym import *
M=int(sys.argv[1])
for m in range(1,M+1):
    N=2*m+1; res=oddcase(m)
    rules={'end(N or N-1)':lambda h,L:(N in h) or (N-1 in h),
           'Rosa-ish(m+1 or m / m+2)':lambda h,L:(m+1 in h) or (m in h) or (m+2 in h),
           'start(1 or 2)':lambda h,L:(1 in h) or (2 in h)}
    out=[]
    for name,r in rules.items():
        fails=[L for L,h in res if not r(h,L)]
        out.append(f"{name}:{len(fails)} {fails[:2]}")
    # parity check
    par=all(all((f - (N*(N+1)//2 - sum(L)))%2==0 for f in h) for L,h in res)
    # fraction of allowed parity holes that work
    tot=sum(len(h) for L,h in res); poss=sum(len([f for f in range(1,N+1) if (f-(N*(N+1)//2-sum(L)))%2==0]) for L,h in res)
    print(f"n={N}: parity-forced={par} holes ok {tot}/{poss} |", " | ".join(out))
