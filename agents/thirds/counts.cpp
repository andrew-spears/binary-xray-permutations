// Full counts for a fixed row set R (see odds.cpp).  Prints for every valid D of size n:
//   letters | N | tight | S:T(S) for every S with T(S) > 0  (S as n-bit string, stone 1 first)
// Usage: ./counts n pattern
#include <bits/stdc++.h>
using namespace std;
int n; uint32_t Rm; int rowd[16]; unordered_map<uint64_t, uint32_t> par; map<uint32_t, long> cnt;
void rec(int r, uint32_t used, uint32_t D) {
    if (r == n) { cnt[D]++; uint32_t S = 0; for (int i = 0; i < n; i++) if (Rm >> i & 1) S |= 1u << __builtin_popcount(D & ((1u << rowd[i]) - 1));
        par[(uint64_t)D << 32 | S]++; return; }
    for (int c = 0; c < n; c++) if (!(used >> c & 1) && !(D >> (r + c) & 1)) { rowd[r] = r + c; rec(r + 1, used | 1u << c, D | 1u << (r + c)); }
}
int main(int argc, char** argv) {
    n = atoi(argv[1]); string pat = argv[2]; for (int r = 0; r < n; r++) if (pat[r % pat.size()] == '1') Rm |= 1u << r;
    rec(0, 0, 0); map<uint32_t, vector<pair<uint32_t, uint32_t>>> odd; for (auto& kv : par) odd[kv.first >> 32].push_back({(uint32_t)kv.first, kv.second});
    for (auto& kv : cnt) { int k = 0, sl = 0, tight = 0; for (int d = 0; d < 2 * n; d++) if (kv.first >> d & 1) { int e = d - 2 * k; printf("%d ", e); sl += e; k++; if (k < n && sl == 0) tight = 1; }
        printf("| %ld | %d |", kv.second, tight); auto& v = odd[kv.first]; sort(v.begin(), v.end());
        for (auto& S : v) { putchar(' '); for (int i = 0; i < n; i++) putchar(S.first >> i & 1 ? '1' : '0'); printf(":%u", S.second); } printf("\n"); }
}
