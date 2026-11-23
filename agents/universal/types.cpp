// Step-closed sets indexed by a coarse, letter-updatable TYPE of the prefix (interface machine as in cores.cpp).
// type(x e) is a function of type(x) and e.  J = the largest family with J(empty word) = {start} and
//     J(type(x e))  inside  step_e(J(type(x)))      for every legal prefix x e with slacks <= B,
// so J(type(x)) is inside F(x), and conj J(type(-reverse y)) is inside A(y) (reversal symmetry, REPORT.md section 1).
// Needed (../weights/REPORT.md section 0: every nonzero word has neighbouring letters 1, 0): at every slack s,
//     J(t) meets conj J(t')   for all types t ending in letter 1 and t' ending in letter 0 at slack s.     ("pairs")
// Usage: ./types B FEATURES [dump|sizes]    FEATURES = letters, each optionally followed by a cap:
//   R[c]  r = length of the final run of letters falling by exactly 1 (with Q: the run that ends where the final
//         run of equal letters starts), capped at c
//   Q[c]  length of the final run of equal letters, capped at c (default 2)
//   P     the letter just before that run (run = falling run, then equal run if Q is on)
//   M[c]  last letter that was larger than its predecessor (or the first letter), and how many letters ago, capped c
//   L[k]  the k letters before the last one (default 1)
//   A[k]  as L, but the window is cleared when a letter is larger than its predecessor (so: the final non-increasing
//         run, at most k + 1 letters);   C[k]  the same, but cleared one letter earlier: the last k + 1 letters, cut off
//         just before the letter that precedes the last rise (that letter is forgotten once the run has k + 1 letters)
//         With the environment variable NEED=file (lines: slack, last letter, the one before, ...; L must come first)
//         the window is variable: the k-th letter before the last is kept only if the slack and the letters after it
//         are a line of the file (and the letter was still known one step earlier).  See ctx.py.
//         With CLAMP=lo,hi the letters kept in the L window are clamped to [lo, hi] (the last letter stays exact).
//         With CLAMPL=lo,hi the last letter is clamped too (lo <= -1, hi >= 2; use only with L): then the number
//         of types is at most (B + 1) * const.  A clamped last letter allows every continuation that is legal for some
//         letter of its class, so some types are reached by no legal prefix: WORKS is still sound, a failure may be spurious.
//   T     whether the slack bound B was reached before the last letter
//   E[c] Z[c] N[c] G[c]   number of even letters / zeros / letters / negative letters so far, capped at c
//   H     largest slack so far
//   K     only types with last letter <= 1 carry a set: a run of letters >= 2 and its closing letter 1 is one block,
//         inside which the exact reachable sets are followed (as in ../majority/blockinv.py)
//         With KLO=lo only types with last letter in [lo, 1] carry a set (KLO=0: a run of negative letters and the
//         letter after it is a block too).
// The type always contains the slack and the last letter.   dump: print J(t) for every type with slack <= 8
// (or <= DUMPMAX).   sizes (instead of dump): the table of |J(t)| for types ending in 0 or 1 (slack printed as 0).
// LET=lo,hi: only words with all letters in [lo, hi] (the family and the pair test are then for that class of words).
// Other environment variables: DIAG=1 (the first type whose set becomes empty, and the constraints on it),
// MINIMIZE=1 (number of types after merging types with equal sets and equivalent futures), CORE=1 (compare J(t) with
// the exact intersection C(t) of F(x) over all prefixes x of type t, small B only; also checks J(t) inside C(t)).
#include <bits/stdc++.h>
using namespace std;
typedef uint64_t u64; typedef vector<u64> Bits; typedef vector<int> Key;
int B, M; const int NONE = -100;
struct St { u64 r, c; };
vector<vector<St>> lev; vector<vector<uint32_t>> off, dat, cj;
map<pair<u64,u64>,uint32_t> idx;
static void succ(St t, int e, vector<St>& out){
    out.clear();
    for (int u=-M;u<=M;u++){
        int v=e-u; if (v<-M||v>M) continue;
        if ((t.r>>(M+u)&1)||(t.c>>(M+v)&1)) continue;
        u64 r2=t.r|(1ULL<<(M+u)), c2=t.c|(1ULL<<(M+v));
        if ((r2&1)&&(c2&1)) out.push_back({r2>>1,c2>>1});
    }
}
static u64 conj(u64 m){ u64 r=0; for (int i=0;i<2*M;i++) if (!(m>>(2*M-1-i)&1)) r|=1ULL<<i; return r; }
static void build(){
    lev.assign(B+1,{}); u64 base=(1ULL<<M)-1; St st{base,base};
    vector<pair<int,uint32_t>> todo; idx[{base,base}]=0; lev[0].push_back(st); todo.push_back({0,0});
    vector<St> o;
    for (size_t q=0;q<todo.size();q++){
        int s=todo[q].first; St t=lev[s][todo[q].second];
        for (int e=-s;e<=B-s;e++){ succ(t,e,o);
            for (St x: o) if (!idx.count({x.r,x.c})){ idx[{x.r,x.c}]=lev[s+e].size(); lev[s+e].push_back(x); todo.push_back({s+e,(uint32_t)lev[s+e].size()-1}); } }
    }
    off.assign(B+1,{}); dat.assign(B+1,{}); cj.assign(B+1,{});
    for (int s=0;s<=B;s++){
        for (St t: lev[s]) for (int e=-s;e<=B-s;e++){ off[s].push_back(dat[s].size()); succ(t,e,o); for (St x: o) dat[s].push_back(idx[{x.r,x.c}]); }
        off[s].push_back(dat[s].size());
        for (St t: lev[s]){ auto it=idx.find({conj(t.r),conj(t.c)}); if (it==idx.end()){ fprintf(stderr,"conj missing\n"); exit(1);} cj[s].push_back(it->second); }
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
static Bits conjset(const Bits& S, int s){
    Bits T(S.size(),0);
    for (size_t w=0;w<S.size();w++) for (u64 x=S[w];x;x&=x-1){ uint32_t j=cj[s][w*64+__builtin_ctzll(x)]; T[j>>6]|=1ULL<<(j&63); }
    return T;
}
static bool meet(const Bits& a, const Bits& b){ for (size_t i=0;i<a.size();i++) if (a[i]&b[i]) return true; return false; }
static bool isempty(const Bits& a){ for (u64 x: a) if (x) return false; return true; }
static long cnt(const Bits& a){ long n=0; for (u64 x: a) n+=__builtin_popcountll(x); return n; }
static bool andin(Bits& a, const Bits& b){ bool ch=false; for (size_t i=0;i<a.size();i++){ u64 x=a[i]&b[i]; if (x!=a[i]){ a[i]=x; ch=true; } } return ch; }
static string diagram(u64 mask){
    vector<int> lam; int holes=0;
    for (int i=0;i<2*M+1;i++){ if (mask>>i&1) lam.push_back(holes); else holes++; }
    string s; for (int i=(int)lam.size()-1;i>=0;i--) if (lam[i]) s+= lam[i]<10 ? to_string(lam[i]) : "("+to_string(lam[i])+")";
    return s.empty()?"-":s;
}
static string name(int s, size_t i){ return diagram(lev[s][i].r)+"|"+diagram(lev[s][i].c); }
static string str(const vector<int8_t>& w){ string s; for (int x: w) s+=(s.empty()?"":" ")+to_string(x); return s.empty()?"(empty)":s; }

// ---- types.  Key = [s, l, features...]
struct Feat { char c; int cap; int pos; };
set<Key> need; bool needon=false; const int WILD=-101; int clo=-1000, chi=1000; int llo=-1000, lhi=1000;
vector<Feat> feats; bool hasQ=false, blocks=false; int qpos=-1;
static Key root(){ Key k={0,NONE}; for (auto& f: feats){ if (f.c=='M'){ k.push_back(NONE); k.push_back(0);} else if (f.c=='L'||f.c=='A'||f.c=='C'){ for (int i=0;i<f.cap;i++) k.push_back(NONE);} else if (f.c=='R'||f.c=='Q') k.push_back(0); else if (f.c=='P') k.push_back(NONE); else k.push_back(0); } return k; }
static Key upd(const Key& k, int e){
    int s=k[0], l=k[1]; Key n=k; n[0]=s+e; n[1]=max(llo,min(lhi,e));
    int q = hasQ ? k[qpos] : 1;
    for (auto& f: feats){ int p=f.pos;
        switch (f.c){
        case 'R': if (l==NONE) n[p]=1; else if (e==l-1) n[p]= (q>1 ? 2 : min(k[p]+1,f.cap)); else if (e==l&&hasQ) n[p]=k[p]; else n[p]=1; break;
        case 'Q': n[p]= (l!=NONE&&e==l) ? min(k[p]+1,f.cap) : 1; break;
        case 'P': if (l==NONE) n[p]=NONE; else if (e==l-1) n[p]= (q>1 ? l : k[p]); else if (e==l&&hasQ) n[p]=k[p]; else n[p]=l; break;
        case 'M': if (l==NONE||e>l){ n[p]=e; n[p+1]=0; } else n[p+1]=min(k[p+1]+1,f.cap); break;
        case 'L': if (!f.cap) break; for (int i=0;i+1<f.cap;i++) n[p+i]=k[p+i+1]; n[p+f.cap-1]= l==NONE ? NONE : max(clo,min(chi,l)); break;   // L0 = no window
        case 'A': case 'C': if (!f.cap) break; if (l==NONE||e>l){ for (int i=0;i<f.cap;i++) n[p+i]=NONE; if (f.c=='C') n[p+f.cap-1]=l; }
                  else { for (int i=0;i+1<f.cap;i++) n[p+i]=k[p+i+1]; n[p+f.cap-1]=l; } break;
        case 'T': n[p]= k[p] || s==B; break;
        case 'E': n[p]=min(k[p]+(e%2==0),f.cap); break;
        case 'Z': n[p]=min(k[p]+(e==0),f.cap); break;
        case 'N': n[p]=min(k[p]+1,f.cap); break;
        case 'G': n[p]=min(k[p]+(e<0),f.cap); break;
        case 'H': n[p]=max(k[p],s+e); break;
        }
    }
    if (needon){ auto& f=feats[0];                // variable window: letter k + 1 is kept only if (slack, last k letters) is in the list
        Key c={n[0],n[1]}; int k=1;
        while (k<=f.cap && n[f.pos+f.cap-k]!=WILD && need.count(c)){ c.push_back(n[f.pos+f.cap-k]); k++; }
        for (int i=k;i<=f.cap;i++) n[f.pos+f.cap-i]=WILD; }
    return n;
}
static string kstr(const Key& k){ string s="("; for (size_t i=0;i<k.size();i++) s+=(i?",":"")+(k[i]==NONE?string("."):k[i]==WILD?string("*"):to_string(k[i])); return s+")"; }

int main(int argc, char** argv){
    B=atoi(argv[1]); M=B+2; string fs=argc>2?argv[2]:""; bool dump=argc>3;
    for (size_t i=0;i<fs.size();){ char c=fs[i++]; int cap=0; bool has=false; while (i<fs.size()&&isdigit(fs[i])){ cap=cap*10+fs[i++]-'0'; has=true; }
        if (c=='K'){ blocks=true; continue; }
        if (!has) cap = c=='Q'?2 : (c=='L'||c=='A'||c=='C')?1 : c=='M'?3 : 1000;
        feats.push_back({c,cap,0}); }
    { int p=2; for (auto& f: feats){ f.pos=p; if (f.c=='Q'){ hasQ=true; qpos=p; } p+= f.c=='M'?2 : (f.c=='L'||f.c=='A'||f.c=='C')?f.cap : 1; } }
    if (getenv("NEED")){ needon=true; ifstream in(getenv("NEED")); string line;
        while (getline(in,line)){ Key k; stringstream t2(line); int a; while (t2>>a) k.push_back(a); if (!k.empty()) need.insert(k); } }
    if (getenv("CLAMP")) sscanf(getenv("CLAMP"),"%d,%d",&clo,&chi);
    if (getenv("CLAMPL")) sscanf(getenv("CLAMPL"),"%d,%d",&llo,&lhi);
    int elo=-1000, ehi=1000; if (getenv("LET")) sscanf(getenv("LET"),"%d,%d",&elo,&ehi);      // only words with letters in [lo, hi]
    build();
    map<Key,int> id; vector<Key> keys; vector<vector<int8_t>> rep; vector<vector<pair<int,int>>> out;
    id[root()]=0; keys.push_back(root()); rep.push_back({}); out.push_back({});
    for (size_t q=0;q<keys.size();q++){
        Key k=keys[q]; int s=k[0], l=k[1];
        for (int e=(l==NONE?0: l<=llo?-s : max(l-1,-s)); e<=B-s; e++){     // l = lhi stands for every letter >= lhi, l = llo for every letter <= llo
            if (e<elo||e>ehi) continue;
            Key n=upd(k,e); auto it=id.find(n); int j;
            if (it==id.end()){ j=keys.size(); id[n]=j; keys.push_back(n); auto w=rep[q]; w.push_back(e); rep.push_back(w); out.push_back({}); } else j=it->second;
            out[q].push_back({e,j});
        }
    }
    int T=keys.size(); vector<Bits> J(T);
    int klo=getenv("KLO")?atoi(getenv("KLO")):-1000;
    auto carries=[&](int t){ return !blocks || (keys[t][1]<=1 && (keys[t][1]>=klo || keys[t][1]==NONE)); };
    for (int t=0;t<T;t++){ int s=keys[t][0]; J[t].assign(words(s),~0ULL); size_t n=lev[s].size(); if (n%64) J[t].back()=(1ULL<<(n%64))-1; }
    J[0].assign(words(0),0); J[0][0]=1;
    deque<int> work; vector<char> inq(T,1); for (int t=0;t<T;t++) if (carries(t)) work.push_back(t);
    long steps=0; bool diag=getenv("DIAG")!=nullptr, done=false;
    vector<vector<pair<int,int>>> in(T); for (int t=0;t<T;t++) for (auto [e,t2]: out[t]) in[t2].push_back({e,t});
    auto report=[&](int t2){ if (!diag||done||!isempty(J[t2])) return; done=true; int s2=keys[t2][0];
        printf("first empty: %s [%s]; constraints from\n", kstr(keys[t2]).c_str(), str(rep[t2]).c_str());
        for (auto [e,t]: in[t2]){ Bits S=step(J[t],keys[t][0],e); printf("   %s [%s] |J| = %ld, step %ld:", kstr(keys[t]).c_str(), str(rep[t]).c_str(), cnt(J[t]), cnt(S));
            int c=0; for (size_t i=0;i<lev[s2].size()&&c<12;i++) if (S[i>>6]>>(i&63)&1){ printf(" %s", name(s2,i).c_str()); c++; } printf("\n"); } };
    while (!work.empty()){
        int t=work.front(); work.pop_front(); inq[t]=0; int s=keys[t][0];
        if (!blocks){
            for (auto [e,t2]: out[t]){ Bits S=step(J[t],s,e); steps++; if (andin(J[t2],S)){ report(t2); if (!inq[t2]){ inq[t2]=1; work.push_back(t2); } } }
        } else {                                   // follow exact sets through types with last letter >= 2
            vector<pair<int,Bits>> st; st.push_back({t,J[t]}); set<pair<int,Bits>> memo;
            while (!st.empty()){ auto [a,S]=st.back(); st.pop_back();
                for (auto [e,t2]: out[a]){ Bits S2=step(S,keys[a][0],e); steps++;
                    if (carries(t2)){ if (andin(J[t2],S2)&&!inq[t2]){ inq[t2]=1; work.push_back(t2); } }
                    else if (memo.insert({t2,S2}).second) st.push_back({t2,S2}); } }
        }
    }
    printf("bound %d, features '%s': %d types (%d carrying a set), %ld steps\n", B, fs.c_str(), T, (int)[&]{ int c=0; for (int t=0;t<T;t++) c+=carries(t); return c; }(), steps);
    long totbad=0, totempty=0; int firstbad=-1; vector<long> badat(B+1,0);
    for (int s=1;s<=B;s++){
        vector<int> t1, t0; int ne=0, nt=0;
        for (int t=0;t<T;t++) if (keys[t][0]==s&&carries(t)){ nt++; if (isempty(J[t])) ne++; if (keys[t][1]==1) t1.push_back(t); if (keys[t][1]==0) t0.push_back(t); }
        map<Bits,int> d1, d0;                       // distinct sets, with one type each
        for (int t: t1) d1.insert({J[t],t});
        for (int t: t0) d0.insert({conjset(J[t],s),t});
        long bad=0; int b1=-1, b0=-1;
        for (auto& a: d1) for (auto& b: d0) if (!meet(a.first,b.first)){ bad++; if (b1<0){ b1=a.second; b0=b.second; } }
        Bits c1(words(s),~0ULL), c0(words(s),~0ULL); for (auto& a: d1) andin(c1,a.first); for (auto& b: d0) andin(c0,b.first);
        long u = (d1.empty()||d0.empty()) ? -1 : cnt([&]{ Bits x=c1; andin(x,c0); return x; }());
        printf("  slack %2d: %5d types, %4d empty; ending in 1: %4zu types, %4zu sets; ending in 0: %4zu types, %4zu sets; bad pairs %5ld; in all of them %5ld",
               s, nt, ne, t1.size(), d1.size(), t0.size(), d0.size(), bad, u);
        if (bad) printf("   e.g. %s [%s] (%ld) vs %s [%s] (%ld)", kstr(keys[b1]).c_str(), str(rep[b1]).c_str(), cnt(J[b1]), kstr(keys[b0]).c_str(), str(rep[b0]).c_str(), cnt(J[b0]));
        printf("\n"); totbad+=bad; totempty+=ne; badat[s]=bad; if (bad&&firstbad<0) firstbad=s;
    }
    printf("summary: bound %d '%s': types %d, empty %ld, bad pairs %ld (first at slack %d), bad pairs at slack B: %ld  => %s\n", B, fs.c_str(), T, totempty, totbad, firstbad, badat[B],
           totbad==0 ? (totempty==0 ? "WORKS" : "no bad pair, but empty sets (at types that cannot be continued within the bound)") : badat[B]==0 ? "fails (top slack alone is fine)" : "FAILS");
    if (getenv("MINIMIZE")){                       // Moore minimisation: merge types with equal sets and equivalent futures
        vector<int> cls(T); { map<pair<int,Bits>,int> m; for (int t=0;t<T;t++) cls[t]=m.insert({{keys[t][0],J[t]},(int)m.size()}).first->second;
            printf("minimise: %d types, %zu distinct (slack, set)", T, m.size()); }
        for (;;){ map<vector<int>,int> m; vector<int> nc(T);
            for (int t=0;t<T;t++){ vector<int> sig={cls[t]}; for (auto [e,t2]: out[t]){ sig.push_back(e); sig.push_back(cls[t2]); } nc[t]=m.insert({sig,(int)m.size()}).first->second; }
            bool same = (int)m.size()==*max_element(cls.begin(),cls.end())+1; cls=nc; if (same) break; }
        int nc=*max_element(cls.begin(),cls.end())+1; printf(", %d classes after minimisation\n", nc);
        map<pair<int,int>,array<set<int>,2>> per; map<pair<int,int>,int> ntp;
        for (int t=0;t<T;t++){ auto k=make_pair(keys[t][0],keys[t][1]); per[k][0].insert(cls[t]); ntp[k]++; }
        for (auto& [k,v]: per) if (k.second>=-1&&k.second<=2) printf("   slack %d last %d: %d types, %zu classes\n", k.first, k.second, ntp[k], v[0].size());
        if (strlen(getenv("MINIMIZE"))>1){ map<int,vector<int>> mem; for (int t=0;t<T;t++) mem[cls[t]].push_back(t);
            for (auto& [c,v]: mem){ int t=v[0]; if (keys[t][1]<0||keys[t][1]>1||keys[t][0]>atoi(getenv("MINIMIZE"))) continue; printf("class s=%d l=%d |J|=%ld:", keys[t][0], keys[t][1], cnt(J[t])); for (int u: v) printf(" %s", kstr(keys[u]).c_str()); printf("\n"); } }
    }
    if (getenv("CORE")){                           // exact cores C(t) = intersection of F(x) over all prefixes x of type t (slacks <= B)
        vector<Bits> C(T); vector<char> seen(T,0); set<pair<int,Bits>> memo; vector<pair<int,Bits>> st; Bits s0(words(0),0); s0[0]=1;
        st.push_back({0,s0}); memo.insert({0,s0});
        while (!st.empty()){ auto [t,S]=st.back(); st.pop_back();
            if (!seen[t]){ seen[t]=1; C[t]=S; } else andin(C[t],S);
            for (auto [e,t2]: out[t]){ Bits S2=step(S,keys[t][0],e); if (memo.insert({t2,S2}).second) st.push_back({t2,S2}); } }
        long eq=0, ne=0, closed=0, notclosed=0, emptyJ=0, unsound=0; int ex=-1;
        for (int t=0;t<T;t++){ if (!carries(t)) continue; { Bits X=J[t]; if (andin(X,C[t])) unsound++; } if (C[t]==J[t]) eq++; else { ne++; if (isempty(J[t])) emptyJ++; if (ex<0||keys[t][0]<keys[ex][0]) ex=t; }
            for (auto [e,t2]: out[t]){ Bits S=step(C[t],keys[t][0],e), X=C[t2]; if (andin(X,S)) notclosed++; else closed++; } }
        printf("cores: %zu (type, F-set) pairs; J(t) not inside C(t) for %ld types (must be 0); J(t) = C(t) for %ld types, smaller for %ld (J empty in %ld of them); C(t2) inside step_e C(t): %ld transitions yes, %ld no\n", memo.size(), unsound, eq, ne, emptyJ, closed, notclosed);
        if (ex>=0) printf("   first difference: %s [%s] |J| = %ld, |C| = %ld\n", kstr(keys[ex]).c_str(), str(rep[ex]).c_str(), cnt(J[ex]), cnt(C[ex]));
    }
    if (dump&&!strcmp(argv[3],"sizes")){            // |J(t)| for every type ending in 0 or 1, one line per window, one column per slack
        map<Key,map<int,long>> tab; for (int t=0;t<T;t++) if (keys[t][1]==0||keys[t][1]==1){ Key k(keys[t].begin()+1,keys[t].end()); tab[k][keys[t][0]]=cnt(J[t]); }
        printf("%-24s","states"); for (int s=1;s<=B;s++) printf(" %6zu", lev[s].size()); printf("\n");
        for (auto& [k,v]: tab){ Key k2={0}; k2.insert(k2.end(),k.begin(),k.end()); printf("%-24s", kstr(k2).c_str()); for (int s=1;s<=B;s++){ if (v.count(s)) printf(" %6ld", v[s]); else printf("      -"); } printf("\n"); }
        return 0; }
    if (dump) for (int t=0;t<T;t++) if (keys[t][0]>=1&&keys[t][0]<=(getenv("DUMPMAX")?atoi(getenv("DUMPMAX")):8)&&carries(t)){
        int s=keys[t][0]; printf("J%s [%s] %ld:", kstr(keys[t]).c_str(), str(rep[t]).c_str(), cnt(J[t]));
        vector<string> v; for (size_t i=0;i<lev[s].size();i++) if (J[t][i>>6]>>(i&63)&1) v.push_back(name(s,i)); sort(v.begin(),v.end()); for (auto& x: v) printf(" %s", x.c_str()); printf("\n"); }
}
