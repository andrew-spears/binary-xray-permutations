// A fixed set of rows.  R = the rows r (1-based) with pattern[(r - 1) mod len] == '1'.
// For every valid D of size n: is there a set S of stones such that the number of solutions whose stones in the rows of R
// are exactly S is odd?   Usage: ./fixedR n pattern      e.g. ./fixedR 10 10   (odd rows),  ./fixedR 9 100
#include <bits/stdc++.h>
using namespace std;
int n; uint32_t Rm; int rowd[16]; unordered_map<uint64_t, uint8_t> par; unordered_map<uint32_t, long> cnt;
void rec(int r, uint32_t used, uint32_t D) {
    if (r == n) { cnt[D]++; uint32_t S = 0; for (int i = 0; i < n; i++) if (Rm >> i & 1) S |= 1u << __builtin_popcount(D & ((1u << rowd[i]) - 1));
        auto it = par.find((uint64_t)D << 32 | S); if (it == par.end()) par[(uint64_t)D << 32 | S] = 1; else par.erase(it); return; }
    for (int c = 0; c < n; c++) if (!(used >> c & 1) && !(D >> (r + c) & 1)) { rowd[r] = r + c; rec(r + 1, used | 1u << c, D | 1u << (r + c)); }
}
int main(int argc, char** argv) {
    n = atoi(argv[1]); string pat = argv[2]; for (int r = 0; r < n; r++) if (pat[r % pat.size()] == '1') Rm |= 1u << r;
    rec(0, 0, 0); unordered_map<uint32_t, long> odd; for (auto& kv : par) odd[kv.first >> 32]++;
    long bad = 0, mn = LONG_MAX;
    for (auto& kv : cnt) { long o = odd.count(kv.first) ? odd[kv.first] : 0; mn = min(mn, o);
        if (!o) { bad++; if (bad <= 6) { printf("  no odd S: N = %ld, letters", kv.second); int k = 0; for (int d = 0; d < 2 * n; d++) if (kv.first >> d & 1) { printf(" %d", d + 2 - 2 * (k + 1)); k++; } printf("\n"); } } }
    printf("n = %d, R = %s...: valid D %zu; without an odd S: %ld; fewest odd S: %ld\n", n, pat.c_str(), cnt.size(), bad, mn);
}
