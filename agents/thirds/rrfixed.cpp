// RR-splits (Lemma R of ../oddsplit/REPORT.md) with a FIXED set of rows.  R = rows r (1-based) with pattern[(r-1) mod len] == '1',
// m = |R|, lam_j = r_j - j (so R = rows 1 mod 3 gives lam = (2m-2, ..., 4, 2, 0)).  For a set S of m stones:
//   u = S-word (e_k + 2 #(S^c before k)),  v = S^c-word read backwards (-e_k + 2 #(S after k)), both >= 0.
// RR with rows R: rho(u) = lam + gam and rho(v) = lam' + gam' for a partition gam (then S on the rows R and the columns
// c_j = gam_j + j is an odd split, both parities exactly 1).
// Also counted: "odd term" = any S of size m and any gam with rho(u) = lam + gam (one side extreme only).
// Usage: ./rrfixed n pattern [all] [v] [p]     default: words without a tight cut; all: every valid word;
// p: print every RR-split as  RR letters | stones of S | columns of S   (checked by brute force in check_rr.py)
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> P;
int n, m; bool verbose, allw, dump; vector<int> e; P lam, lamc; long tot = 0, good = 0, nsum = 0;
P conj(const P& p, int len) { P c(len, 0); for (int i = 0; i < len; i++) for (int x : p) if (x > i) c[i]++; return c; }
bool test(uint32_t S) {
    P w1, w2; int a = 0, b = 0;
    for (int k = 0; k < n; k++) { if (S >> k & 1) { int x = e[k] + 2 * a; if (x < 0) return false; w1.push_back(x); } else a++; }
    for (int k = n - 1; k >= 0; k--) { if (S >> k & 1) b++; else { int x = -e[k] + 2 * b; if (x < 0) return false; w2.push_back(x); } }
    sort(w1.begin(), w1.end(), greater<int>()); sort(w2.begin(), w2.end(), greater<int>());
    P gam(m); for (int j = 0; j < m; j++) { gam[j] = w1[j] - lam[j]; if (gam[j] < 0 || gam[j] > n - m || (j && gam[j] > gam[j - 1])) return false; }
    P gc = conj(gam, n - m); for (int j = 0; j < n - m; j++) if (w2[j] != lamc[j] + gc[j]) return false;
    if (dump) { printf("RR"); for (int x : e) printf(" %d", x); printf(" |"); for (int k = 0; k < n; k++) if (S >> k & 1) printf(" %d", k + 1); printf(" |"); for (int j = m - 1; j >= 0; j--) printf(" %d", gam[j] + (m - j)); printf("\n"); }
    return true;
}
void rec(int k, int sl, bool cut) {
    if (k == n) { if (sl) return; tot++; long c = 0;
        for (uint32_t S = (1u << m) - 1; S < (1u << n);) { if (test(S)) c++; uint32_t t = S | (S - 1); S = (t + 1) | (((~t & -~t) - 1) >> (__builtin_ctz(S) + 1)); }
        good += c > 0; nsum += c;
        if (!c && verbose) { printf("  no RR-split with these rows:"); for (int x : e) printf(" %d", x); printf("%s\n", cut ? "   (tight cut)" : ""); }
        return; }
    int lo = k ? e[k - 1] - 1 : (allw ? 0 : 1);
    for (int x = max(lo, -sl); x <= n; x++) {
        int s2 = sl + x; bool c2 = cut || (k < n - 1 && s2 == 0); if (c2 && !allw) continue;
        if (s2 + (n - 1 - k) * x - (n - 1 - k) * (n - k) / 2 > 0) break;
        e[k] = x; rec(k + 1, s2, c2); }
}
int main(int argc, char** argv) {
    n = atoi(argv[1]); string pat = argv[2]; for (int i = 3; i < argc; i++) { if (!strcmp(argv[i], "v")) verbose = true; if (!strcmp(argv[i], "all")) allw = true; if (!strcmp(argv[i], "p")) dump = true; }
    vector<int> rr; for (int r = 1; r <= n; r++) if (pat[(r - 1) % pat.size()] == '1') rr.push_back(r);
    m = rr.size(); for (int j = 0; j < m; j++) lam.push_back(rr[j] - (j + 1)); sort(lam.begin(), lam.end(), greater<int>()); lamc = conj(lam, n - m);
    e.resize(n); rec(0, 0, false);
    printf("n = %d, R = %s..., %s: %ld; with an RR-split on the rows R: %ld; RR-splits per word: %.2f\n", n, pat.c_str(), allw ? "all valid words" : "words without a tight cut", tot, good, tot ? (double)nsum / tot : 0.);
}
