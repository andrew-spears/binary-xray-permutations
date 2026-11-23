// E-splits (extreme-term splits).  S-word w_j = e_k + 2 #(S^c before k), S^c-word (read backwards) -e_k + 2 #(S after k), both >= 0.
// theta(w): rows of lengths w_j, row j starting in column j.  rho = row lengths, kappa = column lengths (as partitions).
// By Lemma R the state (lam|gam) has an odd count for S if lam + gam = rho_1 or lam' + gam' = kappa_1, and for S^c if
// lam' + gam' = rho_2 or lam + gam = kappa_2.  S is an E-split if some state is odd for both by these rules:
//   RC: rho_1 = kappa_2;  CR: kappa_1 = rho_2;  RR: lam + gam = rho_1, lam u gam = rho_2';  CC: mu + nu = kappa_1, mu u nu = kappa_2'.
// H-split = RR with gam empty.   Usage: ./esplit n [uni] [v]   words without a tight cut; v lists the words without an E-split
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> P;
int n; bool uni, verbose, onlyRR; long goodRR = 0; long tot = 0, good = 0, goodH = 0; vector<int> e;
P conj(const P& p) { P c; if (p.empty()) return c; for (int i = 1; i <= p[0]; i++) { int k = 0; while (k < (int)p.size() && p[k] >= i) k++; c.push_back(k); } return c; }
P rows(const vector<int>& w) { P r; for (int x : w) if (x) r.push_back(x); sort(r.begin(), r.end(), greater<int>()); return r; }
P cols(const vector<int>& w) { map<int,int> c; for (int i = 0; i < (int)w.size(); i++) for (int j = i; j < i + w[i]; j++) c[j]++; P r; for (auto& q : c) r.push_back(q.second); sort(r.begin(), r.end(), greater<int>()); return r; }
// is there lam, gam with lam + gam = sum_ and lam u gam = uni_ ?
bool dfs(const P& s, size_t i, int la, int ga, map<int,int>& cnt, int left) {
    if (i == s.size()) return left == 0;
    for (int a = min(la, s[i]); 2 * a >= s[i]; a--) { int b = s[i] - a; if (b > ga) continue;   // a >= b on this row; try both orders
        for (int sw = 0; sw < 2; sw++) { int x = sw ? b : a, y = sw ? a : b; if (sw && a == b) break; if (x > la || y > ga) continue;
            auto ix = cnt.find(x); if (ix == cnt.end() || !ix->second) continue; ix->second--;
            bool ok = true; if (y) { auto iy = cnt.find(y); if (iy == cnt.end() || !iy->second) ok = false; else iy->second--; }
            if (ok && dfs(s, i + 1, x, y, cnt, left - 1 - (y > 0))) return true;
            if (ok && y) cnt[y]++; cnt[x]++; } }
    return false;
}
bool splits(const P& un, const P& sm) {
    if (accumulate(un.begin(), un.end(), 0) != accumulate(sm.begin(), sm.end(), 0)) return false;
    if (un.size() < sm.size() || un.size() > 2 * sm.size()) return false;
    map<int,int> cnt; for (int x : un) cnt[x]++; return dfs(sm, 0, 1 << 20, 1 << 20, cnt, un.size());
}
int test(int S) {   // 0 none, 1 E-split, 2 RR-split, 3 H-split
    vector<int> w1, w2; int a = 0, b = 0;
    for (int k = 0; k < n; k++) { if (S >> k & 1) { int x = e[k] + 2 * a; if (x < 0) return 0; w1.push_back(x); } else a++; }
    for (int k = n - 1; k >= 0; k--) { if (S >> k & 1) b++; else { int x = -e[k] + 2 * b; if (x < 0) return 0; w2.push_back(x); } }
    P r1 = rows(w1), r2 = rows(w2); if (conj(r1) == r2) return 3;
    if (splits(conj(r2), r1)) return 2;
    if (onlyRR) return 0;
    P k1 = cols(w1), k2 = cols(w2);
    if (r1 == k2 || k1 == r2 || splits(conj(k2), k1)) return 1;
    return 0;
}
void rec(int k, int sl, bool down) {
    if (k == n) { if (sl) return; tot++; int best = 0;
        for (int S = 1; S < (1 << n) - 1 && best < 3; S++) best = max(best, test(S));
        if (best == 1) { onlyRR = true; for (int S = 1; S < (1 << n) - 1 && best < 2; S++) best = max(best, test(S)); onlyRR = false; if (best == 1 && verbose) { printf("  no RR-split:"); for (int x : e) printf(" %d", x); printf("\n"); } }
        good += best > 0; goodRR += best >= 2; goodH += best == 3;
        if (!best && verbose) { printf("  no E-split:"); for (int x : e) printf(" %d", x); printf("\n"); }
        return; }
    int lo = k ? e[k - 1] - 1 : 1;
    for (int x = max(lo, -sl); x <= n; x++) {
        int s2 = sl + x; if (k < n - 1 && s2 <= 0) continue; if (uni && down && x > 0) continue;
        if (s2 > (n - 1 - k) * (n - k) / 2 - (n - 1 - k) * x) break;
        e[k] = x; rec(k + 1, s2, down || x < 0); }
}
int main(int argc, char** argv) {
    if (!strcmp(argv[1], "w")) {   // one word: ./esplit w e_1 ... e_n   counts S of each kind
        n = argc - 2; e.resize(n); for (int i = 0; i < n; i++) e[i] = atoi(argv[i + 2]); long c[4] = {0, 0, 0, 0}; int first = 0;
        for (int S = 1; S < (1 << n) - 1; S++) { int t = test(S); c[t]++; if (t >= 2 && !first) first = S; }
        printf("n = %d: S with H %ld, RR not H %ld, only RC/CR/CC %ld; first RR-split S = ", n, c[3], c[2], c[1]);
        for (int k = 0; k < n; k++) putchar(first >> k & 1 ? 'S' : '.'); printf("\n"); return 0; }
    if (!strcmp(argv[1], "m")) {   // ./esplit m n [uni] [v]: least |S| of an RR-split against ceil(max|e| / 2)
        n = atoi(argv[2]); uni = argc > 3 && !strcmp(argv[3], "uni"); bool vv = !strcmp(argv[argc - 1], "v"); e.resize(n); onlyRR = true; map<pair<int,int>, long> H;
        vector<int> order; for (int S = 1; S < (1 << n) - 1; S++) order.push_back(S);
        stable_sort(order.begin(), order.end(), [](int a, int b) { return __builtin_popcount(a) < __builtin_popcount(b); });
        function<void(int,int,bool)> go = [&](int k, int sl, bool down) {
            if (k == n) { if (sl) return; int M = 0; for (int x : e) M = max(M, abs(x)); int best = 0, bs = 0;
                for (int S : order) if (test(S)) { best = __builtin_popcount(S); bs = S; break; }
                H[{(M + 1) / 2, best}]++;
                if (vv && best != (M + 1) / 2) { printf("  "); for (int x : e) printf(" %d", x); printf("   least |S| = %d: ", best); for (int i = 0; i < n; i++) putchar(bs >> i & 1 ? 'S' : '.'); printf("\n"); }
                return; }
            int lo = k ? e[k - 1] - 1 : 1;
            for (int x = max(lo, -sl); x <= n; x++) { int s2 = sl + x; if (k < n - 1 && s2 <= 0) continue; if (uni && down && x > 0) continue;
                if (s2 > (n - 1 - k) * (n - k) / 2 - (n - 1 - k) * x) break; e[k] = x; go(k + 1, s2, down || x < 0); } };
        go(0, 0, false); printf("n = %d (%s, no tight cut): (ceil(max|e|/2), least |S| of an RR-split, 0 = none) -> words:", n, uni ? "unimodal" : "all valid");
        for (auto& q : H) printf("  (%d,%d): %ld", q.first.first, q.first.second, q.second); printf("\n"); return 0; }
    n = atoi(argv[1]); for (int i = 2; i < argc; i++) { if (!strcmp(argv[i], "uni")) uni = true; if (!strcmp(argv[i], "v")) verbose = true; }
    e.resize(n); rec(0, 0, false);
    printf("n = %d, %s words without a tight cut: %ld; with an E-split: %ld; with an RR-split: %ld; with an H-split: %ld\n", n, uni ? "unimodal" : "all valid", tot, good, goodRR, goodH);
}
