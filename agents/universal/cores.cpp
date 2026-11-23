// Cores at a cut on the interface machine (same model and pruning as ../peak/cut_check.cpp, which see).
// For every slack s <= B and l in {0, 1}:  CF(s, l) = states in F(x) for every legal prefix x ending at (s, l),
// CA(s, l) = states in A(y) for every suffix y from slack s with first letter >= l - 1,  U = CF and CA.
// Writes one line per state of CF or CA:  s l rowholes colholes inCF inCA inLE   (partitions as a.b.c, "-" = empty;
// inLE: in F(x) for every legal prefix x ending at slack s with last letter <= l).
// Usage: ./cores B > cores_B.txt     (all prefixes and suffixes with slacks <= B)
//        ./cores B w > /dev/null    also lists, per (s, l), a small set of prefixes whose F sets already intersect to CF
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

static string parts(u64 mask){
    vector<int> lam; int holes=0;
    for (int i=0;i<2*M+1;i++){ if (mask>>i&1) lam.push_back(holes); else holes++; }
    string s; for (int i=(int)lam.size()-1;i>=0;i--) if (lam[i]) s+=(s.empty()?"":".")+to_string(lam[i]);
    return s.empty()?"-":s;
}
int main(int argc, char** argv){
    B=atoi(argv[1]); M=B; if (B<1||B>31){ fprintf(stderr,"B must be 1..31\n"); return 1; }
    build();
    Fam X=explore(+1,false,true,0,B); Fam Y=explore(-1,false,true,0,B);
    for (int s=1;s<=B;s++) for (int l=0;l<=1;l++){
        auto it=X.at.find({s,l}); if (it==X.at.end()) continue;
        Bits CF(words(s),~0ULL), CA(words(s),~0ULL); int nf=0, na=0;
        for (int i: it->second){ nf++; for (size_t j=0;j<CF.size();j++) CF[j]&=X.sits[i].S[j]; }
        for (auto& kv: Y.at){ if (kv.first.first!=s||kv.first.second==NONE||kv.first.second<l-1) continue;
            for (int i: kv.second){ na++; for (size_t j=0;j<CA.size();j++) CA[j]&=Y.sits[i].S[j]; } }
        if (argc>2){                                   // greedy small subfamily of prefixes with the same intersection
            Bits cur(words(s),~0ULL); size_t n=lev[s].size(); if (n%64) cur.back()=(1ULL<<(n%64))-1;
            fprintf(stderr,"binding prefixes at (%d, %d):\n",s,l);
            for (;;){ long left=0; for (size_t j=0;j<cur.size();j++) left+=__builtin_popcountll(cur[j]&~CF[j]); if (!left) break;
                int best=-1; long bk=-1;
                for (int i: it->second){ long k=0; for (size_t j=0;j<cur.size();j++) k+=__builtin_popcountll(cur[j]&~X.sits[i].S[j]); if (k>bk){ bk=k; best=i; } }
                for (size_t j=0;j<cur.size();j++) cur[j]&=X.sits[best].S[j];
                fprintf(stderr,"   %-60s |F| %6ld  removes %6ld\n",str(X.sits[best].w).c_str(),cnt(X.sits[best].S),bk); }
        }
        Bits LE(words(s),~0ULL);                       // in F(x) for every x ending at slack s with last letter <= l
        for (auto& kv: X.at){ if (kv.first.first!=s||kv.first.second==NONE||kv.first.second>l) continue;
            for (int i: kv.second) for (size_t j=0;j<LE.size();j++) LE[j]&=X.sits[i].S[j]; }
        long nu=0, cf=0, ca=0;
        for (size_t j=0;j<lev[s].size();j++){ int f=CF[j>>6]>>(j&63)&1, a=CA[j>>6]>>(j&63)&1, le=LE[j>>6]>>(j&63)&1; cf+=f; ca+=a; nu+=f&a;
            if (f||a) printf("%d %d %s %s %d %d %d\n",s,l,parts(lev[s][j].r).c_str(),parts(lev[s][j].c).c_str(),f,a,le); }
        fprintf(stderr,"slack %2d last %d: %zu states, %4d F sets, %4d A sets, CF %6ld, CA %6ld, U %5ld\n",s,l,lev[s].size(),nf,na,cf,ca,nu);
    }
}
