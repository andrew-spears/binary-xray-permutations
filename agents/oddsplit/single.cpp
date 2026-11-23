// Odd splits of one word (any n <= 15).  Usage: ./single K e_1 ... e_n      (letters e_k = d_k - 2k)
// Tests the splits S = {e > 0}, S = {e >= 0}, S = {e odd}, every prefix, and then K random admissible S; prints which are odd.
#include <bits/stdc++.h>
using namespace std;
int n, full; vector<int> d; size_t W;
vector<uint64_t> run(int S) {
    vector<uint64_t> A(W), B(W); A[0] = 1;
    for (int k = 0; k < n; k++) if (S >> k & 1) {
        fill(B.begin(), B.end(), 0); int dd = d[k];
        for (size_t w = 0; w < W; w++) { uint64_t x = A[w];
            while (x) { int b = __builtin_ctzll(x); x &= x - 1; long st = w * 64 + b; int R = st >> n, C = st & full;
                for (int r = max(1, dd - n); r <= min(n, dd - 1); r++) { int c = dd - r;
                    if (R >> (r - 1) & 1 || C >> (c - 1) & 1) continue;
                    long t = (long)(R | 1 << (r - 1)) << n | (C | 1 << (c - 1)); B[t >> 6] ^= 1ull << (t & 63); } } }
        swap(A, B);
    }
    return A;
}
long odd(int S) {
    auto A = run(S), B = run(full ^ S); long cnt = 0, all = (1L << (2 * n)) - 1;
    for (size_t w = 0; w < W; w++) { uint64_t x = A[w];
        while (x) { int b = __builtin_ctzll(x); x &= x - 1; long t = (w * 64 + b) ^ all; if (B[t >> 6] >> (t & 63) & 1) cnt++; } }
    return cnt;
}
bool adm(int S) {
    int j = 0; for (int k = 0; k < n; k++) if (S >> k & 1) { j++; if (d[k] < 2 * j) return false; }
    j = 0; for (int k = n - 1; k >= 0; k--) if (!(S >> k & 1)) { j++; if (2 * n + 2 - d[k] < 2 * j) return false; }
    return true;
}
int main(int argc, char** argv) {
    int K = atoi(argv[1]); n = argc - 2; full = (1 << n) - 1; W = ((1UL << (2 * n)) + 63) / 64;
    vector<int> e(n); for (int k = 0; k < n; k++) { e[k] = atoi(argv[k + 2]); d.push_back(2 * (k + 1) + e[k]); }
    int Sp = 0, Sn = 0; for (int k = 0; k < n; k++) { if (e[k] > 0) Sp |= 1 << k; if (e[k] >= 0) Sn |= 1 << k; }
    printf("S = {e > 0}: %ld odd states;  S = {e >= 0}: %ld odd states\n", odd(Sp), odd(Sn));
    { int So = 0; for (int k = 0; k < n; k++) if (e[k] & 1) So |= 1 << k; printf("S = {e odd}: %ld odd states\n", odd(So)); }
    printf("prefix cuts (m: odd states):"); for (int m = 1; m < n; m++) if (adm((1 << m) - 1)) printf(" %d:%ld", m, odd((1 << m) - 1)); printf("\n");
    mt19937 rng(1); int tested = 0, good = 0, tries = 0;
    while (tested < K && tries < 100000 * (K + 1)) { int S = rng() & full; tries++; if (!S || S == full || !adm(S)) continue; tested++;
        long c = odd(S); if (c) { good++; if (good <= 3) { printf("  odd split: S ="); for (int k = 0; k < n; k++) if (S >> k & 1) printf(" %d", k + 1); printf("  (%ld odd states)\n", c); } } }
    printf("random admissible S: %d of %d are odd splits\n", good, tested);
}
