// Smallest third chain.  For one word: the least t such that some solution splits into two chains plus a third chain of t stones.
// ./third e_1 ... e_n  (one word)   or   ./third n 12  (every valid word of length 12).
// Flipped convention: stone (i, c) on line i + c, chains increasing in c as i goes up.   ./third e_1 ... e_n
#include <cstdio>
#include <cstdlib>
#include <vector>
using namespace std;
int n, T; bool inD[200], usedC[70]; long long nodes, cap = 400000000LL;
int sig[70], ch[70];
bool rec(int r, int la, int lb, int lc, int cnt) {
    if (r == n) return true;
    if (++nodes > cap) return false;
    for (int c = 0; c < n; c++) {
        if (usedC[c] || !inD[r + c]) continue;
        usedC[c] = true; inD[r + c] = false; sig[r] = c;
        bool ok = false;
        if (c > la) { ch[r] = 0; ok = rec(r + 1, c, lb, lc, cnt); }
        if (!ok && c > lb && la >= 0) { ch[r] = 1; ok = rec(r + 1, la, c, lc, cnt); }
        if (!ok && c > lc && cnt < T) { ch[r] = 2; ok = rec(r + 1, la, lb, c, cnt + 1); }
        usedC[c] = false; inD[r + c] = true;
        if (ok) return true;
    }
    return false;
}
int best(const vector<int>& e) {
    for (int l = 0; l < 200; l++) inD[l] = false;
    for (int j = 0; j < n; j++) inD[e[j] + 2 * j] = true;
    for (T = 0; T <= n; T++) { nodes = 0; if (rec(0, -1, -1, -1, 0)) return T; if (nodes > cap) return -1; }
    return -2;
}
long long hist[70], byTop[70][70], byHL[2][70]; vector<int> worst; int worstT = -1;
void gen(vector<int>& e, int k, int s) {
    if (k == n) { if (s) return; int t = best(e); if (t < 0) { printf("cut off or unsolved:"); for (int x : e) printf(" %d", x); printf("\n"); return; }
        hist[t]++; { int top = 0, bot = 0, hl = 0, seenHigh = 0; for (int x : e) { if (x > top) top = x; if (-x > bot) bot = -x; if (x >= 2) seenHigh = 1; if (x <= -2 && seenHigh) hl = 1; }
          byTop[top < bot ? top : bot][t]++; byHL[hl][t]++; } if (t > worstT) { worstT = t; worst = e; } return; }
    int lo = k ? e[k - 1] - 1 : 0; if (lo < -s) lo = -s;
    for (int v = lo; v < n - k; v++) { e[k] = v; gen(e, k + 1, s + v); }
}
int main(int argc, char** argv) {
    if (argc == 3 && argv[1][0] == 'n') {     // ./third n 12 : every valid word of length 12
        n = atoi(argv[2]); if (n < 1 || n > 20) return 1; vector<int> e(n); gen(e, 0, 0);
        printf("n=%d smallest third chain: ", n); for (int t = 0; t <= n; t++) if (hist[t]) printf(" %d stones: %lld words;", t, hist[t]);
        printf("\n  by min(largest letter, -smallest letter):"); for (int m = 0; m < n; m++) { bool any = false; for (int t = 0; t <= n; t++) any |= byTop[m][t] > 0; if (!any) continue; printf("  [%d:", m); for (int t = 0; t <= n; t++) if (byTop[m][t]) printf(" %d stones x %lld", t, byTop[m][t]); printf("]"); }
        printf("\n  no high stone before a low stone:"); for (int t = 0; t <= n; t++) if (byHL[0][t]) printf(" %d stones x %lld", t, byHL[0][t]);
        printf("\n  first word needing %d:", worstT); for (int x : worst) printf(" %d", x); printf("\n"); return 0;
    }
    n = argc - 1; if (n < 1 || n > 64) { fprintf(stderr, "usage: third e_1 ... e_n (n <= 64)\n"); return 1; }
    vector<int> e(n); for (int j = 0; j < n; j++) e[j] = atoi(argv[j + 1]);
    for (int j = 0; j < n; j++) { int l = e[j] + 2 * j; if (l < 0 || l > 2 * n - 2) { fprintf(stderr, "letter off the board\n"); return 1; } inD[l] = true; }
    for (T = 0; T <= n; T++) {
        nodes = 0;
        if (rec(0, -1, -1, -1, 0)) {
            printf("n=%d smallest third chain %d (%lld nodes)\n  rows->cols:", n, T, nodes);
            for (int r = 0; r < n; r++) printf(" %d%c", sig[r], "ABC"[ch[r]]);
            printf("\n"); return 0;
        }
        if (nodes > cap) { printf("n=%d third chain %d: search cut off\n", n, T); }
    }
    printf("no solution\n"); return 0;
}
