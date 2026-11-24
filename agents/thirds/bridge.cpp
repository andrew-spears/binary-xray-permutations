// Prefixes that end at slack 1.  A = e_1 .. e_m with all prefix sums >= 0 and sum 1.  After A the used rows and columns
// are (rows 1..m-1 and m+1, columns 1..m) ["row state"] or (rows 1..m, columns 1..m-1 and m+1) ["column state"].
// For a phase p in {0,1,2}, R = rows r (1-based) with r = p (mod 3).   Question: is there a set S of stones of A such
// that the number of partial placements of A in the given state whose stones in the rows of R are exactly S is odd?
// Usage: ./bridge m [pattern]   lists every (A, state, phase) with no odd S.  pattern (default 100) is repeated; phase p
// shifts it: row r is in R iff pattern[(r - p) mod len] == '1'  (so p = 1 is R = rows 1, 4, 7, ... for pattern 100).
#include <bits/stdc++.h>
using namespace std;
int m; vector<int> e; string pat = "100"; long tot = 0, bad = 0, nowhere = 0;
uint32_t Dmask; vector<uint32_t> Sv; vector<int> rowsv; uint32_t colmask; unordered_map<uint32_t, int> par;
int Rbit[40];
void dfs(int i, uint32_t usedc, uint32_t left, uint32_t S) {
    if (i == (int)rowsv.size()) { par[S] ^= 1; return; }
    int r = rowsv[i];
    for (uint32_t x = left; x; x &= x - 1) { int d = __builtin_ctz(x); int c = d - r; if (c < 0 || c > m || !(colmask >> c & 1) || (usedc >> c & 1)) continue;
        int k = __builtin_popcount(Dmask & ((1u << d) - 1)); dfs(i + 1, usedc | 1u << c, left & ~(1u << d), Rbit[r] ? S | 1u << k : S); }
}
void test() {
    tot++; Dmask = 0; for (int k = 0; k < m; k++) Dmask |= 1u << (2 * k + e[k]);
    for (int st = 0; st < 2; st++) {
        rowsv.clear(); colmask = 0;
        if (st == 0) { for (int r = 0; r < m - 1; r++) rowsv.push_back(r); rowsv.push_back(m); colmask = (1u << m) - 1; }
        else { for (int r = 0; r < m; r++) rowsv.push_back(r); colmask = ((1u << (m - 1)) - 1) | 1u << m; }
        bool any = false;
        for (int p = 0; p < (int)pat.size(); p++) {
            for (int r = 0; r <= m; r++) Rbit[r] = pat[(((r + 1 - p) % (int)pat.size()) + pat.size()) % pat.size()] == '1';
            par.clear(); dfs(0, 0, Dmask, 0); bool odd = false, pos = !par.empty(); for (auto& kv : par) if (kv.second) odd = true;
            if (pos) any = true;
            if (pos && !odd) { bad++; printf("  no odd S: A ="); for (int x : e) printf(" %d", x); printf(", %s state, phase %d\n", st ? "column" : "row", p); } }
        if (!any) nowhere++; }
}
void rec(int k, int sl) {
    if (k == m) { if (sl == 1) test(); return; }
    int lo = k ? e[k - 1] - 1 : 0;
    for (int x = max(lo, -sl); x <= m + 1; x++) { int s2 = sl + x; if (s2 + (m - 1 - k) * x - (m - 1 - k) * (m - k) / 2 > 1) break; e[k] = x; rec(k + 1, s2); }
}
int main(int argc, char** argv) { m = atoi(argv[1]); if (argc > 2) pat = argv[2]; e.assign(m, 0); rec(0, 0);
    printf("m = %d, pattern %s: prefixes with slack 1: %ld; (A, state, phase) with placements but no odd S: %ld; (A, state) with no placement at all: %ld\n", m, pat.c_str(), tot, bad, nowhere); }
