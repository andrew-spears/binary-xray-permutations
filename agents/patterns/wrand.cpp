// Random valid arrangements of size n (scores of random tournaments with bias beta): is there a solution of width <= w?
// Complete search per arrangement up to a node cap.  Usage: ./wrand n w trials beta_x100 cap seed
#include <bits/stdc++.h>
using namespace std;
int n, w; bool inD[128], usedc[64]; long long nodes, cap;
bool rec(int i, array<int, 8> t) {
    if (i == n) return true;
    if (++nodes > cap) return false;
    for (int c = 0; c < n; c++) if (!usedc[c] && inD[i + c]) {
        if (c < t[w]) continue;
        array<int, 8> u = t;
        for (int j = w - 1; j >= 1; j--) if (c < t[j]) u[j + 1] = max(u[j + 1], c);
        u[1] = max(u[1], c);
        usedc[c] = true; inD[i + c] = false; bool ok = rec(i + 1, u); usedc[c] = false; inD[i + c] = true;
        if (ok) return true;
    }
    return false;
}
int main(int argc, char **argv) {
    n = atoi(argv[1]); w = atoi(argv[2]); int trials = atoi(argv[3]); double beta = atoi(argv[4]) / 100.0; cap = atoll(argv[5]);
    mt19937_64 rng(atoi(argv[6])); uniform_real_distribution<double> U(0, 1);
    long long none = 0, cut = 0, done = 0, worst = 0; set<vector<int>> seen;
    for (int tr = 0; tr < trials; tr++) {
        vector<int> s(n, 0);
        for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) { double p = 1 / (1 + exp(-beta * (j - i))); if (U(rng) < p) s[j]++; else s[i]++; }
        sort(s.begin(), s.end());
        if (!seen.insert(s).second) continue;
        memset(inD, 0, sizeof inD); memset(usedc, 0, sizeof usedc);
        for (int k = 0; k < n; k++) inD[s[k] + k] = true;                 // letter e_k = s_k - k, D index e_k + 2k
        nodes = 0; array<int, 8> t; t.fill(-1); bool ok = rec(0, t); done++; worst = max(worst, nodes);
        if (!ok) { if (nodes > cap) cut++; else { none++; printf("  NO width-%d solution, word:", w); for (int k = 0; k < n; k++) printf(" %d", s[k] - k); printf("\n"); } }
    }
    printf("n=%d width<=%d beta=%.2f: %lld distinct arrangements, %lld with no such solution, %lld cut off at %lld nodes (largest search %lld)\n", n, w, beta, done, none, cut, cap, worst);
}
