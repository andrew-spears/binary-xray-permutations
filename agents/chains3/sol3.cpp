// All solutions of one word with at most w chains (no decreasing subsequence of length w + 1).
// Convention of agents/patterns: rows, columns 0-based, stone (i, c) on line i + c = e_j + 2j.
// Usage: ./sol3 w cap e_1 ... e_n      prints up to cap permutations (columns, 0-based), one per line.
// Needs w <= 9.
#include <bits/stdc++.h>
using namespace std;
int n, w; bool inD[128], usedc[64]; int piv[64]; long long found, cap;
void rec(int i, array<int, 10> t) {
    if (found >= cap) return;
    if (i == n) { found++; for (int r = 0; r < n; r++) printf("%d%c", piv[r], r == n - 1 ? '\n' : ' '); return; }
    for (int c = 0; c < n; c++) if (!usedc[c] && inD[i + c]) {
        if (c < t[w]) continue;
        array<int, 10> u = t;
        for (int j = w - 1; j >= 1; j--) if (c < t[j]) u[j + 1] = max(u[j + 1], c);
        u[1] = max(u[1], c);
        usedc[c] = true; inD[i + c] = false; piv[i] = c;
        rec(i + 1, u);
        usedc[c] = false; inD[i + c] = true;
    }
}
int main(int argc, char **argv) {
    w = atoi(argv[1]); cap = atoll(argv[2]); n = argc - 3;
    for (int j = 0; j < n; j++) inD[atoi(argv[j + 3]) + 2 * j] = true;
    array<int, 10> t; t.fill(-1); rec(0, t);
}
