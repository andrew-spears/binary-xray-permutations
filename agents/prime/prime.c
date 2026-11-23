// prime.c: for each valid D of size n, enumerate witnesses.
// Tight-cut D: only check a witness exists.  No-tight-cut, mirror-canonical D:
// enumerate witnesses, classify each as simple or not (skeleton size), stop early
// once a direct-sum witness (skeleton 2) is found.
// Output (stdout), one line per canonical no-tight-cut D:
//   D: d1 d2 ... | nwit_seen nsimple_seen minskel complete
// minskel = 0 means every witness is simple (=> prime).  complete=1 if all witnesses enumerated.
// Prime lines also list all witnesses (n<=9) after "W:".
// stderr: summary.  Usage: ./prime n
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int n, D[16], p[16];
long long nwit, nsimp; int minskel; int stop_early; int want_list;
char wl[1 << 20]; int wlen;

// skeleton size of p: 1 = simple (no proper interval of size>=2); else size of simple
// skeleton (2 for direct/skew sum).
int skeleton(void) {
    // direct sum / skew sum
    int mx = -1, mn = 99;
    for (int j = 0; j < n - 1; j++) {
        if (p[j] > mx) mx = p[j];
        if (p[j] < mn) mn = p[j];
        if (mx == j) return 2;
        if (mn == n - 1 - j) return 2;
    }
    // maximal proper intervals
    static int isint[16][16];
    int any = 0;
    for (int a = 0; a < n; a++) {
        int lo = p[a], hi = p[a];
        for (int b = a; b < n; b++) {
            if (p[b] < lo) lo = p[b];
            if (p[b] > hi) hi = p[b];
            isint[a][b] = (hi - lo == b - a) && !(a == 0 && b == n - 1);
            if (isint[a][b] && b > a) any = 1;
        }
    }
    if (!any) return 1;
    // count maximal intervals: greedy from left, take longest interval starting at a
    int k = 0, a = 0;
    while (a < n) {
        int best = a;
        for (int b = n - 1; b >= a; b--) if (isint[a][b]) { best = b; break; }
        k++; a = best + 1;
    }
    return k;
}

int found;
void rec(int i, int usedD, int usedC) {
    if (stop_early) return;
    if (i == n) {
        nwit++;
        if (found == -1) { stop_early = 1; return; } // existence-only mode
        int s = skeleton();
        if (s == 1) {
            nsimp++;
            if (want_list && wlen < (1 << 20) - 64) {
                for (int j = 0; j < n; j++) wlen += sprintf(wl + wlen, "%x", p[j] + 1 > 9 ? p[j] + 1 : p[j] + 1);
                wl[wlen++] = ' ';
            }
        } else {
            if (minskel == 0 || s < minskel) minskel = s;
            if (s == 2) stop_early = 1;
        }
        return;
    }
    for (int j = 0; j < n; j++) {
        if (usedD >> j & 1) continue;
        int c = i + D[j];
        if (c < 0 || c >= n || (usedC >> c & 1)) continue;
        p[i] = c;
        rec(i + 1, usedD | 1 << j, usedC | 1 << c);
        if (stop_early) return;
    }
}

long long cnt_valid, cnt_nowit, cnt_nt, cnt_prime, cnt_dec, skelhist[20], cnt_incomplete;
int cur[16];
void enumD(int k, int prev, int t) {
    if (k == n) {
        if (t != n * (n - 1) / 2) return;
        memcpy(D, cur, sizeof(int) * n);
        cnt_valid++;
        // tight cut?
        int tt = 0, tight = 0;
        for (int i = 0; i < n - 1; i++) { tt += D[i] + n - (i + 1); if (tt == (i + 1) * i / 2) tight = 1; }
        // canonical: D <= sorted(-D)
        int cmp = 0;
        for (int i = 0; i < n && !cmp; i++) { int m = -D[n - 1 - i]; if (D[i] != m) cmp = D[i] < m ? -1 : 1; }
        if (tight || cmp > 0) {
            // existence check
            nwit = 0; stop_early = 0; found = -1; rec(0, 0, 0);
            if (!nwit) { cnt_nowit++; fprintf(stderr, "NO WITNESS:"); for (int i = 0; i < n; i++) fprintf(stderr, " %d", D[i]); fprintf(stderr, "\n"); }
            return;
        }
        cnt_nt++;
        nwit = nsimp = 0; minskel = 0; stop_early = 0; found = 0; wlen = 0; want_list = (n <= 9);
        rec(0, 0, 0);
        if (!nwit) { cnt_nowit++; fprintf(stderr, "NO WITNESS:"); for (int i = 0; i < n; i++) fprintf(stderr, " %d", D[i]); fprintf(stderr, "\n"); }
        printf("D:");
        for (int i = 0; i < n; i++) printf(" %d", D[i]);
        printf(" | %lld %lld %d %d", nwit, nsimp, minskel, stop_early ? 0 : 1);
        if (minskel == 0 && nwit) {
            cnt_prime++;
            if (want_list) { wl[wlen] = 0; printf(" W: %s", wl); }
        } else cnt_dec++;
        skelhist[minskel]++;
        printf("\n");
        return;
    }
    for (int d = prev + 1; d < n; d++) {
        if (d + (n - k - 1) > n - 1) break;
        int t2 = t + d + n - (k + 1);
        if (t2 < (k + 1) * k / 2) continue;
        if (t2 > n * (n - 1) / 2) break;
        cur[k] = d;
        enumD(k + 1, d, t2);
    }
}

int main(int argc, char **argv) {
    n = atoi(argv[1]);
    enumD(0, -n, 0);
    fprintf(stderr, "n=%d valid=%lld nowitness=%lld noTight(mirror)=%lld decomposable=%lld prime=%lld\n",
            n, cnt_valid, cnt_nowit, cnt_nt, cnt_dec, cnt_prime);
    fprintf(stderr, "minskel histogram:");
    for (int i = 0; i < 20; i++) if (skelhist[i]) fprintf(stderr, " [%d]=%lld", i, skelhist[i]);
    fprintf(stderr, "\n");
    return 0;
}
