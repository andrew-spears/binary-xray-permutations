// blocks.c: enumerate all permutations of size n with distinct diagonals d=p(i)-i,
// group by diagonal set D, record block statistics per D.
// Output: one line per realized D (all of them; postprocess filters):
//   mask nwit flags W2 Wmerge Woneside Wfar Wcorner W2ok
// mask: bit m <-> diagonal m-(n-1).  W*: bitmask over mark of lower stone x of a 2-block {x,x+2}.
// flags bits:
//  0 has 2-block            1 has two disjoint 2-blocks     2 has 3-block
//  3 has 132/213 3-block    4 has 321 3-block
//  5 some 2-block contraction sigma is direct sum
//  6 some 2-block contraction sigma has distinct diagonals AND tight cut
//  7 some 2-block contraction sigma has distinct diagonals
//  8 some 3-block contraction: direct sum or (distinct & tight)
//  9 some block (any size 2..n-1) contraction: direct sum or (distinct & tight)
// 10 some 2-block contraction: direct sum or (distinct & tight)
// 11 witness is itself a direct sum (some witness)
// Wmerge: 2-block with no point above-right and none below-left (sigma's D = merge).
// Woneside: AR empty or BL empty.
// Wfar: AR u BL = all other points with |d-centre|>=3.
// Wcorner: block in top-left or bottom-right corner.
// W2ok: 2-block whose contraction has distinct diagonals.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

int n, M;
int p[32];
typedef struct { uint32_t mask; long long nwit; uint32_t flags, W2, Wm, Wo, Wf, Wc, Wok, We; } Rec;
Rec *recs; int nrec, cap; int *idx;

static int tightcut(int *d, int m) { // d sorted ascending, size m
    int t = 0;
    for (int k = 1; k < m; k++) { t += d[k - 1] + m - k; if (t == k * (k - 1) / 2) return 1; }
    return 0;
}
static int directsum(int *q, int m) {
    int mx = -1;
    for (int j = 0; j < m - 1; j++) { if (q[j] > mx) mx = q[j]; if (mx == j) return 1; }
    return 0;
}
// contract rows a..a+k-1 (cols lo..lo+k-1) of p into one point; returns
// bit0 direct sum, bit1 distinct diagonals, bit2 tight (if distinct)
static int contract(int a, int k, int lo) {
    int q[32], m = 0;
    for (int i = 0; i < n; i++) {
        if (i >= a && i < a + k) { if (i == a) q[m++] = lo; continue; }
        int c = p[i]; if (c > lo) c -= k - 1;
        q[m++] = c;
    }
    int r = directsum(q, m) ? 1 : 0;
    int cnt[64] = {0}, dist = 1;
    for (int i = 0; i < m; i++) { int d = q[i] - i + 32; if (cnt[d]++) dist = 0; }
    if (dist) {
        r |= 2;
        int ds[32], t = 0;
        for (int d = 0; d < 64; d++) if (cnt[d]) ds[t++] = d - 32;
        if (tightcut(ds, m)) r |= 4;
    }
    return r;
}

static void leaf(uint32_t dm) {
    int id = idx[dm];
    if (id < 0) {
        if (nrec == cap) { cap *= 2; recs = realloc(recs, sizeof(Rec) * cap); }
        id = nrec++; idx[dm] = id; memset(&recs[id], 0, sizeof(Rec)); recs[id].mask = dm;
    }
    Rec *R = &recs[id];
    R->nwit++;
    uint32_t f = 0;
    if (directsum(p, n)) f |= 1u << 11;
    int first2 = -1, last2 = -1;
    for (int i = 0; i + 1 < n; i++) {
        if (p[i] != p[i + 1] + 1) continue;
        f |= 1;
        if (first2 < 0) first2 = i;
        if (i - first2 >= 2) f |= 2;
        last2 = i;
        int c = p[i + 1], r = i;                // block rows r,r+1 cols c,c+1
        int x = c - r - 1, cen = c - r;         // stones x, x+2
        int xm = x + n - 1;
        R->W2 |= 1u << xm;
        int ar = 0, bl = 0, farok = 1;
        for (int j = 0; j < n; j++) {
            if (j == r || j == r + 1) continue;
            int d = p[j] - j;
            int isAR = (j < r && p[j] > c + 1), isBL = (j > r + 1 && p[j] < c);
            ar |= isAR; bl |= isBL;
            int far = (d - cen >= 3 || cen - d >= 3);
            if (far != (isAR || isBL)) farok = 0;
        }
        if (!ar && !bl) R->Wm |= 1u << xm;
        { // Wext: one side empty, shifted set = the |cen| most extreme stones on the other side
          int okx = 1, need = cen > 0 ? cen : -cen;
          // rank of each other point among other points by diagonal
          for (int j = 0; j < n && okx; j++) {
            if (j == r || j == r + 1) continue;
            int d = p[j] - j, rk = 0;
            for (int k = 0; k < n; k++) { if (k == r || k == r + 1) continue; int e = p[k] - k; if (cen > 0 ? e < d : e > d) rk++; }
            int isAR = (j < r && p[j] > c + 1), isBL = (j > r + 1 && p[j] < c);
            int want = rk < need;
            if (cen > 0) { if (isAR || isBL != want) okx = 0; }
            else if (cen < 0) { if (isBL || isAR != want) okx = 0; }
            else { if (isAR || isBL) okx = 0; }
          }
          if (okx) R->We |= 1u << xm; }
        if (!ar || !bl) R->Wo |= 1u << xm;
        if (farok) R->Wf |= 1u << xm;
        if ((r == 0 && c == 0) || (r == n - 2 && c == n - 2)) R->Wc |= 1u << xm;
        int cr = contract(r, 2, c);
        if (cr & 1) f |= 1u << 5;
        if ((cr & 6) == 6) f |= 1u << 6;
        if (cr & 2) { f |= 1u << 7; R->Wok |= 1u << xm; }
        if ((cr & 1) || (cr & 6) == 6) f |= 1u << 10;
    }
    (void)last2;
    for (int i = 0; i + 2 < n; i++) {
        int lo = p[i], hi = p[i];
        for (int j = i + 1; j < i + 3; j++) { if (p[j] < lo) lo = p[j]; if (p[j] > hi) hi = p[j]; }
        if (hi - lo != 2) continue;
        f |= 4;
        if (p[i] == lo + 2 && p[i + 2] == lo) f |= 16; else f |= 8;
        int cr = contract(i, 3, lo);
        if ((cr & 1) || (cr & 6) == 6) f |= 1u << 8;
    }
    // any proper interval of size >= 2
    for (int a = 0; a < n && !(f >> 9 & 1); a++) {
        int lo = p[a], hi = p[a];
        for (int b = a + 1; b < n; b++) {
            if (p[b] < lo) lo = p[b]; if (p[b] > hi) hi = p[b];
            if (b - a + 1 == n) break;
            if (hi - lo == b - a) {
                int cr = contract(a, b - a + 1, lo);
                if ((cr & 1) || (cr & 6) == 6) { f |= 1u << 9; break; }
            }
        }
    }
    R->flags |= f;
}

static void rec(int r, uint32_t usedDg, uint32_t usedC) {
    if (r == n) { leaf(usedDg); return; }
    for (int c = 0; c < n; c++) {
        if (usedC >> c & 1) continue;
        int m = c - r + n - 1;
        if (usedDg >> m & 1) continue;
        p[r] = c;
        rec(r + 1, usedDg | 1u << m, usedC | 1u << c);
    }
}

int main(int argc, char **argv) {
    n = atoi(argv[1]); M = 2 * n - 1;
    idx = malloc(sizeof(int) << M); memset(idx, -1, sizeof(int) << M);
    cap = 1024; recs = malloc(sizeof(Rec) * cap);
    rec(0, 0, 0);
    for (int i = 0; i < nrec; i++) {
        Rec *R = &recs[i];
        printf("%u %lld %u %u %u %u %u %u %u %u\n", R->mask, R->nwit, R->flags, R->W2, R->Wm, R->Wo, R->Wf, R->Wc, R->Wok, R->We);
    }
    fprintf(stderr, "n=%d realized D=%d\n", n, nrec);
    return 0;
}
