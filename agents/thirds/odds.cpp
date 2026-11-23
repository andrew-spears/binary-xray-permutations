// Odd sets for a fixed row set R.  R = rows r (1-based) with pattern[(r - 1) mod len] == '1'.
// T(S) = number of solutions of D whose stones in the rows of R are exactly S.  Prints, for every valid D of size n,
//   letters | N | tight (1 if D has a tight cut) | the S with T(S) odd, as n-bit strings (stone 1 first).
// Usage: ./odds n pattern      e.g. ./odds 9 100 > /tmp/odds_9.txt
#include <bits/stdc++.h>
using namespace std;
int n; uint32_t Rm; int rowd[16]; unordered_map<uint64_t, uint8_t> par; map<uint32_t, long> cnt;
void rec(int r, uint32_t used, uint32_t D) {
    if (r == n) { cnt[D]++; uint32_t S = 0; for (int i = 0; i < n; i++) if (Rm >> i & 1) S |= 1u << __builtin_popcount(D & ((1u << rowd[i]) - 1));
        auto it = par.find((uint64_t)D << 32 | S); if (it == par.end()) par[(uint64_t)D << 32 | S] = 1; else par.erase(it); return; }
    for (int c = 0; c < n; c++) if (!(used >> c & 1) && !(D >> (r + c) & 1)) { rowd[r] = r + c; rec(r + 1, used | 1u << c, D | 1u << (r + c)); }
}
int main(int argc, char** argv) {
    n = atoi(argv[1]); string pat = argv[2]; for (int r = 0; r < n; r++) if (pat[r % pat.size()] == '1') Rm |= 1u << r;
    rec(0, 0, 0); map<uint32_t, vector<uint32_t>> odd; for (auto& kv : par) odd[kv.first >> 32].push_back((uint32_t)kv.first);
    for (auto& kv : cnt) { int k = 0, sl = 0, tight = 0; for (int d = 0; d < 2 * n; d++) if (kv.first >> d & 1) { int e = d - 2 * k; printf("%d ", e); sl += e; k++; if (k < n && sl == 0) tight = 1; }
        printf("| %ld | %d |", kv.second, tight); auto& v = odd[kv.first]; sort(v.begin(), v.end());
        for (uint32_t S : v) { putchar(' '); for (int i = 0; i < n; i++) putchar(S >> i & 1 ? '1' : '0'); } printf("\n"); }
}
