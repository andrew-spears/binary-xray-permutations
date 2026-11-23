// Fast version of invariant.py: greatest inductive family I(sigma, last L letters) inside slack <= B.
// Usage: ./invariant B L     prints SUFFICES / FAILS and the sizes of the smallest I.
#include <bits/stdc++.h>
using namespace std;
typedef uint64_t u64; typedef vector<u64> Set;
int B, L;
Set step(const Set&S,int e){ Set T; for(u64 s:S){u64 rm=s>>32,cm=s&0xffffffffULL; for(int u=-B;u<=B;u++){int v=e-u; if(v<-B||v>B)continue; if(rm>>(B+u)&1)continue; if(cm>>(B+v)&1)continue; u64 r2=rm|(1ULL<<(B+u)),c2=cm|(1ULL<<(B+v)); if(!(r2&1)||!(c2&1))continue; T.push_back(((r2>>1)<<32)|(c2>>1));}} sort(T.begin(),T.end()); T.erase(unique(T.begin(),T.end()),T.end()); return T; }
int excess(u64 m){ vector<int> xs; for(int j=2*B-1;j>=0;j--) if(m>>j&1) xs.push_back(j-B+1); int s=0; for(size_t i=0;i<xs.size();i++) s+=xs[i]+(int)i; return s; }
int main(int argc,char**argv){ B=atoi(argv[1]); L=atoi(argv[2]);
    typedef pair<int,vector<int>> Sum; map<Sum,int> id; vector<Sum> nodes; vector<vector<pair<int,int>>> out, pre;
    auto get=[&](const Sum&s){ auto it=id.find(s); if(it!=id.end()) return it->second; id[s]=nodes.size(); nodes.push_back(s); out.emplace_back(); pre.emplace_back(); return (int)nodes.size()-1; };
    get({0,{}});
    for(size_t i=0;i<nodes.size();i++){ Sum s=nodes[i]; int sig=s.first; bool first=(i==0); int last=first?0:s.second.back(); // history always stores >=1 letter
        int lo=first?0:last-1;
        for(int e=max(lo,-sig);e<=B-sig;e++){ int s2=sig+e; if(s2==0){ if(sig==0)continue; out[i].push_back({e,-1}); continue; }
            if(s2+(long)max(e,0)*max(e-1,0)/2>B) continue;
            vector<int> h=s.second; h.push_back(e); int keep=max(L,1); if((int)h.size()>keep) h.erase(h.begin(),h.end()-keep);
            int t=get({s2,h}); out[i].push_back({e,t}); pre[t].push_back({(int)i,e}); } }
    // all states by excess
    vector<vector<u64>> masks(B+1); for(u64 m=0;m<(1ULL<<(2*B));m++){ if(__builtin_popcountll(m)!=B)continue; int ex=excess(m); if(ex<=B) masks[ex].push_back(m); }
    vector<Set> all(B+1); for(int sg=0;sg<=B;sg++){ for(int a=0;a<=sg;a++) for(u64 r:masks[a]) for(u64 c:masks[sg-a]) all[sg].push_back((r<<32)|c); sort(all[sg].begin(),all[sg].end()); }
    vector<Set> I(nodes.size()); for(size_t i=0;i<nodes.size();i++) I[i]=all[nodes[i].first];
    bool ch=true; int rounds=0; while(ch){ ch=false; rounds++; for(size_t t=1;t<nodes.size();t++){ Set cur=I[t]; for(auto&pe:pre[t]){ Set st=step(I[pe.first],pe.second); Set tmp; set_intersection(cur.begin(),cur.end(),st.begin(),st.end(),back_inserter(tmp)); cur.swap(tmp);} if(cur.size()!=I[t].size()){ I[t]=cur; ch=true; } } }
    long fails=0; int ex=-1; for(size_t i=0;i<nodes.size();i++){ if(i&&I[i].empty()){fails++; if(ex<0)ex=i;} for(auto&o:out[i]) if(o.second<0 && step(I[i],o.first).empty()){fails++; if(ex<0)ex=i;} }
    printf("B=%d L=%d: %zu summaries, %d rounds; invariant %s",B,L,nodes.size(),rounds,fails?"FAILS":"SUFFICES");
    if(fails){ printf(" (%ld places, e.g. sigma=%d last letters",fails,nodes[ex].first); for(int x:nodes[ex].second)printf(" %d",x); printf(")"); }
    size_t mn=SIZE_MAX; double fr=1; for(size_t i=1;i<nodes.size();i++){ mn=min(mn,I[i].size()); fr=min(fr,(double)I[i].size()/all[nodes[i].first].size()); }
    printf("; smallest I has %zu states, smallest fraction of all states %.3f\n",mn,fr);
}
