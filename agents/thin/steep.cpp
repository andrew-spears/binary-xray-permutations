// Random steep words x 0^z y~ on the interface machine restricted to T(a, b) (same step as words.cpp):
// x, y = products of at most R descending runs of letters in 1..M, last run ending at 1, equal sums (y = x half the time),
// y~ = reverse of -y, z in {1, 2}.  Prints every word with no walk inside T(a, b).  Words can also be given on stdin
// (one per line) with  ./steep a b -.
// Usage: ./steep a b seed count R M        build: g++ -O2 -o steep steep.cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> P; typedef unsigned long long u64;
int A_, B_;
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

bool walk(const vector<int> &w, size_t &big) {
    vector<int> S(1, gets(getp(P()), getp(P())));
    for (int e : w) { vector<int> R; for (int i : S) { const vector<int> &t = tr(i, e); R.insert(R.end(), t.begin(), t.end()); }
        sort(R.begin(), R.end()); R.erase(unique(R.begin(), R.end()), R.end()); S.swap(R); big = max(big, S.size()); if (S.empty()) return false; }
    return true; }
mt19937 g;
vector<int> half(int R, int M) {
    vector<int> x; int r = 1 + g() % R, lo = 1;
    for (int i = 0; i < r; i++) { int a = lo + g() % (M - lo + 1), b = (i == r - 1) ? 1 : 1 + g() % a;
        for (int e = a; e >= b; e--) x.push_back(e); lo = b; }
    return x; }
int main(int argc, char **argv) {
    A_ = atoi(argv[1]); B_ = atoi(argv[2]); size_t big = 0; long long n = 0, bad = 0; int top = 0, len = 0;
    auto test = [&](const vector<int> &w) { int v = 0; for (size_t i = 0; i < w.size(); i++) { v += w[i]; if (v < 0 || (i && w[i] < w[i - 1] - 1)) v = -1000000; }
        if (v) { printf("not a valid word, skipped\n"); return; } n++; len = max(len, (int)w.size()); int s = 0; for (int e : w) { s += e; top = max(top, s); }
        if (!walk(w, big)) { bad++; printf("NO WALK in T(%d,%d):", A_, B_); for (int e : w) printf(" %d", e); printf("\n"); fflush(stdout); }
        if (states.size() > 3000000) { trm.clear(); } };
    if (string(argv[3]) == "-") { string line; while (getline(cin, line)) { istringstream is(line); vector<int> w; int e; while (is >> e) w.push_back(e); if (w.size()) test(w); } }
    else { g.seed(atoi(argv[3])); long long cnt = atoll(argv[4]); int R = atoi(argv[5]), M = atoi(argv[6]);
        while (n < cnt) { vector<int> x = half(R, M), y = x; int sx = accumulate(x.begin(), x.end(), 0);
            if (g() % 2) for (int t = 0; t < 300; t++) { vector<int> c = half(R, M); if (accumulate(c.begin(), c.end(), 0) == sx) { y = c; break; } }
            vector<int> w = x; for (int z = 1 + g() % 2; z > 0; z--) w.push_back(0); for (int i = y.size() - 1; i >= 0; i--) w.push_back(-y[i]);
            test(w); } }
    printf("T(%d,%d): %lld words, longest %d letters, largest slack %d, largest set %zu, %lld without a walk\n", A_, B_, n, len, top, big, bad);
}
