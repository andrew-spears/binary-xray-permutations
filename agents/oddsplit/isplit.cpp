// I-splits = RR-splits with the interleaved pairing lam = (N1, N3, ..), gam = (N2, N4, ..):
//   u_j = e_k + 2 #(S^c before k) (k in S), v_k = -e_k + 2 #(S after k) (k not in S), all >= 0, N_i = #{k not in S: v_k >= i},
//   and the i-th largest u equals N_{2i-1} + N_{2i} = sum over k not in S of clamp(v_k - 2(i-1), 0, 2).
// Usage: ./isplit n [uni] [v]    words without a tight cut.  Columns: I-split; I-split with S before the first negative letter;
// I-split with u weakly increasing.
#include <bits/stdc++.h>
using namespace std;
int n; bool uni, verbose; vector<int> e; long tot, cI, cX, cM, cIc;
int test(int S, int t) {   // bit 0: I-split, bit 1: S inside x, bit 2: u increasing
    int u[32], m = 0, a = 0, b = 0, N[70]; memset(N, 0, sizeof N); bool inc = true;
    for (int k = 0; k < n; k++) { if (S >> k & 1) { int x = e[k] + 2 * a; if (x < 0) return 0; if (m && x < u[m - 1]) inc = false; u[m++] = x; } else a++; }
    for (int k = n - 1; k >= 0; k--) { if (S >> k & 1) b++; else { int x = -e[k] + 2 * b; if (x < 0 || x > 2 * m) return 0; N[x]++; } }
    for (int i = 2 * m - 1; i >= 1; i--) N[i] += N[i + 1];
    sort(u, u + m, greater<int>());
    for (int i = 0; i < m; i++) if (u[i] != N[2 * i + 1] + N[2 * i + 2]) return 0;
    return 1 | ((S >> t) == 0 ? 2 : 0) | (inc ? 4 : 0);
}
void rec(int k, int sl, bool down) {
    if (k == n) { if (sl) return; tot++; int best = 0, t = 0; while (e[t] >= 0) t++;
        int full = (1 << n) - 1; bool co = false;
        for (int S = 1; S < full && best != 7; S++) best |= test(S, t);
        cI += best & 1; cX += (best >> 1) & 1; cM += (best >> 2) & 1;
        if (!(best & 1) && verbose) { printf("  no I-split:"); for (int x : e) printf(" %d", x); printf("\n"); }
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
    printf("n = %d, %swords without a tight cut: %ld; with an I-split: %ld; with one before the first negative letter: %ld; with one with u increasing: %ld\n",
        n, uni ? "unimodal " : "", tot, cI, cX, cM);
}
