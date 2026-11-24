// The fixed-rows claim on words of bounded slack, for n beyond the exhaustive range.
// Words: e_1..e_n without a tight cut, all prefix sums in [1, smax].  For such a word the interface states have at most smax
// cells, so  P(t) = sum over solutions of prod_{stones k in a row of R} t_k  is computed by a transfer matrix over the
// states (used rows, used columns), in the field GF(2^64) with random t_k.  P(t) is a multilinear polynomial whose
// coefficient of prod_{k in S} t_k is T(R, S) mod 2, so
//     P(t) != 0  =>  some T(R, S) is odd (certain);     P(t) = 0 for 3 independent random t  =>  no odd S (error < 2^-170).
// R = rows r (1-based) with pattern[(r - p) mod len] == '1', every phase p.
// Usage: ./lowslack n smax [pattern]     prints every (word, phase) with no odd S.     (g++ -O2 -mpclmul)
#include <bits/stdc++.h>
#include <wmmintrin.h>
using namespace std;
typedef uint64_t u64;
static inline u64 gmul(u64 a, u64 b) {      // GF(2)[x] / (x^64 + x^4 + x^3 + x + 1)
    __m128i p = _mm_clmulepi64_si128(_mm_cvtsi64_si128(a), _mm_cvtsi64_si128(b), 0);
    u64 lo = _mm_cvtsi128_si64(p), hi = _mm_cvtsi128_si64(_mm_srli_si128(p, 8));
    u64 t = hi ^ (hi >> 63) ^ (hi >> 61) ^ (hi >> 60);
    return lo ^ t ^ (t << 1) ^ (t << 3) ^ (t << 4);
}
int n, smax; string pat = "100"; vector<int> e; long tot = 0, bad = 0, zerosol = 0; u64 tv[3][64]; size_t maxstates = 0;
struct St { u64 rows, cols; bool operator==(const St& o) const { return rows == o.rows && cols == o.cols; } };
struct H { size_t operator()(const St& s) const { return (s.rows * 0x9E3779B97F4A7C15ull) ^ (s.cols * 0xC2B2AE3D27D4EB4Full) ^ (s.rows >> 29); } };
void test() {
    tot++; int L = pat.size();
    for (int p = 0; p < L; p++) {
        bool odd = false, any = false;
        for (int trial = 0; trial < 3 && !odd; trial++) {
            unordered_map<St, array<u64, 2>, H> cur, nxt; cur[{0, 0}] = {1, 1};   // value, and number of placements (capped) to detect "no solution"
            for (int k = 0; k < n; k++) {
                int d = 2 * k + e[k]; nxt.clear();
                for (auto& kv : cur) {
                    u64 rows = kv.first.rows, cols = kv.first.cols;
                    // stone k must not skip a row/column that can no longer be filled: every later stone has diagonal > d
                    for (int r = max(0, d - (n - 1)); r <= min(d, n - 1); r++) { int c = d - r;
                        if ((rows >> r & 1) || (cols >> c & 1)) continue;
                        bool inR = pat[(((r + 1 - p) % L) + L) % L] == '1';
                        auto& x = nxt[{rows | 1ull << r, cols | 1ull << c}];
                        x[0] ^= inR ? gmul(kv.second[0], tv[trial][k]) : kv.second[0]; x[1] = min<u64>(x[1] + kv.second[1], 1ull << 62); } }
                // prune states that cannot be completed: an unused row r and unused column c with r + c <= d can never be used together,
                // and the smallest unused row r0 needs a later diagonal d' > d with column d' - r0 unused; keep it simple: drop states
                // whose smallest unused row + smallest unused column is <= d (that cell's diagonal is gone and both must pair with something larger: fine)
                cur.swap(nxt); maxstates = max(maxstates, cur.size());
            }
            auto it = cur.find({(1ull << n) - 1, (1ull << n) - 1});
            if (it != cur.end()) { any = it->second[1] > 0; if (it->second[0]) odd = true; }
        }
        if (!any) zerosol++;
        if (!odd) { bad++; printf("  no odd S: e ="); for (int x : e) printf(" %d", x); printf(", phase %d%s\n", p, any ? "" : "  (no solution!)"); }
    }
}
void rec(int k, int sl) {
    if (k == n) { if (sl == 0) test(); return; }
    int lo = k ? e[k - 1] - 1 : 1;
    for (int x = max(lo, -sl); sl + x <= smax; x++) { int s2 = sl + x; if (k < n - 1 && s2 <= 0) continue;
        if (s2 + (n - 1 - k) * x - (n - 1 - k) * (n - k) / 2 > 0) break; e[k] = x; rec(k + 1, s2); }
}
int main(int argc, char** argv) {
    n = atoi(argv[1]); smax = atoi(argv[2]); if (argc > 3) pat = argv[3];
    mt19937_64 rng(20261124); for (auto& a : tv) for (auto& x : a) x = rng() | 1;
    e.assign(n, 0); rec(0, 0);
    printf("n = %d, prefix sums in [1, %d], pattern %s: words %ld; (word, phase) without an odd S: %ld; without a solution: %ld; max states %zu\n", n, smax, pat.c_str(), tot, bad, zerosol, maxstates);
}
