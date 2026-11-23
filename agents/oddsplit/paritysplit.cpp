// The parity split: S = stones on odd diagonals (odd letters), S^c = stones on even diagonals.
// For every valid D of size n (not evenly spaced): is there (R, C) with L_S(R, C) and L_{S^c}(R^c, C^c) both odd?
// Usage: ./paritysplit n [step]     (step > 1: test only every step-th valid D)
#include <bits/stdc++.h>
using namespace std;
int n, full; vector<int> d; size_t W; long tot = 0, tested = 0, bad = 0, step = 1; long minodd = LONG_MAX;
vector<uint64_t> A, B, P, Q;
void run(int S, vector<uint64_t>& out) {
    fill(A.begin(), A.end(), 0); A[0] = 1;
    for (int k = 0; k < n; k++) if (S >> k & 1) {
        fill(B.begin(), B.end(), 0); int dd = d[k];
        for (size_t w = 0; w < W; w++) { uint64_t x = A[w];
            while (x) { int b = __builtin_ctzll(x); x &= x - 1; long st = w * 64 + b; int R = st >> n, C = st & full;
                for (int r = max(1, dd - n); r <= min(n, dd - 1); r++) { int c = dd - r;
                    if (R >> (r - 1) & 1 || C >> (c - 1) & 1) continue;
                    long t = (long)(R | 1 << (r - 1)) << n | (C | 1 << (c - 1)); B[t >> 6] ^= 1ull << (t & 63); } } }
        swap(A, B);
    }
    out = A;
}
void test() {
    int S = 0; for (int k = 0; k < n; k++) if (d[k] & 1) S |= 1 << k;
    if (!S) return;                                        // evenly spaced
    tot++; if (tot % step) return; tested++;
    run(S, P); run(full ^ S, Q); long cnt = 0, all = (1L << (2 * n)) - 1;
    for (size_t w = 0; w < W; w++) { uint64_t x = P[w];
        while (x) { int b = __builtin_ctzll(x); x &= x - 1; long t = (w * 64 + b) ^ all; if (Q[t >> 6] >> (t & 63) & 1) cnt++; } }
    minodd = min(minodd, cnt);
    if (!cnt) { bad++; if (bad <= 5) { printf("  NO parity split: letters"); for (int k = 0; k < n; k++) printf(" %d", d[k] - 2 * (k + 1)); printf("\n"); } }
}
void rec(int k, int last, int sl) {
    if (k == n) { if (sl == 0) test(); return; }
    for (int x = last + 1; x <= 2 * n; x++) { int s2 = sl + x - 2 * (k + 1); if (s2 < 0) continue; d[k] = x; rec(k + 1, x, s2); }
}
int main(int argc, char** argv) {
    n = atoi(argv[1]); if (argc > 2) step = atol(argv[2]); full = (1 << n) - 1; W = ((1UL << (2 * n)) + 63) / 64; d.resize(n);
    A.resize(W); B.resize(W); rec(0, 1, 0);
    printf("n = %d: valid D other than the evenly spaced one: %ld; tested %ld; without a parity split: %ld; fewest odd states: %ld\n", n, tot, tested, bad, minodd);
}
