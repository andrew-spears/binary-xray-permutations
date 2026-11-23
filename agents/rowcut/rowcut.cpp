// Row cuts.  For a valid D of size n, a in [1, n-1] and a set S of a stones (indices in sorted D), let
//   T_a(S) = number of solutions in which the stones of S are exactly the stones in the top a rows.
// If some T_a(S) is odd then D is solvable.  Prints, for all valid D of size n: how many have an odd T_a(S), and the D without one.
// Usage: ./rowcut n
#include <bits/stdc++.h>
using namespace std;
int n; int p[16]; unordered_map<uint64_t, uint8_t> par; unordered_map<uint32_t, long> cnt;
int main(int argc, char** argv) {
    n = atoi(argv[1]); iota(p, p + n, 0); par.reserve(1 << 24);
    do {
        uint32_t D = 0; bool ok = true;
        for (int r = 0; r < n; r++) { int d = r + p[r]; if (D >> d & 1) { ok = false; break; } D |= 1u << d; }
        if (!ok) continue;
        cnt[D]++; uint32_t S = 0;
        for (int r = 0; r < n - 1; r++) { int d = r + p[r]; S |= 1u << __builtin_popcount(D & ((1u << d) - 1));
            par[(uint64_t)D << 32 | (uint64_t)(r + 1) << 16 | S] ^= 1; }
    } while (next_permutation(p, p + n));
    unordered_map<uint32_t, array<long, 16>> odd;
    for (auto& kv : par) if (kv.second) odd[kv.first >> 32][(kv.first >> 16) & 15]++;
    long good = 0; 
    for (auto& kv : cnt) { uint32_t D = kv.first; bool has = odd.count(D);
        if (__builtin_popcount(D) == n && kv.second == 1) continue;          // skip nothing: unique-solution D are odd anyway
        if (has) good++; else { printf("  no odd row cut: N = %ld, letters", kv.second); int k = 0; for (int d = 0; d < 2 * n; d++) if (D >> d & 1) { printf(" %d", d + 2 - 2 * (k + 1)); k++; } printf("\n"); } }
    long uniq = 0; for (auto& kv : cnt) if (kv.second == 1) uniq++;
    printf("n = %d: valid D %zu (with one solution: %ld); with an odd T_a(S): %ld\n", n, cnt.size(), uniq, good + uniq);
    if (argc > 2) for (auto& kv : odd) { uint32_t D = kv.first; printf("D"); int k = 0; for (int d = 0; d < 2 * n; d++) if (D >> d & 1) { printf(" %d", d + 2 - 2 * (k + 1)); k++; } printf(" : N = %ld; odd S per a:", cnt[D]); for (int a = 1; a < n; a++) printf(" %ld", kv.second[a]); printf("\n"); }
}
