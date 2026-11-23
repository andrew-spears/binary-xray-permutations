// Odd splits.  D = {d_1 < ... < d_n} sums row + column on the n x n board.  For a set S of stones let
// L_S(R, C) = number of bijections R -> C with sums {d_k : k in S}.  N(D) = sum over (R, C) of L_S(R, C) L_{S^c}(R^c, C^c).
// D has an ODD SPLIT if for some S and (R, C) both factors are odd (then D is solvable).
// Prints, for every valid D of size n: is there an odd split with S a prefix {1..m}; with S arbitrary.
// Usage: ./oddsplit n [v]     (v: list the D without an odd split)
#include <bits/stdc++.h>
using namespace std;
int n; vector<vector<uint64_t>> T; int W;
static inline int idx(int R, int C) { return R << n | C; }
int main(int argc, char** argv) {
    n = atoi(argv[1]); bool verbose = argc > 2; W = ((1 << (2 * n)) + 63) / 64; int full = (1 << n) - 1;
    T.assign(1 << n, vector<uint64_t>(W));
    vector<int> d(n); long tot = 0, pre = 0, any = 0; map<int,int> bestm;
    function<void(int,int,int)> rec = [&](int k, int last, int sl) {
        if (k == n) {
            if (sl) return; tot++;
            // T[S] from T[S minus its top stone]
            fill(T[0].begin(), T[0].end(), 0); T[0][0] = 1;
            for (int S = 1; S <= full; S++) {
                int top = 31 - __builtin_clz(S), S0 = S ^ (1 << top), dd = d[top];
                auto& A = T[S0]; auto& B = T[S]; fill(B.begin(), B.end(), 0);
                for (int w = 0; w < W; w++) { uint64_t x = A[w];
                    while (x) { int b = __builtin_ctzll(x); x &= x - 1; int st = w * 64 + b, R = st >> n, C = st & full;
                        for (int r = max(1, dd - n); r <= min(n, dd - 1); r++) { int c = dd - r;
                            if (R >> (r - 1) & 1 || C >> (c - 1) & 1) continue;
                            int t = idx(R | 1 << (r - 1), C | 1 << (c - 1)); B[t >> 6] ^= 1ull << (t & 63); } } }
            }
            for (int i = 0; i < n; i++) printf("%d ", d[i] - 2 * (i + 1)); printf("|");
            for (int S = 1; S < full; S++) {
                auto& A = T[S]; auto& B = T[full ^ S]; long cnt = 0;
                for (int w = 0; w < W; w++) { uint64_t x = A[w];
                    while (x) { int b = __builtin_ctzll(x); x &= x - 1; int st = w * 64 + b, t = st ^ ((1 << (2 * n)) - 1);
                        if (B[t >> 6] >> (t & 63) & 1) cnt++; } }
                if (cnt) printf(" %d:%ld", S, cnt);
            }
            printf("\n");
            return;
        }
        for (int x = last + 1; x <= 2 * n; x++) { int s2 = sl + x - 2 * (k + 1); if (s2 < 0) continue; d[k] = x; rec(k + 1, x, s2); }
    };
    rec(0, 1, 0);
}
