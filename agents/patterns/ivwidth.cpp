// Interval orders of bounded width.  Intervals 1..n by right endpoint; interval t lies above the first k_t earlier ones
// (0 <= k_t <= t-1) and its value is  d_t = k_t - #{t' > t : k_t' >= t}.  Width = max_j #{t : k_t <= j < t}.
// For every valid arrangement D of size n: is D the set of values of an interval order of width <= w?
// Usage: ./ivwidth n w
#include <bits/stdc++.h>
using namespace std;
int n, w; bool inD[64]; int kk[32], cnt[32], ge[32];
bool rec(int t) {                       // choose k_t for t = n, n-1, ..., 1;  ge[t] = #{t' > t : k_t' >= t}
    if (t == 0) return true;
    for (int k = 0; k <= t - 1; k++) {
        int d = k - ge[t] + (n - 1);
        if (d < 0 || !inD[d]) continue;
        bool ok = true; for (int j = k; j < t; j++) if (cnt[j] + 1 > w) { ok = false; break; }
        if (!ok) continue;
        for (int j = k; j < t; j++) cnt[j]++;
        for (int s = 1; s <= k; s++) ge[s]++;
        inD[d] = false; bool r = rec(t - 1); inD[d] = true;
        for (int j = k; j < t; j++) cnt[j]--;
        for (int s = 1; s <= k; s++) ge[s]--;
        if (r) return true;
    }
    return false;
}
int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: ivwidth n w   (1 <= n <= 31, w >= 1)\n"); return 1; }
    n = atoi(argv[1]); w = atoi(argv[2]);
    if (n < 1 || n > 31 || w < 1) { fprintf(stderr, "usage: ivwidth n w   (1 <= n <= 31, w >= 1)\n"); return 1; }
    long long tot = 0, bad = 0; vector<int> e(n);
    function<void(int, int)> gen = [&](int k, int s) {
        if (k == n) { if (s) return; tot++; memset(inD, 0, sizeof inD); memset(cnt, 0, sizeof cnt); memset(ge, 0, sizeof ge);
            for (int j = 0; j < n; j++) inD[e[j] + 2 * j] = true;          // d + n - 1
            if (!rec(n)) { bad++; if (bad <= 3) { printf("  no interval order of width %d:", w); for (int x : e) printf(" %d", x); printf("\n"); } }
            return; }
        int lo = k ? e[k - 1] - 1 : 0;
        for (int x = max(lo, -s); x <= n - 1 - k; x++) { e[k] = x; gen(k + 1, s + x); }
    };
    gen(0, 0);
    printf("n=%d interval orders of width<=%d: %lld arrangements, %lld not realised\n", n, w, tot, bad);
}
