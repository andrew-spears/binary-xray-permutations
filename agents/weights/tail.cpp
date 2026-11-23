// dim-weight (dim = C(s,|lam|) f^lam f^mu) and number of states of the exact sets F(1^s) = P_s - E_s, F(1^s 0) = Q_{s,1} - E0_s,
// F(1^s 0^b) = Q_{s,b} (b >= 2), via the charge c(lam) = (#odd - #even beta-numbers)/2 (even number of beads): the sets are
// P_s: c1 + c2 = [s odd];  Q_{s,b}: |D| <= b, D = c1 + c2 (s + b even), 1 - c1 - c2 (s + b odd).  E_s, E0_s are ignored
// (E_s: weight printed separately).   Usage: ./tail N
#include <bits/stdc++.h>
using namespace std; typedef long double ld;
int N; vector<map<int,ld>> G, G2, Cn; vector<ld> Ew;      // G[n][c] = sum of f^lam, Cn = number of lam, Ew[n] = sum f^lam f^lam' over lam with empty 2-core
void gen(int n,int m,vector<int>& l,int tot){
    if (n==0){ int k=l.size(), d=0; ld f=1; int q=1;
        for (int i=0;i<2*N;i++){ int b=(i<k?l[i]:0)+2*N-1-i; d+= (b%2==0)?1:-1; }   // position b+1: odd iff b even
        for (int i=0;i<k;i++) for (int j=0;j<l[i];j++){ int leg=0; for (int t=i+1;t<k;t++) if (l[t]>j) leg++; f*=(ld)q/(l[i]-j+leg); q++; }
        G[tot][d/2]+=f; Cn[tot][d/2]+=1; if (d==0) Ew[tot]+=f*f; return; }
    for (int a=min(n,m);a>=1;a--){ l.push_back(a); gen(n-a,a,l,tot); l.pop_back(); } }
int main(int argc,char** argv){ N=atoi(argv[1]); G.resize(N+1); Cn.resize(N+1); Ew.assign(N+1,0);
    for (int n=0;n<=N;n++){ vector<int> l; gen(n,n,l,n); }
    vector<vector<ld>> C(N+1,vector<ld>(N+1,0)); for (int n=0;n<=N;n++){ C[n][0]=1; for (int k=1;k<=n;k++) C[n][k]=C[n-1][k-1]+(k<n?C[n-1][k]:0); }
    printf("  s   dim-weight of: F(1^s)   F(1^s 0)   sum    F(1^s 0 0)  F(1^s 0^3)  F(1^s 0^4) | E_s    | states: P_s  Q_s,1  Q_s,2  all\n");
    for (int s=2;s<=N;s++){ map<int,ld> W, K; ld tot=0;                   // W[c1+c2] = weight
        for (int a=0;a<=s;a++) for (auto& x: G[a]) for (auto& y: G[s-a]){ W[x.first+y.first]+=C[s][a]*x.second*y.second; K[x.first+y.first]+=Cn[a][x.first]*Cn[s-a][y.first]; }
        for (auto& x: W) tot+=x.second;
        auto mass=[&](map<int,ld>& M,int b){ ld r=0; for (auto& x: M){ int D = (s+b)%2==0 ? x.first : 1-x.first; if (abs(D)<=b) r+=x.second; } return r; };
        ld e = s%4==0 ? C[s][s/2]*Ew[s/2]/tot : 0, all=0; for (auto& x: K) all+=x.second;
        printf("%3d                  %.4Lf   %.4Lf   %.4Lf   %.4Lf   %.4Lf   %.4Lf   | %.5Lf | %.0Lf %.0Lf %.0Lf %.0Lf\n", s, mass(W,0)/tot-e, mass(W,1)/tot, mass(W,0)/tot-e+mass(W,1)/tot, mass(W,2)/tot, mass(W,3)/tot, mass(W,4)/tot, e, mass(K,0), mass(K,1), mass(K,2), all); }
}
