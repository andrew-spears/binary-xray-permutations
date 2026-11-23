// witenum.c: enumerate ALL permutations with distinct diagonals (= witnesses of some D),
// group by D, and record the set A_wit(D) of induced parity vectors.
// Convention: rows 1..n, a(d) = row mod 2.  a encoded as mask over sorted stones:
// bit k = a(d_k), d_0 < d_1 < ... (k = 0 is the smallest diagonal).
// Output lines:  d_0 ... d_{n-1} | nwit | firstA | hexbitset(2^n bits, bit a set iff a in A_wit)
// firstA = parity mask of the lexicographically first witness (permutation order by rows).
// Usage: ./witenum n > wit_n.txt
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <immintrin.h>

int n, M; // marks 0..2n-2 <-> diagonal m-(n-1)
int *idx; // mark-mask -> D index
int nD; int *flags; int perm[32]; uint32_t *Dmask; long long *nwit; int *firstA; uint64_t *bits; int W;
uint32_t parmask;

void rec(int r, uint32_t usedDg, uint32_t usedC) {
    if (r == n) {
        int id = idx[usedDg];
        if (id < 0) { id = nD++; idx[usedDg] = id; Dmask[id] = usedDg; firstA[id] = -1; }
        int a = (int)_pext_u32(parmask, usedDg);
        nwit[id]++;
        { int inv=1, cen=1; for (int i=0;i<n;i++){ if (perm[perm[i]]!=i) inv=0; if (perm[n-1-i]!=n-1-perm[i]) cen=0; }
          flags[id] |= inv | (cen<<1); }
        if (firstA[id] < 0) firstA[id] = a;
        bits[(size_t)id * W + (a >> 6)] |= 1ULL << (a & 63);
        return;
    }
    // row r (0-based) is row r+1; parity (r+1)&1
    uint32_t pb = (r + 1) & 1;
    for (int c = 0; c < n; c++) {
        if (usedC >> c & 1) continue;
        int m = c - r + n - 1;
        if (usedDg >> m & 1) continue;
        if (pb) parmask |= 1u << m;
        perm[r] = c;
        rec(r + 1, usedDg | 1u << m, usedC | 1u << c);
        if (pb) parmask &= ~(1u << m);
    }
}

int main(int argc, char **argv) {
    n = atoi(argv[1]); M = 2 * n - 1;
    idx = malloc(sizeof(int) << M); memset(idx, -1, sizeof(int) << M);
    int cap = 60000;
    W = ((1 << n) + 63) / 64;
    Dmask = calloc(cap, 4); flags = calloc(cap, 4); nwit = calloc(cap, 8); firstA = calloc(cap, 4);
    bits = calloc((size_t)cap * W, 8);
    rec(0, 0, 0);
    // sort output by D mask for stable order (by sorted d tuple lex): just output in index order
    for (int id = 0; id < nD; id++) {
        uint32_t dm = Dmask[id];
        for (int m = 0; m < M; m++) if (dm >> m & 1) printf("%d ", m - (n - 1));
        printf("| %lld | %d | ", nwit[id], firstA[id]);
        // hex bitset, little-endian bit order: print words from 0..W-1
        for (int w = 0; w < W; w++) printf("%016llx", (unsigned long long)bits[(size_t)id * W + w]);
        printf(" | %d\n", flags[id]);
    }
    fprintf(stderr, "n=%d nD=%d\n", n, nD);
    return 0;
}
