// Word-dependent thin family: after a prefix with r descending runs (r = 1 + #{k : e_{k+1} >= e_k}) only states
// (lambda | mu) with  #part sizes(lambda) + #part sizes(mu) <= r + c  are kept (same step as words.cpp).
// ./dyn N c      every valid word with at most N letters (depth-first; a set seen again with the same last letter,
//                at most as many runs and no more letters left is skipped)
// ./dyn - c      words on stdin, one per line
// build: g++ -O2 -o dyn dyn.cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> P; typedef unsigned long long u64;
int N, C_;
map<P, int> pid; vector<P> part; vector<int> pcorn;
int getp(const P &p) { auto it = pid.find(p); if (it != pid.end()) return it->second; pid[p] = part.size(); part.push_back(p);
    pcorn.push_back(set<int>(p.begin(), p.end()).size()); return part.size() - 1; }
map<pair<int, int>, int> addm;                                  // (pid, u) -> pid or -1
int add(int p, int u) {
    auto it = addm.find({p, u}); if (it != addm.end()) return it->second;
    P lam = part[p]; int L = lam.size(), res = -1;              // copy: getp may reallocate part
    for (int h = max(u, 0); h <= u + L; h++) { int j = 0; for (int x : lam) if (x > h) j++;
        if (h - j == u) { P r; for (int i = 0; i < j; i++) if (lam[i] - 1) r.push_back(lam[i] - 1);
            if (h) r.push_back(h); for (int i = j; i < L; i++) r.push_back(lam[i]); res = getp(r); break; } }
    return addm[{p, u}] = res; }
struct St { int l, m; }; vector<St> states; unordered_map<u64, int> sid; vector<u64> z1, z2; mt19937_64 rng(777);
int gets(int l, int m) { u64 k = ((u64)l << 32) | (unsigned)m; auto it = sid.find(k); if (it != sid.end()) return it->second;
    sid[k] = states.size(); states.push_back({l, m}); z1.push_back(rng()); z2.push_back(rng()); return states.size() - 1; }
unordered_map<u64, vector<int>> trm;
const vector<int> &tr(int s, int e) {
    u64 k = ((u64)s << 8) | (unsigned)(e + 100); auto it = trm.find(k); if (it != trm.end()) return it->second;
    vector<int> out; int l = states[s].l, m = states[s].m, Ll = part[l].size(), Lm = part[m].size();
    for (int u = -Ll; u <= e + Lm; u++) { int x = add(l, u); if (x < 0) continue; int y = add(m, e - u); if (y < 0) continue;
        out.push_back(gets(x, y)); }
    return trm[k] = out; }
map<tuple<int, int, int>, bool> finm;
bool fin(int s, int l, int m) {                                 // can slack s after last letter l return to 0 within m letters
    if (s == 0) return true; if (m == 0) return false;
    auto k = make_tuple(s, l, m); auto it = finm.find(k); if (it != finm.end()) return it->second;
    bool r = false; for (int e = max(l - 1, -s); e <= max(l - 1, 0) && !r; e++) r = fin(s + e, e, m - 1);   // lower letters only help
    return finm[k] = r; }

int corn(int i) { return pcorn[states[i].l] + pcorn[states[i].m]; }
vector<int> stepc(const vector<int> &S, int e, int cap) {
    vector<int> R; for (int i : S) for (int t : tr(i, e)) if (corn(t) <= cap) R.push_back(t);
    sort(R.begin(), R.end()); R.erase(unique(R.begin(), R.end()), R.end()); return R; }
struct H { size_t operator()(const pair<u64, u64> &k) const { return k.first ^ (k.second * 0x9E3779B97F4A7C15ULL); } };
unordered_map<pair<u64, u64>, pair<int, int>, H> seen; long long nodes = 0; size_t big = 0; int maxslack = 0; vector<int> path;
bool dfs(const vector<int> &S, int last, int s, int k, int r) {       // false = rejected
    u64 h1 = (u64)(last + 100) * 1000003ULL, h2 = last; for (int i : S) { h1 ^= z1[i]; h2 += z2[i]; }
    auto f = seen.find({h1, h2}); if (f != seen.end() && f->second.first >= N - k && f->second.second <= r) return true; seen[{h1, h2}] = {N - k, r};
    nodes++; big = max(big, S.size()); maxslack = max(maxslack, s);
    for (int e = (k ? max(last - 1, -s) : 0); ; e++) {
        if (!fin(s + e, e, N - k - 1)) { if (e > 0) break; else continue; }
        int r2 = (k == 0) ? 1 : r + (e >= last);
        vector<int> R = stepc(S, e, r2 + C_);
        path.push_back(e);
        if (R.empty()) { printf("corners <= runs + %d REJECTS (N = %d):", C_, N); for (int x : path) printf(" %d", x); printf("   (slack %d)\n", s + e); return false; }
        if (s + e > 0 && !dfs(R, e, s + e, k + 1, r2)) return false;
        path.pop_back(); }
    return true; }
int main(int argc, char **argv) {
    C_ = atoi(argv[2]); vector<int> S0(1, gets(getp(P()), getp(P())));
    if (string(argv[1]) == "-") { string line; while (getline(cin, line)) { istringstream is(line); vector<int> w; int e; while (is >> e) w.push_back(e); if (w.empty()) continue;
            vector<int> S = S0; int r = 0, top = 0, sl = 0; size_t bg = 0; bool ok = true;
            for (size_t k = 0; k < w.size() && ok; k++) { r = k ? r + (w[k] >= w[k - 1]) : 1; S = stepc(S, w[k], r + C_); bg = max(bg, S.size()); sl += w[k]; top = max(top, sl); ok = !S.empty(); }
            printf("%s  (%zu letters, slack %d, %d runs, largest set %zu):", ok ? "walk" : "NO WALK", w.size(), top, r, bg); for (int e2 : w) printf(" %d", e2); printf("\n"); }
        return 0; }
    N = atoi(argv[1]);
    if (dfs(S0, 0, 0, 0, 0)) printf("corners <= runs + %d: every valid word with <= %d letters has a walk   (%lld prefixes, largest slack %d, largest set %zu, %zu states touched)\n",
        C_, N, nodes, maxslack, big, states.size());
}
