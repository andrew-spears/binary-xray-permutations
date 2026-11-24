// The exact class of row sets that work.  A row pattern w in {0,1}^n (R = positions of the ones) WORKS if every valid D
// of size n has a set S of stones with  T(R, S) = #{solutions whose stones in the rows of R are exactly S}  odd.
// If D has a tight cut, T is a product over the blocks, so w works  <=>  every factor (substring) v of w is "good":
// v has an odd S for every D of size |v| WITHOUT a tight cut.  The class is closed under factors, complement
// and reversal, so it is given by its minimal forbidden words.  This program finds them length by length.
// Usage: ./forbid nmax [part parts]      prints, for each n <= nmax, the number of working words and the minimal
// forbidden words (up to complement and reversal) with one D that kills each.
#include <bits/stdc++.h>
using namespace std;
int n; vector<int> e; vector<uint32_t> alive; vector<vector<int>> killer; vector<uint32_t> dead;
vector<uint64_t> sols; int dsum[16]; uint32_t Dmask;
void solve(int r, uint32_t used, uint32_t left, uint64_t packed) {
    if (r == n) { sols.push_back(packed); return; }
    for (uint32_t m = left; m; m &= m - 1) { int d = __builtin_ctz(m); int c = d - r; if (c < 0 || c >= n || (used >> c & 1)) continue;
        int k = __builtin_popcount(Dmask & ((1u << d) - 1)); solve(r + 1, used | 1u << c, left & ~(1u << d), packed | (uint64_t)k << (4 * r)); }
}
vector<uint8_t> tab; vector<uint32_t> lo, hi, Sv;
void testD() {
    Dmask = 0; for (int k = 0; k < n; k++) Dmask |= 1u << (2 * k + e[k]);
    sols.clear(); solve(0, 0, Dmask, 0); if (sols.empty()) { printf("UNSOLVABLE D!\n"); exit(1); }
    int h = n / 2, g = n - h; size_t ns = sols.size(); lo.assign(ns << h, 0); hi.assign(ns << g, 0);
    for (size_t i = 0; i < ns; i++) { uint32_t* L = &lo[i << h]; uint32_t* H = &hi[i << g];
        for (uint32_t m = 1; m < (1u << h); m++) { int b = __builtin_ctz(m); L[m] = L[m & (m - 1)] | 1u << (sols[i] >> (4 * b) & 15); }
        for (uint32_t m = 1; m < (1u << g); m++) { int b = __builtin_ctz(m); H[m] = H[m & (m - 1)] | 1u << (sols[i] >> (4 * (b + h)) & 15); } }
    Sv.resize(ns);
    for (size_t a = 0; a < alive.size();) { uint32_t R = alive[a], Rl = R & ((1u << h) - 1), Rh = R >> h; bool odd = false;
        for (size_t i = 0; i < ns; i++) { uint32_t S = lo[(i << h) | Rl] | hi[(i << g) | Rh]; Sv[i] = S; tab[S] ^= 1; }
        for (size_t i = 0; i < ns; i++) { if (tab[Sv[i]]) odd = true; tab[Sv[i]] = 0; }
        if (!odd) { dead.push_back(R); killer.push_back(e); alive[a] = alive.back(); alive.pop_back(); } else a++; }
}
long idx = 0; int part = 0, parts = 1;
void rec(int k, int sl) {
    if (k == n) { if (sl) return; if (idx++ % parts == part && !alive.empty()) testD(); return; }
    int lo_ = k ? e[k - 1] - 1 : 1;
    for (int x = max(lo_, -sl); x <= n; x++) { int s2 = sl + x; if (k < n - 1 && s2 <= 0) continue;
        if (s2 + (n - 1 - k) * x - (n - 1 - k) * (n - k) / 2 > 0) break; e[k] = x; rec(k + 1, s2); }
}
uint32_t rev(uint32_t w, int n) { uint32_t r = 0; for (int i = 0; i < n; i++) if (w >> i & 1) r |= 1u << (n - 1 - i); return r; }
uint32_t canon(uint32_t w, int n) { uint32_t c = ~w & ((1u << n) - 1); return min(min(w, rev(w, n)), min(c, rev(c, n))); }
string str(uint32_t w, int n) { string s; for (int i = 0; i < n; i++) s += (w >> i & 1) ? '1' : '0'; return s; }
int main(int argc, char** argv) {
    int nmax = atoi(argv[1]); if (argc > 3) { part = atoi(argv[2]); parts = atoi(argv[3]); }
    set<uint32_t> prev = {0, 1};   // working words of length n - 1 (as masks)
    for (n = 2; n <= nmax; n++) {
        vector<uint32_t> cand; for (uint32_t w = 0; w < (1u << n); w++) if (prev.count(w >> 1) && prev.count(w & ((1u << (n - 1)) - 1))) cand.push_back(w);
        set<uint32_t> cs; for (uint32_t w : cand) cs.insert(canon(w, n)); alive.assign(cs.begin(), cs.end()); dead.clear(); killer.clear();
        e.assign(n, 0); tab.assign(1u << n, 0); idx = 0; if (n == 1) { } else rec(0, 0);
        set<uint32_t> al(alive.begin(), alive.end()); set<uint32_t> now; for (uint32_t w : cand) if (al.count(canon(w, n))) now.insert(w);
        printf("n = %d: D without a tight cut %ld; candidates %zu; working words %zu; minimal forbidden (up to complement, reversal) %zu:", n, idx, cand.size(), now.size(), dead.size());
        for (size_t i = 0; i < dead.size(); i++) { printf("  %s [", str(dead[i], n).c_str()); for (int x : killer[i]) printf(" %d", x); printf(" ]"); } printf("\n"); fflush(stdout);
        prev = now; }
    if (parts == 1) { printf("working words of length %d (up to complement, reversal):", nmax); for (uint32_t w : alive) printf(" %s", str(w, nmax).c_str()); printf("\n"); }
}
