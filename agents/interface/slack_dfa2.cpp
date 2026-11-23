// Bounded-slack automaton with repeated diagonals allowed (see README.md, "twice" section).
// Words: b nondecreasing with every value used at most M times  <=>  e_{k+1} >= e_k - 2, and a run of
// equal b's (letters dropping by exactly 2) has length <= M.   M = 1 is the original conjecture.
// Usage: ./slack_dfa2 B M
#include <bits/stdc++.h>
using namespace std;
typedef uint64_t u64;
int B, M;
struct Key { int e, run, sig; vector<u64> S; bool operator<(const Key&o) const { return tie(e,run,sig,S)<tie(o.e,o.run,o.sig,o.S);} };
// can[(e,run,sig)]: the word can be completed to slack 0 without exceeding B
map<array<int,3>,bool> can;
vector<array<int,2>> letters(int e,int run,int sig,bool first){ // (e2, run2)
    vector<array<int,2>> out;
    int lo = first?0:(run<M? e-2 : e-1);
    for (int e2=max(lo,-sig); e2<=B-sig; e2++){ if (sig==0 && e2==0) continue; out.push_back({e2,(!first && e2==e-2)?run+1:1}); }
    return out;
}
int main(int argc,char**argv){
    B=atoi(argv[1]); M=atoi(argv[2]); if (B < 1 || B > 16) { fprintf(stderr, "B must be 1..16: a state packs two 2B-bit masks into 64 bits\n"); return 1; }
    // completability: backward fixpoint
    vector<array<int,3>> dom; for(int e=-B;e<=B;e++)for(int r=1;r<=M;r++)for(int s=1;s<=B;s++){dom.push_back({e,r,s});can[{e,r,s}]=false;}
    bool ch=true; while(ch){ch=false; for(auto&d:dom){ if(can[d])continue; for(auto&l:letters(d[0],d[1],d[2],false)){int s2=d[2]+l[0]; if(s2==0||can[{l[0],l[1],s2}]){can[d]=true;ch=true;break;}}}}
    u64 base=(1ULL<<B)-1;
    map<Key,int> seen; vector<Key> q; vector<pair<int,int>> par;
    Key st{0,1,0,{(base<<32)|base}}; seen[st]=0; q.push_back(st); par.push_back({-1,0});
    size_t maxset=0; long bad=-1; int bade=0;
    for(size_t i=0;i<q.size()&&bad<0;i++){
        Key cur=q[i];
        for(auto&l:letters(cur.e,cur.run,cur.sig,i==0)){
            int e=l[0], sig2=cur.sig+e;
            if(sig2!=0 && !can[{e,l[1],sig2}]) continue;
            vector<u64> T;
            for(u64 s:cur.S){ u64 rm=s>>32, cm=s&0xffffffffULL;
                for(int u=-B;u<=B;u++){ int v=e-u; if(v<-B||v>B)continue; if(rm>>(B+u)&1)continue; if(cm>>(B+v)&1)continue;
                    u64 r2=rm|(1ULL<<(B+u)), c2=cm|(1ULL<<(B+v)); if(!(r2&1)||!(c2&1))continue; T.push_back(((r2>>1)<<32)|(c2>>1)); } }
            sort(T.begin(),T.end()); T.erase(unique(T.begin(),T.end()),T.end());
            if(T.empty()){bad=i;bade=e;break;}
            if(sig2==0) continue;
            Key nx{e,l[1],sig2,T};
            if(!seen.count(nx)){seen[nx]=q.size();q.push_back(nx);par.push_back({(int)i,e});maxset=max(maxset,T.size());}
        }
    }
    printf("B=%d M=%d dfa_states=%zu max_set=%zu %s\n",B,M,q.size(),maxset,bad<0?"ALL ACCEPTED":"REJECTED");
    if(bad>=0){ vector<int> w; w.push_back(bade); for(long i=bad;i>0;i=par[i].first) w.push_back(par[i].second); reverse(w.begin(),w.end());
        printf("rejected prefix e ="); for(int x:w)printf(" %d",x); printf("\n   b ="); for(size_t k=0;k<w.size();k++)printf(" %d",(int)(2*(k+1)+w[k])); printf("  (prefix; completable inside the bound)\n"); }
}
