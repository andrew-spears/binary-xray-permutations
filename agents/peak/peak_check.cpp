// PEAK on the interface machine: F(x 0) inside F(x 1 0 -1) for every legal prefix x with all slacks <= B
// (same model and situations as ../interface/run_rule.py: tight cuts allowed, no completability pruning).
// BFS by prefix length over (reachable set, slack, last letter); only the current level is kept in memory and
// situations are deduplicated by a 128-bit hash, so memory stays small.  The first failure printed is a shortest one.
// Usage: ./peak_check B [lo] [cap] [L]
//   lo, cap = only prefixes x with all letters in [lo, cap] (default: no restriction; lo = 0 is the case the
//             induction uses; lo = -1, cap = 1 is the class l1)
//   L       = lookahead (default 0): for each failing x, test F(x 0 y) inside F(x 1 0 -1 y) for all legal y,
//             |y| <= L, slacks <= B + 3 (the machine window is then B + 3)
#include <bits/stdc++.h>
using namespace std;
typedef uint64_t u64; typedef unsigned __int128 st_t; const int W = 64;
int B, M;                      // enumeration bound, machine window
typedef vector<st_t> Set;
static Set step(const Set& S, int e){
    Set T;
    for (st_t s: S){
        u64 rm=(u64)(s>>W), cm=(u64)s;
        u64 fr = ~rm & (M==32 ? ~0ULL : ((1ULL<<(2*M+1))-1)) ; if (2*M+1>64) fr = ~rm;
        for (; fr; fr&=fr-1){
            int u=__builtin_ctzll(fr)-M; int v=e-u; if (v<-M||v>M) continue;
            if (cm>>(M+v)&1) continue;
            u64 r2=rm|(1ULL<<(M+u)), c2=cm|(1ULL<<(M+v));
            if (!(r2&1)||!(c2&1)) continue;
            T.push_back(((st_t)(r2>>1)<<W)|(st_t)(c2>>1));
        }
    }
    sort(T.begin(),T.end()); T.erase(unique(T.begin(),T.end()),T.end());
    return T;
}
static bool subset(const Set& a, const Set& b){ return includes(b.begin(),b.end(),a.begin(),a.end()); }
static pair<u64,u64> hsh(const Set& S, int last){
    u64 h1=1469598103934665603ULL^(u64)(last+1000), h2=0x9E3779B97F4A7C15ULL*(u64)(last+1000);
    for (st_t s: S){ u64 a=(u64)(s>>W), b=(u64)s;
        h1=(h1^a)*1099511628211ULL; h1=(h1^b)*1099511628211ULL; h1^=h1>>29;
        h2=(h2+a)*0xff51afd7ed558ccdULL; h2^=h2>>33; h2=(h2+b)*0xc4ceb9fe1a85ec53ULL; h2^=h2>>31; }
    return {h1,h2};
}
static string str(const vector<int>& w){ string s; for(int x:w) s+=" "+to_string(x); return s; }
static void show(st_t s, int k){            // print a state as absolute rows / columns after k stones
    u64 rm=(u64)(s>>W), cm=(u64)s;
    for (int t=0;t<2;t++){ u64 m=t?cm:rm; printf(t?"  cols":"      rows"); for (int p=1;p<=k+M;p++){ int off=p-k; bool used = off<=-M ? true : (m>>(M+off-1)&1); if (used) printf(" %d",p);} }
    printf("\n");
}
// frontier sets are stored as 32-bit ids of states to save memory
struct H { size_t operator()(st_t x) const { u64 a=(u64)(x>>64), b=(u64)x; a^=b*0x9E3779B97F4A7C15ULL; a^=a>>32; return a*0xff51afd7ed558ccdULL; } };
unordered_map<st_t,uint32_t,H> idof; vector<st_t> stateof;
static vector<uint32_t> pack(const Set& S){ vector<uint32_t> r; r.reserve(S.size()); for (st_t s: S){ auto it=idof.find(s); if (it==idof.end()){ it=idof.emplace(s,(uint32_t)stateof.size()).first; stateof.push_back(s);} r.push_back(it->second);} return r; }
static Set unpack(const vector<uint32_t>& r){ Set S; S.reserve(r.size()); for (uint32_t i: r) S.push_back(stateof[i]); sort(S.begin(),S.end()); return S; }
struct Sit { vector<uint32_t> P; int s, last; vector<int> w; };
int L=0;
static void look(const Set& a, const Set& b, int s, int last, vector<int>& y, long& t, long& f){   // a = F(x 0 y), b = F(x 1 0 -1 y)
    if (!y.empty()){ t++; if (!subset(a,b)){ f++; printf("      lookahead fails for y =%s\n",str(y).c_str()); } else return; }   // inclusion is inherited by longer y
    if ((int)y.size()==L) return;
    for (int e=max(last-1,-s); e<=B+3-s; e++){ y.push_back(e); look(step(a,e),step(b,e),s+e,e,y,t,f); y.pop_back(); }
}
int main(int argc, char**argv){
    B = atoi(argv[1]); int lomin = argc>2 ? atoi(argv[2]) : -1000, cap = argc>3 ? atoi(argv[3]) : 1000; if (argc>4) L=atoi(argv[4]);
    M = L ? B+3 : B; if (B < 1 || M > 31) { fprintf(stderr, "window B (B + 3 with lookahead) must be <= 31\n"); return 1; }
    u64 base = (1ULL<<M)-1;
    set<pair<u64,u64>> seen; vector<Sit> cur, nxt;
    { Set S0{((st_t)base<<W)|base}; seen.insert(hsh(S0,INT_MIN)); cur.push_back({pack(S0),0,INT_MIN,{}}); }
    long nsit=1,pt=0,pf=0,lt=0,lf=0; size_t maxset=0;
    for (int len=0; !cur.empty(); len++){
        for (auto& c: cur){
            int s=c.s, last=c.last; const Set S=unpack(c.P); vector<uint32_t>().swap(c.P);
            if ((last==INT_MIN || last<=1) && s+1<=B){
                Set a=step(S,0), b=step(step(step(S,1),0),-1); pt++;
                if (!subset(a,b)){
                    pf++; Set d; set_difference(a.begin(),a.end(),b.begin(),b.end(),back_inserter(d));
                    printf("PEAK FAILS: x =%s  (length %d, slack %d)  |F(x 0)| = %zu, |F(x 1 0 -1)| = %zu, lost %zu\n",str(c.w).c_str(),len,s,a.size(),b.size(),d.size());
                    for (size_t i=0;i<d.size()&&i<4;i++) show(d[i],len+1);
                    if (L){ vector<int> y; look(a,b,s,0,y,lt,lf); }     // after x 0: next letter >= -1; after x 1 0 -1: >= -2; use >= -1
                    fflush(stdout);
                }
            }
            int lo = last==INT_MIN ? 0 : max(last-1,-s); lo=max(lo,lomin);
            for (int e=lo; e<=min(B-s,cap); e++){
                Set T=step(S,e); if (T.empty()) continue;
                maxset=max(maxset,T.size());
                if (seen.insert(hsh(T,e)).second){ vector<int> w=c.w; w.push_back(e); nxt.push_back({pack(T),s+e,e,std::move(w)}); nsit++; }
            }
        }
        cur.swap(nxt); nxt.clear();
        fprintf(stderr,"  length %d done, next level %zu situations\n",len,cur.size());
    }
    printf("B=%d letters in [%d, %d]: situations=%ld max_set=%zu\nPEAK tested %ld fails %ld\n",B,lomin,cap,nsit,maxset,pt,pf);
    if (L) printf("lookahead <= %d: (failing x, y) pairs tested %ld, fails %ld\n",L,lt,lf);
}
