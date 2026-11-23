// Levels.  For a set A of stones and a map rho: A -> rows let c(A, rho) = number of solutions with stone k in row rho(k) for all k in A.
// level(D) = the smallest |A| for which some c(A, rho) is odd  (level 0 <=> N odd; level 1 <=> the matrix M(k, r) = N(k, r) mod 2 is not 0).
// For a row set R:  G_R(A) = sum over rho: A -> R of c(A, rho) = number of solutions with all stones of A in rows of R, and
// (some T(R, S) is odd)  <=>  (some G_R(A) is odd)   [P(t) = sum_S T(R,S) t^S,  G_R(A) = coefficient of t^A in P(1 + t)].
// So the smallest |A| with G_R(A) odd is >= level(D).  This program tests EQUALITY:  is some G_R(A) with |A| = level(D) odd?
// R = rows r (1-based) with pattern[(r - p) mod len] == '1', every phase p; words without a tight cut (levels add over the
// blocks of a tight cut, so equality for these words and all phases gives equality for every valid D).
// Usage: ./levels n [pattern] [v]      (default pattern 100)
#include <bits/stdc++.h>
using namespace std;
int n; string pat = "100"; bool verbose; vector<int> e; vector<array<signed char, 16>> sols; array<signed char, 16> cur;
long tot = 0, failw = 0, failwp = 0; map<int, long> levd, levf;
void solve(int k, unsigned rows, unsigned cols) {
    if (k == n) { sols.push_back(cur); return; }
    int d = 2 * k + e[k];
    for (int r = max(0, d - (n - 1)); r <= min(d, n - 1); r++) { int c = d - r;
        if ((rows >> r & 1) || (cols >> c & 1)) continue; cur[k] = r; solve(k + 1, rows | 1u << r, cols | 1u << c); }
}
void test() {
    tot++; sols.clear(); solve(0, 0, 0); int L = pat.size(); vector<uint64_t> keys(sols.size());
    for (int j = 0; j <= n; j++) {
        bool found = false; vector<char> okp(L, 0);
        vector<int> A(j); for (int i = 0; i < j; i++) A[i] = i;
        while (true) {
            for (size_t s = 0; s < sols.size(); s++) { uint64_t key = 0; for (int i : A) key = key << 4 | sols[s][i]; keys[s] = key; }
            sort(keys.begin(), keys.end());
            for (size_t a = 0; a < keys.size();) { size_t b = a; while (b < keys.size() && keys[b] == keys[a]) b++; if ((b - a) & 1) found = true; a = b; }
            for (int p = 0; p < L; p++) { long c = 0;
                for (auto& s : sols) { bool in = true; for (int i : A) if (pat[(((s[i] + 1 - p) % L) + L) % L] != '1') { in = false; break; } c += in; }
                if (c & 1) okp[p] = 1; }
            int i = j - 1; while (i >= 0 && A[i] == n - j + i) i--;
            if (i < 0) break;
            A[i]++; for (int q = i + 1; q < j; q++) A[q] = A[q - 1] + 1;
        }
        if (found) { levd[j]++; int nf = 0; for (int p = 0; p < L; p++) nf += !okp[p];
            if (nf) { failw++; failwp += nf; levf[j]++; if (verbose || failw <= 5) { printf("  level %d, N = %zu, phases without an odd G_R(A), |A| = level:", j, sols.size());
                for (int p = 0; p < L; p++) if (!okp[p]) printf(" %d", p); printf(";  e ="); for (int x : e) printf(" %d", x); printf("\n"); } }
            return; }
    }
}
void rec(int k, int sl) {
    if (k == n) { if (sl == 0) test(); return; }
    int lo = k ? e[k - 1] - 1 : 1;
    for (int x = max(lo, -sl); x < n; x++) { int s2 = sl + x; if (k < n - 1 && s2 <= 0) continue;
        if (s2 + (n - 1 - k) * x - (n - 1 - k) * (n - k) / 2 > 0) break; e[k] = x; rec(k + 1, s2); }
}
int main(int argc, char** argv) {
    n = atoi(argv[1]); if (argc > 2) pat = argv[2]; verbose = argc > 3; e.assign(n, 0); rec(0, 0);
    printf("n = %d, pattern %s: words without a tight cut %ld; level -> words:", n, pat.c_str(), tot);
    for (auto& kv : levd) printf(" %d: %ld", kv.first, kv.second);
    printf("; words where some phase has no odd G_R(A) with |A| = level: %ld (word, phase pairs: %ld); by level:", failw, failwp);
    for (auto& kv : levd) printf(" %d: %ld", kv.first, levf[kv.first]); printf("\n");
}
