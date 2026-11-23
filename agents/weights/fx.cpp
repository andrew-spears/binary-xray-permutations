// F(x) for one prefix x by direct enumeration (relative coordinates, 128-bit masks, slack <= 60), with the weights
// dim = C(s,|lam|) f^lam f^mu, core2 dim, core2 dim^2 of F(x) (normalised) after every letter.   Usage: ./fx e1 e2 ...
#include <bits/stdc++.h>
using namespace std;
typedef unsigned __int128 u128; typedef long double ld;
const int M = 60;
struct St { u128 r, c; bool operator==(const St& o) const { return r==o.r && c==o.c; } };
struct H { size_t operator()(const St& t) const { uint64_t a=(uint64_t)t.r*0x9E3779B97F4A7C15ULL ^ (uint64_t)(t.r>>64)*0xC2B2AE3D27D4EB4FULL ^ (uint64_t)t.c*0x165667B19E3779F9ULL ^ (uint64_t)(t.c>>64)*0xff51afd7ed558ccdULL; a^=a>>29; return a*0xBF58476D1CE4E5B9ULL; } };
static vector<int> part(u128 m){ vector<int> l; int z=0; vector<int> zs; for (int i=0;i<=2*M;i++){ if (m>>i&1) zs.push_back(z); else z++; }
    for (int i=zs.size()-1;i>=0;i--) if (zs[i]) l.push_back(zs[i]); return l; }
static ld flam(const vector<int>& l){ int n=0; for (int a: l) n+=a; ld f=1; int k=1;
    for (size_t i=0;i<l.size();i++) for (int j=0;j<l[i];j++){ int leg=0; for (size_t t=i+1;t<l.size();t++) if (l[t]>j) leg++; f*= (ld)k/(l[i]-j-1+leg+1); k++; } (void)n; return f; }
static int core(const vector<int>& l){ // 0 empty, 1 single box, 2 larger: beta-numbers with 2M beads
    int d=0; for (int i=0;i<2*M;i++){ int b=(i<(int)l.size()?l[i]:0)+2*M-1-i; d+= b%2?1:-1; } return d==0?0: d==-2?1:2; }  // top bead 2M-1 odd -> even
static map<vector<int>,pair<ld,int>> memo;
static pair<ld,int> info(const vector<int>& l){ auto it=memo.find(l); if (it!=memo.end()) return it->second; return memo[l]={flam(l),core(l)}; }
static void gen(int n,int m,vector<int>& l,vector<array<ld,6>>& S,int tot){ // S[size][core*2+p]
    if (n==0){ auto x=info(l); if (x.second<2){ S[tot][x.second*2]+=x.first; S[tot][x.second*2+1]+=x.first*x.first; } S[tot][4]+=x.first; return; }
    for (int a=min(n,m);a>=1;a--){ l.push_back(a); gen(n-a,a,l,S,tot); l.pop_back(); } }
int main(int argc,char** argv){
    bool dumpF = argc>1 && !strcmp(argv[1],"-d");   // ./fx -d e1 e2 ... : print the states of F(x) as lam|mu, nothing else
    vector<int> w; for (int i=1+dumpF;i<argc;i++) w.push_back(atoi(argv[i]));
    int smax=0,s=0; for (int e: w){ s+=e; smax=max(smax,s); }
    vector<array<ld,6>> S(smax+1); for (auto& a: S) a.fill(0);
    for (int n=0;n<=smax;n++){ vector<int> l; gen(n,n,l,S,n); }
    vector<vector<ld>> C(smax+1,vector<ld>(smax+1,0)); for (int n=0;n<=smax;n++){ C[n][0]=1; for (int k=1;k<=n;k++) C[n][k]=C[n-1][k-1]+(k<n?C[n-1][k]:0); }
    u128 base=((u128)1<<M)-1; unordered_set<St,H> cur; cur.insert({base,base}); s=0;
    for (size_t i=0;i<w.size();i++){ int e=w[i]; unordered_set<St,H> nx; nx.reserve(cur.size()*2);
        for (const St& t: cur) for (int u=-M;u<=M;u++){ int v=e-u; if (v<-M||v>M) continue;
            if ((t.r>>(M+u)&1)||(t.c>>(M+v)&1)) continue; u128 r2=t.r|((u128)1<<(M+u)), c2=t.c|((u128)1<<(M+v));
            if ((r2&1)&&(c2&1)) nx.insert({r2>>1,c2>>1}); }
        cur.swap(nx); s+=e;
        if (dumpF){ if (i+1==w.size()) for (const St& t: cur){ auto l=part(t.r), m=part(t.c);
            for (size_t q=0;q<l.size();q++) printf("%s%d", q?",":"", l[q]); if (l.empty()) printf("-"); printf("|");
            for (size_t q=0;q<m.size();q++) printf("%s%d", q?",":"", m[q]); if (m.empty()) printf("-"); printf("\n"); } continue; }
        ld tot[3]={0,0,0}, got[3]={0,0,0};
        for (int a=0;a<=s;a++){ ld c=C[s][a]; tot[0]+=c*S[a][4]*S[s-a][4];
            if (s%2==0){ tot[1]+=c*S[a][0]*S[s-a][0]; tot[2]+=c*c*S[a][1]*S[s-a][1]; }
            else { tot[1]+=c*(S[a][0]*S[s-a][2]+S[a][2]*S[s-a][0]); tot[2]+=c*c*(S[a][1]*S[s-a][3]+S[a][3]*S[s-a][1]); } }
        for (const St& t: cur){ auto l=part(t.r), m=part(t.c); auto x=info(l), y=info(m); int a=0; for (int q: l) a+=q;
            ld d=C[s][a]*x.first*y.first; got[0]+=d; bool ok = s%2==0 ? (x.second==0&&y.second==0) : (x.second+y.second==1);
            if (ok){ got[1]+=d; got[2]+=d*d; } }
        printf("after letter %2zu (%2d): slack %2d  |F| = %9zu   dim %.4Lf   core2 dim %.4Lf   core2 dim^2 %.4Lf\n", i+1, e, s, cur.size(), got[0]/tot[0], got[1]/tot[1], got[2]/tot[2]); fflush(stdout);
    }
}
