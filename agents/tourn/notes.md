# Davis–Schroeder arXiv:2606.21532 — definitions (extracted 2026-11-22)
Conventions: vertices Z_n={0..n-1}; phi in S_n; C(phi)={i+phi(i)} (antidiagonal x-ray; binary iff distinct);
c(phi)=sorted C. alpha(c)_j = c_j - j. Our D convention: reflect phi -> n-1-phi gives i+phi(i)=n-1-d, so
c sorted <-> -D, i.e. alpha(c) = our score seq for the mirror -D (harmless).
T(phi): transitive tournament, vertex i has phi(i) wins. T^2(phi)=T(eps)+T(phi) (2-tournament, weights 0/1/2:
 w(x,y)=2 if x>y & phi(x)>phi(y); 0 if x<y & phi(x)<phi(y); 1 otherwise). Lemma 3.1: s(T^2(phi))=c(phi).
TTD: k-tournament = sum of k transitive tournaments (adjacency matrices add).
Thm 3.4 (gamma): phi binary. T=T^2(phi), scores strictly increasing; rho(i)=rank of s_T(i). T(rho) is contained
 in T (w>=1 on rank-increasing pairs); gamma(phi):=T - T(rho). Then s(gamma(phi)) = alpha(c(phi)).
Lemma 3.5 (delta): for tournament T, need transitive T' with x<_{T'}y => s_T(x)<=s_T(y) (T' = score order, ties
 broken any way) such that T+T' has a TTD (=R1+R2). Then R1,R2 give phi (Lemma 3.2) with c(phi)=s(T+T')=
 (s_j+j), so alpha(c(phi))=s(T). Ex 3.7: some T with s=(1,1,2,3,3) fails for every T'.

## Reformulation (mine)
T+T' = R1+R2 iff P := (arcs of T that agree with T') is a partial order of dimension <= 2
 (weight-2 arcs = R1∩R2 = P; weight-1 pairs = upsets = incomparable pairs).
domain(delta) = image(gamma) exactly (up to permuting tied vertices): if T accepted, gamma(delta(T)) = T.
Explicit gamma: points (i,phi(i)); label by rank of i+phi(i). p beats q iff p is NE of q (dominance), or
 p,q form an inversion (NW/SE) and p has the SMALLER antidiagonal i+phi(i). Upsets of gamma(phi) = inversions of phi.
So "every score seq has an accepted tournament" is literally equivalent to the conjecture.

## Results (2026-11-22)
- check_gamma.out: gamma lands on alpha(c(phi)) for all witnesses n<=8; delta(gamma(phi)) round-trips.
- check_domain.out: exhaustive n<=6: delta accepts T <=> T in tie-closure of gamma image (0 mismatches).
- stats_{5..8}.out: every valid s has >=1 accepted tournament (equivalent to conjecture, already known n<=22).
  Accepted fraction of labelled tournaments with score s: min/mean n=6 .25/.56, n=7 .090/.42, n=8 .022/.24.
- Candidates for a canonical accepted tournament, all fail:
  * staircase/local (upsets i<j iff j<=f(i), f nondecr.): usually don't exist (n=8: only 23/61 s); a few exist but rejected.
  * round/rotational: exist for 7/61 s at n=8.
  * Havel-Hakimi greedy (4 variants): best 39/61 at n=8.
  * max strict upsets: accepted set attains the max for all s, n<=8 (maxup.out), FAILS at n=9:
    s=(1,2,3,3,4,5,5,6,7) (accepted max 10 vs 11), (1,2,3,4,4,5,5,6,6) and its converse (11 vs 12).
