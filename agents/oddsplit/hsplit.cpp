// H-splits.  For a set S of stones: S-word w_j = e_k + 2 #(S^c before k), S^c-word (read backwards) -e_k + 2 #(S after k).
// S is an H-split if both words are >= 0 and the positive letters of the S-word, sorted, are the conjugate partition of
// the positive letters of the S^c-word.  Then (Lemma R of REPORT.md) the number of ways to place the stones of S in the
// first |S| columns and rows {j + u_j} (u = letters sorted increasingly) is odd, and likewise for S^c in the other rows.
// Usage: ./hsplit n [uni] [v]    all valid words without a tight cut (uni: only unimodal ones); v lists words without an H-split
#include <bits/stdc++.h>
using namespace std;
int n; bool uni, verbose; long tot = 0, good = 0, goodpre = 0; vector<int> e;
bool hs(int S) {
    static int w1[64], w2[64], cnt[130]; int m = 0, a = 0, q = 0, b = 0;
    for (int k = 0; k < n; k++) { if (S >> k & 1) { int x = e[k] + 2 * a; if (x < 0) return false; if (x) w1[m++] = x; } else a++; }
    for (int k = n - 1; k >= 0; k--) { if (S >> k & 1) b++; else { int x = -e[k] + 2 * b; if (x < 0) return false; if (x) w2[q++] = x; } }
    // conj(w1) == w2 as multisets: #{w1 >= i} for i = 1.. must be w2 sorted decreasingly
    sort(w1, w1 + m, greater<int>()); sort(w2, w2 + q, greater<int>());
    if (m == 0) return q == 0; if (w1[0] != q) return false;
    for (int i = 1; i <= q; i++) { int c = 0; while (c < m && w1[c] >= i) c++; if (w2[i - 1] != c) return false; }
    return true;
}
void rec(int k, int sl, bool down) {
    if (k == n) { if (sl) return; tot++; bool ok = false;
        int p = 0; while (p < n && e[p] >= 0) p++;   // S inside the nonnegative prefix first
        for (int S = 1; S < (1 << p) && !ok; S++) ok = hs(S);
        if (ok) goodpre++;
        for (int S = 1; S < (1 << n) - 1 && !ok; S++) ok = hs(S);
        good += ok; if (!ok && verbose) { printf("  no H-split:"); for (int x : e) printf(" %d", x); printf("\n"); }
        return; }
    int lo = k ? e[k - 1] - 1 : 1;
    for (int x = max(lo, -sl); x <= n; x++) {
        int s2 = sl + x; if (k < n - 1 && s2 <= 0) continue; if (uni && down && x > 0) continue;
        if (s2 > (n - 1 - k) * (n - k) / 2 - (n - 1 - k) * x) break;
        e[k] = x; rec(k + 1, s2, down || x < 0); }
}
int main(int argc, char** argv) {
    n = atoi(argv[1]); for (int i = 2; i < argc; i++) { if (!strcmp(argv[i], "uni")) uni = true; if (!strcmp(argv[i], "v")) verbose = true; }
    e.resize(n); rec(0, 0, false);
    printf("n = %d, %s words without a tight cut: %ld; with an H-split: %ld; with one inside the letters before the first negative one: %ld\n", n, uni ? "unimodal" : "all valid", tot, good, goodpre);
}
