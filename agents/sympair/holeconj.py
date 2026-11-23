# "Generalized Nordh Conj 8 with one hole": for P = {1..N}\{f}, N=2m+1, L of size m:
# parity (sum L == sum P mod 2) + density (top-K(L) <= top-K(P) - bottom-K(P) for all K) => pairing of P?
import itertools, sys
from sym import pairings, landau
M=int(sys.argv[1])
for m in range(1,M+1):
    N=2*m+1; cex=[]; tested=0
    for L in itertools.combinations(range(1,2*m+1),m):
        Ls=sorted(L,reverse=True)
        for f in range(1,N+1):
            P=[x for x in range(1,N+1) if x!=f]
            if (sum(L)-sum(P))%2: continue
            ok=all(sum(Ls[:K])<=sum(P[-K:])-sum(P[:K]) for K in range(1,m+1))
            if not ok: continue
            tested+=1
            if not pairings(L,N,f): cex.append((L,f))
    print(f"N={N}: (L,f) passing parity+density={tested}, no pairing={len(cex)}",cex[:6],flush=True)
