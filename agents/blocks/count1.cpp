// Number of solutions of one word with at most w chains, for w = 2, 3, 4 and for every w.   ./count1 e_1 ... e_n
// Flipped convention: stone (i, c) on line i + c; at most w chains = no decreasing run of w + 1 columns.
#include <cstdio>
#include <cstdlib>
#include <vector>
using namespace std;
int n, W; bool inD[200], usedC[70];
// t[j] = largest possible last column of a decreasing run of length j so far (-1 if none)
long long rec(int r, vector<int>& t) {
    if (r == n) return 1;
    long long tot = 0;
    for (int c = 0; c < n; c++) {
        if (usedC[c] || !inD[r + c]) continue;
        if (W < n && t[W] > c) continue;
        vector<int> u = t;
        for (int j = (W < n ? W : n) - 1; j >= 1; j--) if (t[j] > c && c > u[j + 1]) u[j + 1] = c;
        if (c > u[1]) u[1] = c;
        usedC[c] = true; inD[r + c] = false; tot += rec(r + 1, u); usedC[c] = false; inD[r + c] = true;
    }
    return tot;
}
int main(int argc, char** argv) {
    n = argc - 1; if (n < 1 || n > 20) { fprintf(stderr, "usage: count1 e_1 ... e_n (n <= 20)\n"); return 1; }
    for (int j = 0; j < n; j++) { int l = atoi(argv[j + 1]) + 2 * j; if (l < 0 || l > 2 * n - 2) { fprintf(stderr, "letter off the board\n"); return 1; } inD[l] = true; }
    printf("n=%d solutions with at most w chains:", n);
    for (int w : {2, 3, 4, n}) { W = w < n ? w : n; vector<int> t(n + 2, -1); printf("  w=%d: %lld", W, rec(0, t)); }
    printf("\n"); return 0;
}
