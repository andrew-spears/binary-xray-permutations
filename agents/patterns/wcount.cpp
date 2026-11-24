// Per arrangement: number of solutions of width <= w.  Prints the minimum over arrangements and the words attaining it.
#include <bits/stdc++.h>
using namespace std;
int n, w; bool inD[64], usedc[32];
long long rec(int i, array<int, 8> t) {
    if (i == n) return 1;
    long long r = 0;
    for (int c = 0; c < n; c++) if (!usedc[c] && inD[i + c]) {
        if (c < t[w]) continue;
        array<int, 8> u = t;
        for (int j = w - 1; j >= 1; j--) if (c < t[j]) u[j + 1] = max(u[j + 1], c);
        u[1] = max(u[1], c);
        usedc[c] = true; inD[i + c] = false; r += rec(i + 1, u); usedc[c] = false; inD[i + c] = true;
    }
    return r;
}
int main(int argc, char **argv) {
    n = atoi(argv[1]); w = atoi(argv[2]); vector<int> e(n); long long best = LLONG_MAX; vector<vector<int>> arg; map<long long, int> hist;
    function<void(int, int)> gen = [&](int k, int s) {
        if (k == n) { if (s) return; memset(inD, 0, sizeof inD); for (int j = 0; j < n; j++) inD[e[j] + 2 * j] = true;
            array<int, 8> t; t.fill(-1); long long c = rec(0, t); hist[c]++;
            if (c < best) { best = c; arg.clear(); } if (c == best) arg.push_back(e); return; }
        int lo = k ? e[k - 1] - 1 : 0;
        for (int x = max(lo, -s); x <= n - 1 - k; x++) { e[k] = x; gen(k + 1, s + x); }
    };
    gen(0, 0);
    printf("n=%d width<=%d: fewest solutions %lld, attained by %zu arrangements;", n, w, best, arg.size());
    int sh = 0; for (auto &kv : hist) { if (sh++ >= 6) break; printf(" [%lld sols: %d]", kv.first, kv.second); } printf("\n");
    for (size_t i = 0; i < min<size_t>(arg.size(), 6); i++) { printf("   "); for (int x : arg[i]) printf(" %d", x); printf("\n"); }
}
