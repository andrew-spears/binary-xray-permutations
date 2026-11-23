// Exhaustive check of the "at most M times" version at fixed n (see README.md).
// Enumerates all nondecreasing b with prefix sums >= k(k+1), total n(n+1), every value used <= M times,
// and searches for permutations rho, gamma of 1..n with rho(k) + gamma(k) = b_k.
// Usage: ./twice n M     prints counts and the first few failures.
#include <bits/stdc++.h>
using namespace std;
int n, M; int b[32]; long cand=0, fail=0, nodes=0;
bool place(int k, unsigned R, unsigned C){   // stones n-1 .. 0 (largest first)
    if (k<0) return true;
    nodes++;
    for (int r=1;r<=n;r++){ if (R>>r&1) continue; int c=b[k]-r; if (c<1||c>n||(C>>c&1)) continue;
        if (k+1<n && b[k+1]==b[k] && false) continue;
        if (place(k-1,R|1u<<r,C|1u<<c)) return true; }
    return false;
}
// memoised version on (k, R, C) to avoid blowups
unordered_set<unsigned long long> dead;
bool place2(int k, unsigned R, unsigned C){
    if (k<0) return true;
    unsigned long long key=((unsigned long long)R<<32)|C;
    if (dead.count(key)) return false;
    for (int r=1;r<=n;r++){ if (R>>r&1) continue; int c=b[k]-r; if (c<1||c>n||(C>>c&1)) continue;
        if (place2(k-1,R|1u<<r,C|1u<<c)) return true; }
    dead.insert(key); return false;
}
void rec(int k,int last,int run,int tot){
    if (k==n){ if (tot!=n*(n+1)) return; cand++; dead.clear();
        if (!place2(n-1,0,0)){ fail++; if (fail<=5 || getenv("ALLFAIL")){ printf("FAIL b ="); for(int i=0;i<n;i++)printf(" %d",b[i]); printf("\n"); } }
        return; }
    for (int x=last;x<=2*n;x++){
        int r2 = (x==last)?run+1:1; if (r2>M) continue;
        int t=tot+x; if (t<(k+1)*(k+2)) continue;
        if (t + x*(n-k-1) > n*(n+1)) break;
        b[k]=x; rec(k+1,x,r2,t);
    }
}
int main(int argc,char**argv){ n=atoi(argv[1]); M=atoi(argv[2]); rec(0,2,0,0);
    printf("n=%d M=%d candidates=%ld failures=%ld\n",n,M,cand,fail); }
