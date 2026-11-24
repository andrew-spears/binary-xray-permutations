// Universal states restricted to nonnegative-letter prefixes (machine and pruning: ../universal/cores.cpp).
// P(s, l) = states in F(x) for EVERY prefix x with all letters >= 0, slack s, last letter l (l = 0 or 1).
// U+(s) = P(s, 1) and conj P(s, 0)   (conj = conjugate both diagrams; A(y) = conj F(-reverse y)).
// A unimodal word cut after its last positive letter is  x | y  with x, -reverse(y) of this kind, so
// U+(s) nonempty for every s  ==>  every unimodal word is solvable.  Exact for all s <= B (the slack never exceeds s).
// Usage: ./uplus B [L]       summary on stderr; states of U+(s) on stdout:  s rowholes colholes
//        L > 0: prefix letters in 0..L only (the family 'letters in 0..L, then letters in -L..0'); default no cap.
//        L = -1: instead checks the unrestricted U(s, 0) of ../universal (test of conj).
#define main cores_main
#include "../universal/cores.cpp"
#undef main
// nonnegative-letter prefixes with letters <= cap; keeps the inclusion-minimal sets per (slack, last letter)
static Fam explore_cap(int cap){
    Fam F;
    auto add=[&](Bits&& S, int s, int l, vector<int8_t>&& w){
        if (empty(S)){ F.empties++; return; }
        auto& v=F.at[{s,l}];
        for (int i: v) if (sub(F.sits[i].S,S)) return;
        vector<int> keep; for (int i: v){ if (sub(S,F.sits[i].S)) F.sits[i].alive=false; else keep.push_back(i); }
        v.swap(keep);
        v.push_back(F.sits.size()); F.sits.push_back({std::move(S),s,l,std::move(w),true});
    };
    { Bits S0(1,1); add(std::move(S0),0,NONE,{}); }
    for (size_t q=0;q<F.sits.size();q++){
        if (!F.sits[q].alive) continue;
        int s=F.sits[q].s, l=F.sits[q].l, lo = l==NONE ? 0 : max(l-1,0);
        for (int e=lo;e<=min(cap,B-s);e++){ vector<int8_t> w=F.sits[q].w; w.push_back(e); Bits T=step(F.sits[q].S,s,e); add(std::move(T),s+e,e,std::move(w)); }
    }
    return F;
}
static u64 conjmask(u64 m){ u64 r=0; for (int i=0;i<2*M;i++) if (!(m>>(2*M-1-i)&1)) r|=1ULL<<i; return r; }
int main(int argc, char** argv){
    B=atoi(argv[1]); M=B; if (B<1||B>31) return 1;
    build();
    int L = argc>2 ? atoi(argv[2]) : 0;
    Fam X = L>0 ? explore_cap(L) : explore(+1,L==0,true,0,B);
    for (int s=1;s<=B;s++){
        size_t n=lev[s].size(); Bits P[2];
        int nf[2]={0,0};
        for (int l=0;l<=1;l++){ P[l].assign(words(s),~0ULL); if (n%64) P[l].back()=(1ULL<<(n%64))-1;
            auto it=X.at.find({s,l}); if (it==X.at.end()) continue;
            for (int i: it->second){ nf[l]++; for (size_t j=0;j<P[l].size();j++) P[l][j]&=X.sits[i].S[j]; } }
        if (L<0){ // unrestricted: U(s,0) = CF(s,0) and conj LE(s,1), LE(s,1) = all last letters <= 1
            Bits LE(words(s),~0ULL);
            for (auto& kv: X.at){ if (kv.first.first!=s||kv.first.second==NONE||kv.first.second>1) continue;
                for (int i: kv.second) for (size_t j=0;j<LE.size();j++) LE[j]&=X.sits[i].S[j]; }
            long u=0; string names;
            for (size_t j=0;j<n;j++){ if (!(P[0][j>>6]>>(j&63)&1)) continue;
                auto it=idx.find({conjmask(lev[s][j].r),conjmask(lev[s][j].c)}); if (it==idx.end()||slk[it->first]!=s){ fprintf(stderr,"conj leaves the level\n"); return 1; }
                uint32_t k=it->second; if (LE[k>>6]>>(k&63)&1){ u++; if (u<=4) names+=" "+name(s,j); } }
            fprintf(stderr,"slack %2d: unrestricted U(s,0) = %ld%s\n",s,u,names.c_str()); continue; }
        long u=0, p0=cnt(P[0]), p1=cnt(P[1]);
        for (size_t j=0;j<n;j++){ if (!(P[1][j>>6]>>(j&63)&1)) continue;
            auto it=idx.find({conjmask(lev[s][j].r),conjmask(lev[s][j].c)}); if (it==idx.end()||slk[it->first]!=s){ fprintf(stderr,"conj leaves the level\n"); return 1; }
            uint32_t k=it->second; if (P[0][k>>6]>>(k&63)&1){ u++; printf("%d %s %s\n",s,parts(lev[s][j].r).c_str(),parts(lev[s][j].c).c_str()); } }
        fprintf(stderr,"slack %2d: %6zu states; minimal F sets: %4d (last 1), %4d (last 0); P(s,1) %6ld, P(s,0) %6ld, U+ %6ld\n",s,n,nf[1],nf[0],p1,p0,u);
    }
}
