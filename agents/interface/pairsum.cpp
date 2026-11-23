// Pair-sum problem: partition {1..2m} into pairs with prescribed distinct sums c_1 < ... < c_m.
// Necessary: sum_{i<=j} c_i >= j(2j+1) for all j, equality at j = m.
// The x-ray conjecture at size n is exactly the case m = n with all c_i odd (c_i = 2 d_i + 2n + 1):
// an odd sum forces one odd element 2r'-1 and one even element 2c, i.e. a cell (r', c).
// Usage: ./pairsum m [odd|any]   exhaustive over all majorized c; prints failures.
#include <bits/stdc++.h>
using namespace std;
int m; int c[40]; long cand=0, fail=0; bool oddonly=false;
bool solve(unsigned long long used, unsigned sums, int top){   // top = largest unused element
    while (top>0 && (used>>top&1)) top--;
    if (top==0) return true;
    for (int j=m-1;j>=0;j--){ if (sums>>j&1) continue; int y=c[j]-top; if (y>=top) continue; if (y<1) break; if (used>>y&1) continue;
        if (solve(used|1ULL<<top|1ULL<<y, sums|1u<<j, top-1)) return true; }
    return false;
}
void rec(int k,int last,int tot){
    if (k==m){ if (tot!=m*(2*m+1)) return; cand++;
        if (!solve(0,0,2*m)){ fail++; if (fail<=10){ printf("FAIL c ="); for(int i=0;i<m;i++)printf(" %d",c[i]); printf("\n"); } }
        return; }
    for (int x=last+1;x<=4*m-1;x++){
        if (oddonly && x%2==0) continue;
        int t=tot+x; if (t<(k+1)*(2*k+3)) continue;
        // remaining m-k-1 sums are > x: minimal total
        int rem=m-k-1; if (t + rem*x + rem*(rem+1)/2 > m*(2*m+1)) break;
        c[k]=x; rec(k+1,x,t);
    }
}
int main(int argc,char**argv){ m=atoi(argv[1]); oddonly = argc>2 && !strcmp(argv[2],"odd"); rec(0,2,0);
    printf("m=%d %s: majorized sum-sets=%ld failures=%ld\n",m,oddonly?"odd sums only":"all sums",cand,fail); }
