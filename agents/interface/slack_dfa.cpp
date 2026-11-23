// Bounded-slack automaton, fast version of slack_dfa.py (same model; see README.md).
// Determinizes the interface automaton over all valid no-tight-cut words with max slack <= B.
// Usage: ./slack_dfa B     Output: #DFA states, largest reachable set, verdict.
#include <bits/stdc++.h>
using namespace std;
typedef uint64_t u64;
int B;
struct Key { int e, sig; vector<u64> S; bool operator<(const Key&o) const { if (e!=o.e) return e<o.e; if (sig!=o.sig) return sig<o.sig; return S<o.S; } };
int main(int argc, char**argv){
    B = atoi(argv[1]);
    u64 base = (1ULL<<B)-1;
    map<Key,int> seen; vector<Key> q; vector<pair<int,int>> par;
    Key st{INT_MIN,0,{(base<<32)|base}}; seen[st]=0; q.push_back(st); par.push_back({-1,0});
    size_t maxset=0; long bad=-1; int bade=0;
    for (size_t i=0;i<q.size() && bad<0;i++){
        Key cur=q[i];
        int lo = cur.e==INT_MIN ? 0 : cur.e-1;
        for (int e=max(lo,-cur.sig); e<=B-cur.sig; e++){
            int sig2=cur.sig+e; if (sig2==0 && cur.sig==0) continue;
            vector<u64> T;
            for (u64 s: cur.S){
                u64 rm=s>>32, cm=s&0xffffffffULL;
                for (int u=-B;u<=B;u++){
                    int v=e-u; if (v<-B||v>B) continue;
                    if (rm>>(B+u)&1) continue; if (cm>>(B+v)&1) continue;
                    u64 r2=rm|(1ULL<<(B+u)), c2=cm|(1ULL<<(B+v));
                    if (!(r2&1)||!(c2&1)) continue;
                    T.push_back(((r2>>1)<<32)|(c2>>1));
                }
            }
            sort(T.begin(),T.end()); T.erase(unique(T.begin(),T.end()),T.end());
            if (sig2==0){ if (T.empty()){bad=i;bade=e;break;} continue; }
            if (T.empty()){ if (sig2 + (long)max(e,0)*max(e-1,0)/2 <= B){bad=i;bade=e;break;} continue; }
            Key nx{e,sig2,T};
            if (!seen.count(nx)){ seen[nx]=q.size(); q.push_back(nx); par.push_back({(int)i,e}); maxset=max(maxset,T.size()); }
        }
    }
    printf("B=%d dfa_states=%zu max_set=%zu %s\n",B,q.size(),maxset,bad<0?"ALL ACCEPTED":"REJECTED");
    if (bad>=0){ vector<int> w; w.push_back(bade); for (long i=bad;i>0;i=par[i].first) w.push_back(par[i].second); reverse(w.begin(),w.end()); printf("rejected word:"); for(int x:w) printf(" %d",x); printf("\n"); }
    // per-level summary: number of distinct sets and min/max size
    map<int,array<size_t,3>> lev;
    for (auto&k:q){ auto&a=lev[k.sig]; if(!a[0]){a[1]=k.S.size();} a[0]++; a[1]=min(a[1],k.S.size()); a[2]=max(a[2],k.S.size()); }
    for (auto&kv:lev) printf("  sigma=%d: dfa states %zu, set sizes %zu..%zu\n",kv.first,kv.second[0],kv.second[1],kv.second[2]);
}
