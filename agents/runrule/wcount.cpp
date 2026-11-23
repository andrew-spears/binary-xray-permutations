// Word-level test of a rule u -> v behind a given prefix x, with multiplicity:
// for every continuation y (length <= Ly, slacks <= B, legal after both x u and x v) that closes the word,
// compare N(x u y) and N(x v y), the numbers of permutation matrices with these diagonal words.
// Same interface machine as rules.cpp.  Usage: ./wcount B Ly < cases.txt     cases.txt: "name : x | u | v" per line
#include <bits/stdc++.h>
using namespace std;
typedef uint64_t u64; typedef unsigned __int128 big;
int B, W, Ly;
struct St { u64 r, c; bool operator==(const St& o) const { return r == o.r && c == o.c; } };
struct StH { size_t operator()(const St& s) const { return s.r * 0x9E3779B97F4A7C15ULL ^ (s.c + 0x7F4A7C15ULL) * 0xC2B2AE3D27D4EB4FULL; } };
vector<St> states; vector<int> slk, lidx, thr; vector<vector<int>> lvl; vector<int> succ; vector<long> off;
unordered_map<St, int, StH> sid;
typedef vector<pair<int, big>> Vec;                 // sparse counts: (state id, count), all of one slack
Vec step(const Vec& A, int e, vector<big>& tmp) {
    Vec out; if (A.empty()) return out; int s2 = slk[A[0].first] + e; vector<int> touched;
    for (auto& p : A) { long o = (long)p.first * W + (e + B);
        for (long k = off[o]; k < off[o + 1]; k++) { int t = lvl[s2][succ[k]]; if (thr[t] < e) continue; if (!tmp[t]) touched.push_back(t); tmp[t] += p.second; } }
    for (int t : touched) { out.push_back({t, tmp[t]}); tmp[t] = 0; }
    return out;
}
long tested, viol; double minratio; vector<int> worst, cur;
void dfs(const Vec& A, const Vec& V, int s, int last, int depth, vector<big>& tmp) {
    if (A.empty()) return;                         // N(x u y ...) = 0 from here on
    if (s == 0) { big a = A[0].second, v = V.empty() ? 0 : V[0].second; tested++; if (a > v) viol++;
        double r = (double)v / (double)a; if (r < minratio) { minratio = r; worst = cur; } }
    if (depth == Ly) return;
    for (int e = max(-s, last - 1); e <= B - s; e++) { cur.push_back(e); dfs(step(A, e, tmp), step(V, e, tmp), s + e, e, depth + 1, tmp); cur.pop_back(); }
}
int main(int argc, char** argv) {
    B = atoi(argv[1]); Ly = atoi(argv[2]); W = 2 * B + 1; u64 base = (1ULL << B) - 1;
    states.push_back({base, base}); slk.push_back(0); sid[states[0]] = 0; lvl.assign(B + 1, {}); lidx.push_back(0); lvl[0].push_back(0);
    for (size_t i = 0; i < states.size(); i++) {
        St st = states[i]; int s = slk[i];
        for (int e = -B; e <= B; e++) {
            off.push_back(succ.size());
            if (s + e < 0 || s + e > B) continue;
            for (int u = -B; u <= B; u++) {
                int v = e - u; if (v < -B || v > B) continue;
                if (st.r >> (B + u) & 1) continue; if (st.c >> (B + v) & 1) continue;
                u64 r2 = st.r | (1ULL << (B + u)), c2 = st.c | (1ULL << (B + v));
                if (!(r2 & 1) || !(c2 & 1)) continue;
                St t{r2 >> 1, c2 >> 1}; auto it = sid.find(t); int id;
                if (it == sid.end()) { id = states.size(); sid[t] = id; states.push_back(t); slk.push_back(s + e); lidx.push_back(lvl[s + e].size()); lvl[s + e].push_back(id); }
                else id = it->second;
                succ.push_back(lidx[id]);
            }
        }
    }
    off.push_back(succ.size());
    thr.assign(states.size(), INT_MIN); thr[0] = INT_MAX;      // live states, as in rules.cpp
    for (bool ch = true; ch;) { ch = false;
        for (size_t g = 1; g < states.size(); g++) for (int e = B - slk[g]; e >= -slk[g] && e + 1 > thr[g]; e--) {
            long o = (long)g * W + (e + B); bool ok = false;
            for (long k = off[o]; k < off[o + 1] && !ok; k++) ok = thr[lvl[slk[g] + e][succ[k]]] >= e;
            if (ok) { thr[g] = e + 1; ch = true; break; }
        } }
    vector<big> tmp(states.size(), 0); string line;
    while (getline(cin, line)) {
        size_t c = line.find(':'), b1 = line.find('|'), b2 = line.rfind('|'); if (c == string::npos || b1 == string::npos || b1 == b2) continue;
        vector<int> x, u, v; int t;
        { istringstream a(line.substr(c + 1, b1 - c - 1)); while (a >> t) x.push_back(t); }
        { istringstream a(line.substr(b1 + 1, b2 - b1 - 1)); while (a >> t) u.push_back(t); }
        { istringstream a(line.substr(b2 + 1)); while (a >> t) v.push_back(t); }
        Vec A{{0, 1}}; int s = 0; for (int e : x) { A = step(A, e, tmp); s += e; }
        Vec V = A; int su = s, sv = s; for (int e : u) { A = step(A, e, tmp); su += e; } for (int e : v) { V = step(V, e, tmp); sv += e; }
        set<int> inV; for (auto& p : V) inV.insert(p.first); int missing = 0; for (auto& p : A) missing += !inV.count(p.first);
        tested = viol = 0; minratio = 1e300; worst.clear(); cur.clear();
        dfs(A, V, su, u.empty() ? x.back() : u.back(), 0, tmp);
        printf("%s x =", line.substr(0, c).c_str()); for (int e : x) printf(" %d", e);
        printf(": live states of F(xu) missing from F(xv): %d; continuations y tested %ld; N(xuy) > N(xvy): %ld; least N(xvy)/N(xuy) = %.3f at y =", missing, tested, viol, minratio);
        for (int e : worst) printf(" %d", e); printf("\n"); fflush(stdout);
    }
}
