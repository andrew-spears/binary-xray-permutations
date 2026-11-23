// Restricted interface machine, subset construction (same machine as thin.py / ../universal/maya.py).
// Family T(a, b): (lambda | mu) with  #part sizes(lambda) <= a and #part sizes(mu) <= b,  or the same with lambda, mu swapped.
// (#part sizes = number of corners of the Young diagram; a = b = 99 gives the full machine.)
// Explores every legal prefix with slacks <= B (legal: e_{k+1} >= e_k - 1, slack >= 0, slack + (e-1) + ... + 1 <= B)
// and reports the first one after which no walk inside T survives.  Pruning (sound: fewer states and a smaller last
// letter only make a prefix harder): a set S' with last letter l' is skipped if a set S <= S' was already expanded at
// the same slack with last letter l <= l'.  Mode h: only S = S' is used (sets identified by a 128-bit hash).
// Usage: ./thin B a b [q] [h]        build: g++ -O2 -o thin thin.cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> P; typedef unsigned long long u64;
int B; vector<P> part; map<P, int> pid; vector<int> psize, pcorn; vector<vector<int>> addt;   // addt[p][u + len(p)]
void gen(int n, int mx, P &cur) { if (!n) { pid[cur] = part.size(); part.push_back(cur); return; }
    for (int k = min(n, mx); k >= 1; k--) { cur.push_back(k); gen(n - k, k, cur); cur.pop_back(); } }
int add(const P &lam, int u) {
    int L = lam.size();
    for (int h = max(u, 0); h <= u + L; h++) {
        int j = 0; for (int p : lam) if (p > h) j++;
        if (h - j == u) { P r; for (int i = 0; i < j; i++) if (lam[i] - 1) r.push_back(lam[i] - 1);
            if (h) r.push_back(h); for (int i = j; i < L; i++) r.push_back(lam[i]);
            auto it = pid.find(r); return it == pid.end() ? -1 : it->second; } }
    return -1; }
struct H { size_t operator()(const pair<u64, u64> &k) const { return k.first ^ (k.second * 0x9E3779B97F4A7C15ULL); } };
int main(int argc, char **argv) {
    B = atoi(argv[1]); int a = atoi(argv[2]), b = atoi(argv[3]); bool quiet = argc > 4, hashonly = argc > 5;
    for (int n = 0; n <= B; n++) { P c; gen(n, n, c); }
    int NP = part.size(); psize.resize(NP); pcorn.resize(NP); addt.resize(NP);
    for (int p = 0; p < NP; p++) { psize[p] = accumulate(part[p].begin(), part[p].end(), 0);
        pcorn[p] = set<int>(part[p].begin(), part[p].end()).size(); int L = part[p].size();
        for (int u = -L; u <= B - psize[p]; u++) addt[p].push_back(add(part[p], u)); }
    // states of T, by slack
    vector<vector<pair<int, int>>> lev(B + 1); unordered_map<u64, int> loc;
    for (int l = 0; l < NP; l++) for (int m = 0; m < NP; m++) if (psize[l] + psize[m] <= B)
        if ((pcorn[l] <= a && pcorn[m] <= b) || (pcorn[l] <= b && pcorn[m] <= a)) {
            int s = psize[l] + psize[m]; loc[(u64)l * NP + m] = lev[s].size(); lev[s].push_back({l, m}); }
    if (!quiet) { printf("T(%d,%d), B = %d.  states per slack:", a, b, B); for (int s = 0; s <= B; s++) printf(" %zu", lev[s].size()); printf("\n"); }
    // transitions: tr[s][e + s][i] = successors (indices in level s + e)
    vector<vector<vector<vector<int>>>> tr(B + 1);
    for (int s = 0; s <= B; s++) { tr[s].assign(B + 1, {});
        for (int e = -s; e <= B - s; e++) { auto &t = tr[s][e + s]; t.resize(lev[s].size());
            for (size_t i = 0; i < lev[s].size(); i++) { int l = lev[s][i].first, m = lev[s][i].second, Ll = part[l].size(), Lm = part[m].size();
                for (int u = -Ll; u <= min(B - psize[l], e + Lm); u++) { int v = e - u; if (v > B - psize[m]) continue;
                    int x = addt[l][u + Ll]; if (x < 0) continue; int y = addt[m][v + Lm]; if (y < 0) continue;
                    auto it = loc.find((u64)x * NP + y); if (it != loc.end()) t[i].push_back(it->second); } } } }
    vector<int> W(B + 1); vector<vector<u64>> zob(B + 1), zob2(B + 1); mt19937_64 rng(12345);
    for (int s = 0; s <= B; s++) { W[s] = (lev[s].size() + 63) / 64; for (size_t i = 0; i < lev[s].size(); i++) { zob[s].push_back(rng()); zob2[s].push_back(rng()); } }
    unordered_map<pair<u64, u64>, signed char, H> seen;
    struct Item { vector<u64> S; int last, sl, depth; };
    vector<Item> st; st.push_back({vector<u64>(1, 1), -100, 0, 0}); vector<int> path; long long nd = 0; size_t big = 0;
    struct St { vector<u64> S; int last; }; vector<vector<St>> stored(B + 1); vector<vector<vector<int>>> reg(B + 1);
    for (int s = 0; s <= B; s++) reg[s].resize(lev[s].size());
    while (!st.empty()) {
        Item it = move(st.back()); st.pop_back(); path.resize(it.depth); if (it.depth) path[it.depth - 1] = it.last;
        int s = it.sl; u64 h1 = s * 1000003ULL, h2 = s; size_t cnt = 0; vector<int> mem;
        for (int w = 0; w < W[s]; w++) { u64 x = it.S[w]; while (x) { int i = w * 64 + __builtin_ctzll(x); x &= x - 1; mem.push_back(i); h1 ^= zob[s][i]; h2 += zob2[s][i]; } }
        auto f = seen.find({h1, h2});
        if (f != seen.end() && f->second <= it.last) continue;
        if (!hashonly) { bool dom = false;
            for (int i : mem) { for (int k : reg[s][i]) { St &q = stored[s][k]; if (q.last > it.last) continue; bool sub = true;
                    for (int w = 0; w < W[s]; w++) if (q.S[w] & ~it.S[w]) { sub = false; break; }
                    if (sub) { dom = true; break; } }
                if (dom) break; }
            if (dom) continue;
            int piv = mem[0]; for (int i : mem) if (reg[s][i].size() < reg[s][piv].size()) piv = i;
            reg[s][piv].push_back(stored[s].size()); stored[s].push_back({it.S, it.last}); }
        seen[{h1, h2}] = it.last; nd++; big = max(big, mem.size());
        vector<Item> kids;
        int lo = it.last == -100 ? -s : max(-s, it.last - 1);
        for (int e = B - s; e >= lo; e--) { if (e > 0 && s + e + e * (e - 1) / 2 > B) continue;
            vector<u64> R(W[s + e], 0); bool any = false; auto &t = tr[s][e + s];
            for (int i : mem) for (int j : t[i]) { R[j >> 6] |= 1ULL << (j & 63); any = true; }
            if (!any) { printf("T(%d,%d) REJECTS at B = %d:", a, b, B); for (int x : path) printf(" %d", x); printf(" %d\n", e); return 1; }
            kids.push_back({move(R), e, s + e, it.depth + 1}); }
        auto pc = [](const Item &x) { long long c = 0; for (u64 w : x.S) c += __builtin_popcountll(w); return c; };
        stable_sort(kids.begin(), kids.end(), [&](const Item &x, const Item &y) { return pc(x) > pc(y); });   // smallest set is expanded first
        for (auto &k : kids) st.push_back(move(k)); }
    long long tot = 0; for (int s = 0; s <= B; s++) tot += lev[s].size();
    printf("T(%d,%d) accepts every valid word with slacks <= %d   (%lld states, %lld sets explored, largest %zu)\n", a, b, B, tot, nd, big);
}
