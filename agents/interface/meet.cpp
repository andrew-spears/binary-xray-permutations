// Fast version of meet.py, middle cut only (k = n/2).
// F = pairs (rows, cols) reachable by the k smallest diagonals, G = by the n-k largest (complemented),
// N = all pairs of k-subsets of [n] with total excess sigma_k.  Reports worst (|F|+|G|)/N and worst |F|/N
// over all valid no-tight-cut D of size n.     Usage: ./meet n   (all D)   or   ./meet n e_1 ... e_n   (one word)
#include <bits/stdc++.h>
using namespace std;
int n; vector<int> e; long cntD=0; double worst=9, worstF=9; vector<int> wD, wFD; long below=0;
vector<vector<long>> pbox; // pbox[k][j]: partitions of j in k x (n-k) box
size_t level(const vector<int>&w,int steps){
    vector<uint32_t> cur{0}, nxt; static vector<uint8_t> seen; seen.assign(1u<<(2*n),0);
    for(int k=0;k<steps;k++){ nxt.clear(); int b=2*(k+1)+w[k];
        for(uint32_t s:cur){ uint32_t R=s>>n, C=s&((1u<<n)-1);
            for(int r=1;r<=n;r++){ if(R>>(r-1)&1)continue; int c=b-r; if(c<1||c>n||(C>>(c-1)&1))continue;
                uint32_t t=((R|1u<<(r-1))<<n)|(C|1u<<(c-1)); if(!seen[t]){seen[t]=1;nxt.push_back(t);} } }
        for(uint32_t t:nxt) seen[t]=0; cur.swap(nxt); }
    return cur.size(); }
void done(){ cntD++; int k=n/2; int sig=0; for(int i=0;i<k;i++) sig+=e[i];
    vector<int> em(n); for(int i=0;i<n;i++) em[i]=-e[n-1-i];
    size_t f=level(e,k), g=level(em,n-k); long N=0; for(int a=0;a<=sig;a++) N+=pbox[k][a]*pbox[k][sig-a];
    double v=(double)(f+g)/N, d=(double)min(f,g)/N; if(v<=1) below++;
    if(v<worst){worst=v;wD=e;} if(d<worstF){worstF=d;wFD=e;} }
void rec(int k,int last,int sig){ if(k==n){ if(sig==0) done(); return; }
    for(int x=max(k?last-1:0,-sig);;x++){ int s2=sig+x; if(s2==0&&k+1<n) continue; if(s2<0) continue;
        // remaining letters can drop the slack by at most ... prune: need to return to 0 within n-k-1 letters
        long rem=n-k-1; if(s2>0&&rem==0) break; // minimal future sum: letters x-1, x-2, ... 
        long minfut=0; for(long j=1;j<=rem;j++) minfut+=x-j; if(s2+minfut>0) break;
        e[k]=x; rec(k+1,x,s2); } }
int main(int argc,char**argv){ n=atoi(argv[1]); if (n < 2 || n > 15) { fprintf(stderr, "n must be 2..15: a state packs two n-bit masks into 32 bits\n"); return 1; } e.assign(n,0);
    pbox.assign(n+1,{}); int S=n*n; for(int k=0;k<=n;k++){ // partitions with <=k parts, each <= n-k
        vector<vector<long>> dp(k+1, vector<long>(S+1,0)); // gaussian binomial coefficients via dp over parts
        // count subsets: k-subsets of [n] by excess
        vector<vector<long>> c(k+1, vector<long>(S+1,0)); c[0][0]=1;
        for(int x=1;x<=n;x++) for(int j=min(k,x);j>=1;j--) for(int s=S;s>=x;s--) c[j][s]+=c[j-1][s-x];
        pbox[k].assign(S+1,0); for(int s=k*(k+1)/2;s<=S;s++) pbox[k][s-k*(k+1)/2]=c[k][s]; }
    if(argc>2){ for(int i=0;i<n;i++) e[i]=atoi(argv[2+i]); done(); } else rec(0,0,0);
    printf("n=%d: %ld no-tight-cut D; middle cut (|F|+|G|)/N worst %.4f (<=1 for %ld) at e=",n,cntD,worst,below); for(int x:wD)printf("%d ",x);
    printf("; min(|F|,|G|)/N worst %.4f at e=",worstF); for(int x:wFD)printf("%d ",x); printf("\n"); }
