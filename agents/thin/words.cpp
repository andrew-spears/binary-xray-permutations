// Every valid word with at most N letters (= every valid set of n <= N diagonals), NO slack bound, on the interface
// machine restricted to T(a, b) = { (lambda | mu) : #part sizes <= a and <= b in some order }  (same step as thin.cpp).
// Depth-first over prefixes that can still be completed within N letters; a prefix whose restricted set is empty
// is a valid word with no walk inside T(a, b).  A set reached again with the same last letter and no more letters
// left than before is skipped (128-bit hash).
// Usage: ./words N a b        build: g++ -O2 -o words words.cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> P; typedef unsigned long long u64;
int N, A_, B_;
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
        if ((pcorn[x] <= A_ && pcorn[y] <= B_) || (pcorn[x] <= B_ && pcorn[y] <= A_)) out.push_back(gets(x, y)); }
    return trm[k] = out; }
map<tuple<int, int, int>, bool> finm;
bool fin(int s, int l, int m) {                                 // can slack s after last letter l return to 0 within m letters
    if (s == 0) return true; if (m == 0) return false;
    auto k = make_tuple(s, l, m); auto it = finm.find(k); if (it != finm.end()) return it->second;
    bool r = false; for (int e = max(l - 1, -s); e <= max(l - 1, 0) && !r; e++) r = fin(s + e, e, m - 1);   // lower letters only help
    return finm[k] = r; }
struct H { size_t operator()(const pair<u64, u64> &k) const { return k.first ^ (k.second * 0x9E3779B97F4A7C15ULL); } };
unordered_map<pair<u64, u64>, int, H> seen; long long nodes = 0; size_t big = 0; int maxslack = 0; vector<int> path;
bool dfs(const vector<int> &S, int last, int s, int k) {       // false = rejected
    u64 h1 = (u64)(last + 100) * 1000003ULL, h2 = last; for (int i : S) { h1 ^= z1[i]; h2 += z2[i]; }
    auto f = seen.find({h1, h2}); if (f != seen.end() && f->second >= N - k) return true; seen[{h1, h2}] = N - k;
    nodes++; big = max(big, S.size()); maxslack = max(maxslack, s);
    for (int e = (k ? max(last - 1, -s) : 0); ; e++) {
        if (!fin(s + e, e, N - k - 1)) { if (e > 0) break; else continue; }
        vector<int> R; for (int i : S) { const vector<int> &t = tr(i, e); R.insert(R.end(), t.begin(), t.end()); }
        sort(R.begin(), R.end()); R.erase(unique(R.begin(), R.end()), R.end());
        path.push_back(e);
        if (R.empty()) { printf("T(%d,%d) REJECTS (N = %d):", A_, B_, N); for (int x : path) printf(" %d", x); printf("   (slack %d)\n", s + e); return false; }
        if (s + e > 0 && !dfs(R, e, s + e, k + 1)) return false;
        path.pop_back(); }
    return true; }
int main(int argc, char **argv) {
    N = atoi(argv[1]); A_ = atoi(argv[2]); B_ = atoi(argv[3]);
    vector<int> S0(1, gets(getp(P()), getp(P())));
    if (dfs(S0, 0, 0, 0)) printf("T(%d,%d): every valid word with <= %d letters has a walk   (%lld prefixes, largest slack %d, largest set %zu, %zu states touched)\n",
        A_, B_, N, nodes, maxslack, big, states.size());
}
