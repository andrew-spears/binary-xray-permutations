// For every valid arrangement D of size n: is there a solution whose order has width <= w,
// i.e. a permutation pi with {i + pi(i)} = D + n + 1 and no decreasing subsequence of length w + 1?
// Usage: ./width n w [print]      (complete search per D)
#include <bits/stdc++.h>
using namespace std;
int n, w; bool inD[64], usedc[32]; int piv[32]; long long nodes;
bool rec(int i, array<int, 8> t) {            // t[j] = largest last value over decreasing j-subsequences so far
    if (i == n) return true;
    nodes++;
    for (int c = 0; c < n; c++) if (!usedc[c] && inD[i + c]) {
        if (c < t[w]) continue;
        array<int, 8> u = t;
        for (int j = w - 1; j >= 1; j--) if (c < t[j]) u[j + 1] = max(u[j + 1], c);
        u[1] = max(u[1], c);
        usedc[c] = true; inD[i + c] = false; piv[i] = c;
        bool ok = rec(i + 1, u);
        usedc[c] = false; inD[i + c] = true;
        if (ok) return true;
    }
    return false;
}
int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: width n w [print]   (1 <= n <= 31, 1 <= w <= 7)\n"); return 1; }
    n = atoi(argv[1]); w = atoi(argv[2]);
    if (n < 1 || n > 31 || w < 1 || w > 7) { fprintf(stderr, "usage: width n w [print]   (1 <= n <= 31, 1 <= w <= 7)\n"); return 1; }
    bool pr = argc > 3;
    long long tot = 0, bad = 0, worst = 0; vector<int> e(n);
    // words: letters e_k = s_k - (k-1), nondecreasing scores => e_k >= e_{k-1} - 1, partial sums >= 0, total 0
    function<void(int, int)> gen = [&](int k, int s) {
        if (k == n) {
            if (s) return;
            tot++; memset(inD, 0, sizeof inD);
            for (int j = 0; j < n; j++) inD[e[j] + 2 * j] = true;        // i + c with 0-based rows and columns: d + n - 1
            nodes = 0; array<int, 8> t; t.fill(-1);
            if (!rec(0, t)) { bad++; if (pr || bad <= 3) { printf("  no width-%d solution:", w); for (int x : e) printf(" %d", x); printf("\n"); } }
            worst = max(worst, nodes); return;
        }
        int lo = k ? e[k - 1] - 1 : 0;
        for (int x = max(lo, -s); x <= n - 1 - k; x++) { e[k] = x; gen(k + 1, s + x); }
    };
    gen(0, 0);
    printf("n=%d width<=%d: %lld arrangements, %lld without such a solution (largest search %lld nodes)\n", n, w, tot, bad, worst);
}
