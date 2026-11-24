// One word: smallest width of a solution (complete search, node cap).  Usage: ./width1 cap e_1 ... e_n
#include <bits/stdc++.h>
using namespace std;
int n, w; bool inD[128], usedc[64]; int piv[64]; long long nodes, cap;
bool rec(int i, array<int, 10> t) {
    if (i == n) return true;
    if (++nodes > cap) return false;
    for (int c = 0; c < n; c++) if (!usedc[c] && inD[i + c]) {
        if (c < t[w]) continue;
        array<int, 10> u = t;
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
    if (argc < 3 || argc - 2 > 64) { fprintf(stderr, "usage: width1 cap e_1 ... e_n   (1 <= n <= 64, the letters of a valid word)\n"); return 1; }
    cap = atoll(argv[1]); n = argc - 2; vector<int> e(n); for (int j = 0; j < n; j++) e[j] = atoi(argv[j + 2]);
    for (int j = 0; j < n; j++) if (e[j] + 2 * j < 0 || e[j] + 2 * j > 2 * n - 2) { fprintf(stderr, "letter %d puts a stone off the board\n", j + 1); return 1; }
    for (w = 1; w <= 8; w++) {
        memset(inD, 0, sizeof inD); memset(usedc, 0, sizeof usedc); for (int j = 0; j < n; j++) inD[e[j] + 2 * j] = true;
        nodes = 0; array<int, 10> t; t.fill(-1);
        bool ok = rec(0, t);
        printf("  width<=%d: %s (%lld nodes)\n", w, ok ? "solution" : nodes > cap ? "search cut off" : "none", nodes);
        if (ok) { printf("  pi ="); for (int i = 0; i < n; i++) printf(" %d", piv[i] + 1); printf("\n"); break; }
    }
}
