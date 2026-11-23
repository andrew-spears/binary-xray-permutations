# Conjecture H: N=2m+1, hole f != m+1 (centre), L of size m with parity + density for P_f => pairing of P_f.
# Also report counterexamples at centre f=m+1, and check H covers all no-tight-cut valid L via f in {m-1,m,m+2,m+3}.
import itertools, sys
from sym import pairings, landau
M=int(sys.argv[1])
for m in range(1,M+1):
    N=2*m+1; cex_off=[]; cex_c=0; tested=0
    for L in itertools.combinations(range(1,2*m+1),m):
        Ls=sorted(L,reverse=True)
        for f in range(1,N+1):
            P=[x for x in range(1,N+1) if x!=f]
            if (sum(L)-sum(P))%2: continue
            if not all(sum(Ls[:K])<=sum(P[-K:])-sum(P[:K]) for K in range(1,m+1)): continue
            tested+=1
            if not pairings(L,N,f):
                if f==m+1: cex_c+=1
                else: cex_off.append((L,f))
    # coverage claim: every strictly valid L passes density at some f in {m-1,m,m+2,m+3} of right parity
    cov_bad=0
    for L in itertools.combinations(range(1,2*m+1),m):
        Ls=sorted(L,reverse=True)
        if not landau(L,N) or any(sum(Ls[:K])==K*(N-K) for K in range(1,m+1)): continue
        good=False
        for f in (m,m+2,m-1,m+3):
            if not 1<=f<=N: continue
            P=[x for x in range(1,N+1) if x!=f]
            if (sum(L)-sum(P))%2: continue
            if all(sum(Ls[:K])<=sum(P[-K:])-sum(P[:K]) for K in range(1,m+1)): good=True
        if not good: cov_bad+=1
    print(f"N={N}: tested={tested} centre-failures={cex_c} off-centre failures={len(cex_off)} {cex_off[:5]} | no-tight-cut L not covered={cov_bad}",flush=True)
