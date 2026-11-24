// Row sets.  T(R, S) = number of solutions in which the stones of S are exactly the stones in the rows of R (R any set of rows).
// For every valid D of size n: is some T(R, S) odd, with R not empty and not everything?  Usage: ./rowset n
#include <bits/stdc++.h>
using namespace std;
int n; int p[16];
int main(int argc, char** argv) {
    n = atoi(argv[1]); if (n < 2 || n > 12) { fprintf(stderr, "need 2 <= n <= 12 (a row set must be nonempty and proper)\n"); return 1; }
    iota(p, p + n, 0); unordered_map<uint32_t, vector<array<uint8_t, 12>>> W;
    do {
        uint32_t D = 0; bool ok = true;
        for (int r = 0; r < n; r++) { int d = r + p[r]; if (D >> d & 1) { ok = false; break; } D |= 1u << d; }
        if (!ok) continue;
        array<uint8_t, 12> st; for (int r = 0; r < n; r++) st[r] = __builtin_popcount(D & ((1u << (r + p[r])) - 1));
        W[D].push_back(st);
    } while (next_permutation(p, p + n));
    long good = 0, tot = 0; vector<uint8_t> par(1u << (2 * n));
    for (auto& kv : W) { tot++; auto& V = kv.second; if (V.size() == 1) { good++; continue; }
        fill(par.begin(), par.end(), 0); vector<uint32_t> touched;
        for (auto& st : V) for (uint32_t R = 1; R + 1 < (1u << n); R++) { uint32_t S = 0; for (uint32_t x = R; x; x &= x - 1) S |= 1u << st[__builtin_ctz(x)];
            uint32_t key = R << n | S; par[key] ^= 1; }
        long odd = 0; for (uint32_t k = 0; k < (1u << (2 * n)); k++) odd += par[k];
        if (odd) good++; else { printf("  no odd T(R, S): N = %zu, letters", V.size()); int k = 0; for (int d = 0; d < 2 * n; d++) if (kv.first >> d & 1) { printf(" %d", d + 2 - 2 * (k + 1)); k++; } printf("\n"); } }
    printf("n = %d: valid D %ld; with an odd T(R, S): %ld\n", n, tot, good);
}
