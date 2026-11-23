// Exact sets F(x) for single words, by direct propagation on the interface machine of types.cpp (no state table), slack <= 30.
// Usage: ./fw < words      one word per line (letters separated by spaces).  For every prefix x (or, with OLD=1, only the
// prefixes with no young suffix: the last j letters sum to at most j, for every j) one line
//     n slack |F| |states|  |F n Central| |Central|  young  : classes c:|F n class|/|class| ... : missing central states
// young = max over j of (sum of the last j letters) - j (0 if never positive); the missing central states (those of
// Central(slack) not in F(x)) are listed if there are at most LIST (default 40) of them.  Central = class c = slack mod 2,
// c = a + b the sum of the 2-core charges of the two diagrams (../l1sets/REPORT.md).  LAST=1: only the last prefix of each word.
// JSTAR=1 or 2 (with OLD=1): instead, for every old prefix ending in a letter 0 or 1 with slack >= S0 (default 11), one line
//     n slack tail |J*| |states| missing : the states of J*(slack, tail) that are not in F(x)
// J* as in jstar.py (JSTAR=3: conjecture OLD of REPORT3.md; JSTAR=2: D <= 2 for every tail and k|k not removed;
// JSTAR=1: no bound on D except D <= 2 for the tail 0 0, A(17) and k|k not removed).
// ZERO=1 (with JSTAR, without OLD): only the prefixes ending in a letter 0, young or old; the line also has "y young" (REPORT4.md).
#include <bits/stdc++.h>
using namespace std;
typedef uint64_t u64; typedef pair<u64,u64> St;
const int M = 32;
static int c0(u64 m){ int a=0; for (int p=0;p<64;p++){ if ((p-M)&1) continue; if (p>=M){ if (m>>p&1) a++; } else if (!(m>>p&1)) a--; } return a; }
static string diagram(u64 mask){
    vector<int> lam; int holes=0;
    for (int i=0;i<64;i++){ if (mask>>i&1) lam.push_back(holes); else holes++; }
    string s; for (int i=(int)lam.size()-1;i>=0;i--) if (lam[i]) s+= lam[i]<10 ? to_string(lam[i]) : "("+to_string(lam[i])+")";
    return s.empty()?"-":s;
}
vector<vector<u64>> parts(31);                       // Maya masks of the partitions of n
unordered_map<u64,u64> cj;                           // mask of the conjugate partition
static u64 mk(const vector<int>& cur){ u64 m=0; for (int i=0;i<M;i++){ int l= i<(int)cur.size()?cur[i]:0; m|=1ULL<<(M+l-i-1); } return m; }
static bool pairs(u64 m){ const u64 E=0x5555555555555555ULL; return ((m>>1)&E)==(m&E); }
static bool isE0(u64 Mm, u64 Bm){ if (!pairs(Mm)||!pairs(Bm)) return false; u64 B2=(Bm>>2)|3; return (B2&~Mm)==0 && __builtin_popcountll(Mm&~B2)==2; }
// J*(s, tail) of jstar.py; a, b = masks of lam, mu; tail: 0 = "1 1", 1 = ". 1", 2 = "1 0", 3 = "0 0", 4 = ". 0"
static bool jstar(u64 a, u64 b, int s, int tail, int mode){
    static u64 e=mk({}); static set<St> A17={{mk({3,3,1,1}),mk({5,2,2})},{mk({3,3,1,1,1}),mk({4,2,2})},{mk({4,2,2}),mk({3,3,1,1,1})},{mk({5,2,2}),mk({3,3,1,1})}};
    int ca=c0(a), cb=c0(b), c=ca+cb, D=abs(ca-cb); static const int dmax[5]={4,3,3,2,3}; if ((mode==2&&D>2)||(mode==3&&D>dmax[tail])) return false;
    bool sc= a==cj[b], row= (a==e&&b==mk({s}))||(b==e&&a==mk({s})), rect= s%2==0&&((a==e&&b==mk({s/2,s/2}))||(b==e&&a==mk({s/2,s/2}))), kk= s%2==0&&a==mk({s/2})&&b==mk({s/2});
    switch (tail){
        case 0: return 0<=c&&c<=1&&!sc;
        case 1: return -1<=c&&c<=2&&!sc&&!(mode>=2&&s==17&&A17.count({a,b}))&&!(mode==3&&kk);
        case 2: return -1<=c&&c<=2&&!row&&!rect&&!isE0(a,cj[b]);
        case 3: return -2<=c&&c<=3&&(mode!=1||D<=2)&&!row;
        default: return -2<=c&&c<=3&&!row;
    }
}
static void gen(int n, int mx, vector<int>& cur, int tot){
    { u64 m=mk(cur); parts[tot].push_back(m); vector<int> t; for (int j=0;j<(cur.empty()?0:cur[0]);j++){ int k=0; for (int x: cur) k+= x>j; t.push_back(k); } cj[m]=mk(t); }
    for (int a=min(mx,n);a>=1;a--){ cur.push_back(a); gen(n-a,a,cur,tot+a); cur.pop_back(); }
}
int main(){
    vector<int> cur; gen(30,30,cur,0);
    bool old=getenv("OLD"), lastonly=getenv("LAST"), zero=getenv("ZERO"); int LIST=getenv("LIST")?atoi(getenv("LIST")):40;
    int mode=getenv("JSTAR")?atoi(getenv("JSTAR")):0, S0=getenv("S0")?atoi(getenv("S0")):11; const char* tn[5]={"11",".1","10","00",".0"};
    string line;
    while (getline(cin,line)){
        vector<int> w; { istringstream is(line); int e; while (is>>e) w.push_back(e); } if (w.empty()) continue;
        printf("word %s\n", line.c_str());
        u64 base=(1ULL<<M)-1; vector<St> F={{base,base}}, G; int s=0;
        for (size_t n=1;n<=w.size();n++){
            int e=w[n-1]; G.clear();
            for (auto& t: F) for (int u=-M;u<M;u++){ int v=e-u; if (v<-M||v>=M) continue;
                if ((t.first>>(M+u)&1)||(t.second>>(M+v)&1)) continue;
                u64 r2=t.first|(1ULL<<(M+u)), c2=t.second|(1ULL<<(M+v)); if ((r2&1)&&(c2&1)) G.push_back({r2>>1,c2>>1}); }
            sort(G.begin(),G.end()); G.erase(unique(G.begin(),G.end()),G.end()); F.swap(G); s+=e;
            if (s>30){ printf("  slack above 30\n"); break; }
            if (s<0||(n>1&&e<w[n-2]-1)){ printf("  not a legal word (slack below 0, or a letter more than 1 below its predecessor)\n"); break; }
            int young=0, sum=0; for (int j=1;j<=(int)n;j++){ sum+=w[n-j]; young=max(young,sum-j); }
            if ((old&&young>0)||(lastonly&&n<w.size())) continue;
            if (mode){
                if (s<S0||e<0||e>1||(zero&&e)) continue;
                int p= n>1?w[n-2]:-1, tail= e==1 ? (p==1?0:1) : (p==1?2:p==0?3:4); long nj=0, nall=0, nmiss=0; vector<string> miss;
                for (int k=0;k<=s;k++) for (u64 a: parts[k]) for (u64 b: parts[s-k]){ nall++; if (!jstar(a,b,s,tail,mode)) continue; nj++;
                    if (!binary_search(F.begin(),F.end(),St{a,b})){ nmiss++; if ((int)miss.size()<LIST) miss.push_back(diagram(a)+"|"+diagram(b)); } }
                if (zero) printf("  %zu slack %d tail %s y %d %ld %ld missing %ld :", n, s, tn[tail], young, nj, nall, nmiss); else
                printf("  %zu slack %d tail %s %ld %ld missing %ld :", n, s, tn[tail], nj, nall, nmiss); for (auto& x: miss) printf(" %s", x.c_str()); printf("\n");
                continue;
            }
            map<int,long> inF, all; long nall=0; vector<string> miss; long nmiss=0; int cen=s&1;
            for (auto& t: F) inF[c0(t.first)+c0(t.second)]++;
            for (int k=0;k<=s;k++) for (u64 a: parts[k]){ int ca=c0(a); for (u64 b: parts[s-k]){ int c=ca+c0(b); all[c]++; nall++;
                if (c==cen&&!binary_search(F.begin(),F.end(),St{a,b})){ nmiss++; if ((int)miss.size()<=LIST) miss.push_back(diagram(a)+"|"+diagram(b)); } } }
            printf("  %zu slack %d |F| %zu of %ld  central %ld of %ld  young %d :", n, s, F.size(), nall, inF[cen], all[cen], young);
            for (auto& [c,k]: all) printf(" %d:%ld/%ld", c, inF[c], k);
            printf(" :"); if (nmiss<=LIST) for (auto& x: miss) printf(" %s", x.c_str()); else printf(" (%ld missing)", nmiss);
            printf("\n");
        }
    }
}
