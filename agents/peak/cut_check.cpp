// Two claims at a cut of the word, on the interface machine (same model as ../interface/rewrite.py):
//  (A) NONNEG: every legal prefix x with last letter l >= 0 and end slack s has a prefix x' with all letters >= 0,
//      the same (s, l), and F(x') inside F(x).
//  (B) universal cut states: for l in {0, 1} the intersection of all F(x) at (s, l), and of all A(y) at slack s
//      with first letter >= l - 1, is nonempty.
// All prefixes / suffixes with every slack <= B.  The states of slack s are indexed once (they are the pairs of
// partitions of total size s) and every set is a bitset over them.
// Pruning (default): if F(x1) is inside F(x2), same end slack, last(x1) <= last(x2), then F(x1 y) is inside
// F(x2 y) for every y legal after x2, so x2 is not extended; only the inclusion-minimal sets at each (s, l) are
// kept.  Both claims only depend on the minimal sets, so nothing is lost.  PRUNE = 0 keeps every set (slow; the
// first failure of (A) printed is then a shortest failing prefix).
// Usage: ./cut_check B [PRUNE=1] [LMAX=0] [VERBOSE=0] [AP=1] [DOB=1]
//   LMAX > 0: only prefixes x of length <= LMAX, (A) and (A') only;  VERBOSE: print a witness x' for every set;
//   AP = 0: skip (A') (x' never above its end slack), which costs B extra explorations;  DOB = 0: skip (B)
#include <bits/stdc++.h>
using namespace std;
typedef uint64_t u64; typedef vector<u64> Bits;
int B, M; const int NONE = -100;
struct St { u64 r, c; };
vector<vector<St>> lev;                          // states by slack
vector<vector<uint32_t>> off, dat;               // successors: off[s][i*(B+1)+(e+s)] .. into dat[s]
struct KH { size_t operator()(const pair<u64,u64>& k) const { u64 a=k.first*0x9E3779B97F4A7C15ULL^k.second; a^=a>>31; return a*0xff51afd7ed558ccdULL; } };
unordered_map<pair<u64,u64>,uint32_t,KH> idx;    // state -> index in its level
unordered_map<pair<u64,u64>,int,KH> slk;
static void succ(St t, int e, vector<St>& out){
    out.clear();
    for (int u=-M;u<=M;u++){
        int v=e-u; if (v<-M||v>M) continue;
        if ((t.r>>(M+u)&1)||(t.c>>(M+v)&1)) continue;
        u64 r2=t.r|(1ULL<<(M+u)), c2=t.c|(1ULL<<(M+v));
        if ((r2&1)&&(c2&1)) out.push_back({r2>>1,c2>>1});
    }
}
static void build(){
    lev.assign(B+1,{}); u64 base=(1ULL<<M)-1; St st{base,base};
    vector<pair<int,uint32_t>> todo; idx[{base,base}]=0; slk[{base,base}]=0; lev[0].push_back(st); todo.push_back({0,0});
    vector<St> o;
    for (size_t q=0;q<todo.size();q++){
        int s=todo[q].first; St t=lev[s][todo[q].second];
        for (int e=-s;e<=B-s;e++){ succ(t,e,o);
            for (St x: o) if (!idx.count({x.r,x.c})){ idx[{x.r,x.c}]=lev[s+e].size(); slk[{x.r,x.c}]=s+e; lev[s+e].push_back(x); todo.push_back({s+e,(uint32_t)lev[s+e].size()-1}); } }
    }
    off.assign(B+1,{}); dat.assign(B+1,{});
    for (int s=0;s<=B;s++){
        off[s].reserve(lev[s].size()*(B+1)+1);
        for (St t: lev[s]) for (int e=-s;e<=B-s;e++){ off[s].push_back(dat[s].size()); succ(t,e,o); for (St x: o) dat[s].push_back(idx[{x.r,x.c}]); }
        off[s].push_back(dat[s].size());
    }
}
static size_t words(int s){ return (lev[s].size()+63)/64; }
static Bits step(const Bits& S, int s, int e){
    Bits T(words(s+e),0);
    for (size_t w=0;w<S.size();w++) for (u64 x=S[w];x;x&=x-1){
        size_t i=w*64+__builtin_ctzll(x), k=i*(B+1)+(e+s);
        for (uint32_t p=off[s][k];p<off[s][k+1];p++){ uint32_t j=dat[s][p]; T[j>>6]|=1ULL<<(j&63); }
    }
    return T;
}
static Bits pre(const Bits& A, int s, int e){     // states of slack s - e with an e-successor in A (A at slack s)
    int s0=s-e; Bits T(words(s0),0);
    for (size_t i=0;i<lev[s0].size();i++){ size_t k=i*(B+1)+(e+s0);
        for (uint32_t p=off[s0][k];p<off[s0][k+1];p++){ uint32_t j=dat[s0][p]; if (A[j>>6]>>(j&63)&1){ T[i>>6]|=1ULL<<(i&63); break; } } }
    return T;
}
static bool sub(const Bits& a, const Bits& b){ for (size_t i=0;i<a.size();i++) if (a[i]&~b[i]) return false; return true; }
static bool empty(const Bits& a){ for (u64 x: a) if (x) return false; return true; }
static long cnt(const Bits& a){ long n=0; for (u64 x: a) n+=__builtin_popcountll(x); return n; }
static string str(const vector<int8_t>& w){ string s; for (int x: w) s+=(s.empty()?"":" ")+to_string(x); return s.empty()?"(empty)":s; }
static string diagram(u64 mask){                 // hole pattern as a partition (as in ../majority/core.py)
    vector<int> lam; int holes=0;
    for (int i=0;i<2*M+1;i++){ if (mask>>i&1) lam.push_back(holes); else holes++; }
    string s; for (int i=(int)lam.size()-1;i>=0;i--) if (lam[i]) s+= lam[i]<10 ? to_string(lam[i]) : "("+to_string(lam[i])+")";
    return s.empty()?"-":s;
}
static string name(int s, size_t i){ return diagram(lev[s][i].r)+"|"+diagram(lev[s][i].c); }
struct Sit { Bits S; int s, l; vector<int8_t> w; bool alive; };
struct Fam { vector<Sit> sits; map<pair<int,int>,vector<int>> at; long pruned=0, empties=0; };
static pair<u64,u64> hsh(const Bits& S, int s, int l){
    u64 h1=1469598103934665603ULL^(u64)(l+1000)^((u64)s<<20), h2=0x9E3779B97F4A7C15ULL*(u64)(l+1000+7919*s);
    for (u64 a: S){ h1=(h1^a)*1099511628211ULL; h1^=h1>>29; h2=(h2+a)*0xff51afd7ed558ccdULL; h2^=h2>>33; }
    return {h1,h2};
}
// dir = +1: prefixes (sets F), dir = -1: suffixes (sets A).  nonneg: prefix letters >= 0 only.
static Fam explore(int dir, bool nonneg, bool prune, int lmax, int bound){
    Fam F; set<pair<u64,u64>> seen;
    auto add=[&](Bits&& S, int s, int l, vector<int8_t>&& w){
        if (empty(S)){ F.empties++; return; }
        auto& v=F.at[{s,l}];
        if (prune){
            for (int i: v) if (sub(F.sits[i].S,S)) return;
            vector<int> keep; for (int i: v){ if (sub(S,F.sits[i].S)) F.sits[i].alive=false; else keep.push_back(i); }
            v.swap(keep);
        } else if (!seen.insert(hsh(S,s,l)).second) return;
        v.push_back(F.sits.size()); F.sits.push_back({std::move(S),s,l,std::move(w),true});
    };
    { Bits S0(1,1); add(std::move(S0),0,NONE,{}); }
    for (size_t q=0;q<F.sits.size();q++){
        if (!F.sits[q].alive) continue;
        int s=F.sits[q].s, l=F.sits[q].l;
        if (lmax && (int)F.sits[q].w.size()>=lmax) continue;
        if (prune && l!=NONE){ bool dom=false;       // a set at the same slack that allows at least the same continuations
            for (auto& kv: F.at){ if (kv.first.first!=s||kv.first.second==NONE) continue; int l2=kv.first.second;
                if (dir>0 ? l2>=l : l2<=l) continue;
                for (int i: kv.second) if (sub(F.sits[i].S,F.sits[q].S)){ dom=true; break; }
                if (dom) break; }
            if (dom){ F.pruned++; continue; } }
        if (dir>0){
            int lo = l==NONE ? 0 : max(l-1,-s); if (nonneg) lo=max(lo,0);
            for (int e=lo;e<=bound-s;e++){ vector<int8_t> w=F.sits[q].w; w.push_back(e); Bits T=step(F.sits[q].S,s,e); add(std::move(T),s+e,e,std::move(w)); }
        } else {
            int hi = l==NONE ? 0 : l+1;                // the letter before first letter l is <= l + 1; a last letter is <= 0
            for (int e=s-B;e<=min(hi,s);e++){ vector<int8_t> w; w.push_back(e); w.insert(w.end(),F.sits[q].w.begin(),F.sits[q].w.end()); Bits T=pre(F.sits[q].S,s,e); add(std::move(T),s-e,e,std::move(w)); }
        }
    }
    return F;
}
int main(int argc, char** argv){
    B=atoi(argv[1]); M=B; bool prune = argc>2 ? atoi(argv[2]) : 1; int lmax = argc>3 ? atoi(argv[3]) : 0; int verbose = argc>4 ? atoi(argv[4]) : 0; bool doAp = argc>5 ? atoi(argv[5]) : 1; bool doB = argc>6 ? atoi(argv[6]) : 1;
    if (B<1||B>31){ fprintf(stderr,"B must be 1..31\n"); return 1; }
    build(); long ns=0, nt=0; for (int s=0;s<=B;s++){ ns+=lev[s].size(); nt+=dat[s].size(); }
    printf("B = %d: %ld states, %ld transitions, %zu states at slack B\n",B,ns,nt,lev[B].size()); fflush(stdout);
    Fam P=explore(+1,true,true,0,B);
    long alive=0; for (auto& x: P.sits) alive+=x.alive;
    printf("nonnegative prefixes: %zu sets kept, %ld minimal, %ld not extended, %ld empty\n",P.sits.size(),alive,P.pruned,P.empties); fflush(stdout);
    Fam X=explore(+1,false,prune,lmax,B);
    alive=0; for (auto& x: X.sits) alive+=x.alive;
    printf("all prefixes%s: %zu sets kept, %ld %s, %ld not extended, %ld EMPTY\n",lmax?(" of length <= "+to_string(lmax)).c_str():"",X.sits.size(),alive,prune?"minimal":"distinct",X.pruned,X.empties); fflush(stdout);
    // (A)
    long tested=0, bad=0, badrel=0; map<int,long> bads, badl;
    for (auto& x: X.sits){ if (!x.alive||x.l==NONE||x.l<0) continue; tested++;
        bool ok=false; auto it=P.at.find({x.s,x.l});
        if (it!=P.at.end()) for (int i: it->second) if (sub(P.sits[i].S,x.S)){ ok=true; if (verbose) printf("  x = %s  (s %d, l %d)  <-  x' = %s\n",str(x.w).c_str(),x.s,x.l,str(P.sits[i].w).c_str()); break; }
        if (!ok){ bool ok2=false;                    // relaxed: x' nonnegative, same end slack, last letter <= l
            for (int l2=0;l2<x.l&&!ok2;l2++){ auto i2=P.at.find({x.s,l2}); if (i2!=P.at.end()) for (int i: i2->second) if (sub(P.sits[i].S,x.S)){ ok2=true; if (bad<12) printf("(A) fails, relaxed form holds: x = %s <- x' = %s (last letter %d)\n",str(x.w).c_str(),str(P.sits[i].w).c_str(),l2); break; } }
            if (!ok2) badrel++; badl[x.l]++; }
        if (!ok){ bad++; bads[x.s]++; if (bad<=12||x.l<=1){ printf("(A) FAILS: x = %s  (length %zu, end slack %d, last letter %d, |F(x)| = %ld of %zu states)\n",str(x.w).c_str(),x.w.size(),x.s,x.l,cnt(x.S),lev[x.s].size());
            vector<tuple<long,int,size_t>> near;      // nonnegative candidates by number of states outside F(x)
            if (it!=P.at.end()) for (int i: it->second){ long d=0; size_t ex=0; for (size_t j=0;j<lev[x.s].size();j++) if ((P.sits[i].S[j>>6]>>(j&63)&1)&&!(x.S[j>>6]>>(j&63)&1)){ if (!d) ex=j; d++; } near.push_back({d,i,ex}); }
            sort(near.begin(),near.end()); printf("      %zu minimal nonnegative sets at (%d, %d); closest:\n",near.size(),x.s,x.l);
            for (size_t k=0;k<near.size()&&k<3;k++){ int i=get<1>(near[k]); printf("      x' = %s: |F(x')| = %ld, %ld states not in F(x), e.g. %s\n",str(P.sits[i].w).c_str(),cnt(P.sits[i].S),get<0>(near[k]),name(x.s,get<2>(near[k])).c_str()); } } } }
    printf("(A) NONNEG: %ld sets tested, %ld failures",tested,bad); for (auto& kv: bads) printf("  [slack %d: %ld]",kv.first,kv.second); printf("\n"); printf("    failures by last letter:"); for (auto& kv: badl) printf("  [%d: %ld]",kv.first,kv.second); printf("\n    relaxed form (x' nonnegative, same end slack, last letter <= l): %ld failures\n",badrel); fflush(stdout);
    if (verbose==2 && !prune){   // is there ONE nonnegative x' per (s, l) inside F(x) for every x at (s, l) whose set is not F of a nonnegative word?
        Fam Q=explore(+1,true,false,0,B); set<pair<u64,u64>> nn; for (auto& x: Q.sits) nn.insert(hsh(x.S,x.s,x.l));
        map<pair<int,int>,vector<int>> oth; for (size_t i=0;i<X.sits.size();i++){ auto& x=X.sits[i]; if (x.l!=NONE&&x.l>=0&&!nn.count(hsh(x.S,x.s,x.l))) oth[{x.s,x.l}].push_back(i); }
        for (auto& kv: oth){ auto it=P.at.find(kv.first); int k=0; string ex;
            if (it!=P.at.end()) for (int i: it->second){ bool all=true; for (int j: kv.second) if (!sub(P.sits[i].S,X.sits[j].S)){ all=false; break; } if (all){ if (k<4) ex+="  ["+str(P.sits[i].w)+"]"; k++; } }
            if (getenv("WIT")) for (int j: kv.second){ string wl; int c=0; if (it!=P.at.end()) for (int i: it->second) if (sub(P.sits[i].S,X.sits[j].S)){ if (c<6) wl+="  ["+str(P.sits[i].w)+"]"; c++; } printf("   x = %-28s %3d x':%s\n",str(X.sits[j].w).c_str(),c,wl.c_str()); }
            printf("common x' at slack %2d last %d: %4zu other sets, %3zu minimal nonnegative sets, %3d inside all others:%s\n",kv.first.first,kv.first.second,kv.second.size(),it==P.at.end()?0:it->second.size(),k,ex.c_str()); }
    }
    // (A'): x' may have negative letters but never rises above its end slack
    if (doAp){ long t2=0, bad2=0, shown=0; map<pair<int,int>,vector<Bits>> low;
      for (int Pk=0;Pk<=B;Pk++){ Fam L=explore(+1,false,true,0,Pk); for (auto& kv: L.at) if (kv.first.first==Pk) for (int i: kv.second) low[kv.first].push_back(std::move(L.sits[i].S)); }
      for (auto& x: X.sits){ if (!x.alive||x.l==NONE||x.l<0) continue; t2++; bool ok=false;
          for (auto& S: low[{x.s,x.l}]) if (sub(S,x.S)){ ok=true; break; }
          if (!ok){ bad2++; if (shown++<10) printf("(A') FAILS: x = %s  (length %zu, end slack %d, last letter %d)\n",str(x.w).c_str(),x.w.size(),x.s,x.l); } }
      printf("(A') x' never above its end slack: %ld sets tested, %ld failures\n",t2,bad2); fflush(stdout); }
    if (lmax || !doB) return 0;
    // (B)
    Fam Y=explore(-1,false,prune,0,B);
    alive=0; for (auto& x: Y.sits) alive+=x.alive;
    printf("all suffixes: %zu sets kept, %ld %s, %ld not extended, %ld empty (dropped)\n",Y.sits.size(),alive,prune?"minimal":"distinct",Y.pruned,Y.empties);
    for (int s=1;s<=B;s++) for (int l=-1;l<=2;l++){
        auto it=X.at.find({s,l}); if (it==X.at.end()) continue;
        Bits U(words(s),~0ULL); int nf=0, na=0;
        for (int i: it->second){ nf++; for (size_t j=0;j<U.size();j++) U[j]&=X.sits[i].S[j]; }
        if (lev[s].size()%64) U.back()&=(1ULL<<(lev[s].size()%64))-1;
        long uf=cnt(U); Bits UF=U; long miss=0;
        for (auto& kv: Y.at){ if (kv.first.first!=s||kv.first.second==NONE||kv.first.second<l-1) continue;
            for (int i: kv.second){ na++; bool meet=false; for (size_t j=0;j<U.size();j++){ if (UF[j]&Y.sits[i].S[j]) meet=true; U[j]&=Y.sits[i].S[j]; } if (!meet) miss++; } }
        string ex; int k=0; for (size_t j=0;j<lev[s].size()&&k<6;j++) if (U[j>>6]>>(j&63)&1){ ex+=" "+name(s,j); k++; }
        printf("(B) slack %2d last %2d: %5d F, %5d A, in all F %5ld, A sets missing them %ld, universal %4ld: %s\n",s,l,nf,na,uf,miss,cnt(U),ex.c_str());
    }
}
