// Fast check of rewrite rules u -> v on the interface machine (same model as ../interface/rewrite.py, run_rule.py),
// with reachable sets stored as bitsets over all interface states of the same slack, so bounds B > 16 fit in memory.
// A situation is (F(x), slack, last letter) over legal prefixes x with all slacks <= B (e_1 >= 0, drops <= 1, sums >= 0).
// A rule holds in a situation if F(xu) is a subset of F(xv) (both read legally with slacks <= B).
// Usage: ./rules B [dump.txt] < rules.txt     rules.txt: one rule per line  "name : u letters | v letters"
// Per rule: tested, fails, fails1 (situations where for some next letter z legal after both, F(xuz) is not inside
// F(xvz)), and the shortest failing prefixes (NEX=k: print k of them; FAST=1: stop each rule at its first failure, skip fails1 and examples).
// failsLive: situations where a missing state is live, i.e. can still be completed to a valid word (slacks <= B)
// by a continuation that is legal after x u.
// SIM=1: also failsSim, situations where a live missing state is not simulated by any state of F(xv).
// Also reports whether some legal prefix has an empty reachable set (none <=> every valid word with slacks <= B is
// solvable, for every n).  With dump.txt: the situation graph (id slack last size parent letter : letter>id ...).
#include <bits/stdc++.h>
using namespace std;
typedef uint64_t u64;
int B, W;                                    // W = 2B+1 letters
struct St { u64 r, c; bool operator==(const St& o) const { return r == o.r && c == o.c; } };
struct StH { size_t operator()(const St& s) const { return s.r * 0x9E3779B97F4A7C15ULL ^ (s.c + 0x7F4A7C15ULL) * 0xC2B2AE3D27D4EB4FULL; } };
vector<St> states; vector<int> slk, lidx; vector<vector<int>> lvl; vector<int> succ; vector<long> off;
unordered_map<St, int, StH> sid;
struct Sit { int s, last, par, pe; };
vector<Sit> sit; vector<vector<u64>> bits; vector<vector<int>> nxt; vector<int> cnt;
unordered_map<u64, vector<int>> seen;
u64 hashbits(const vector<u64>& b, int s, int last) { u64 h = 1469598103934665603ULL * (s + 7) + 1000003ULL * (last + 100); for (u64 x : b) { h ^= x; h *= 0x100000001B3ULL; h ^= h >> 29; } return h; }
int follow(int id, const vector<int>& w) { for (int e : w) { if (e < -B || e > B) return -1; id = nxt[id][e + B]; if (id < 0) return -1; } return id; }
vector<int> prefix(int id) { vector<int> w; for (; sit[id].par >= 0; id = sit[id].par) w.push_back(sit[id].pe); reverse(w.begin(), w.end()); return w; }
bool subset(int a, int b) { const auto &x = bits[a], &y = bits[b]; for (size_t i = 0; i < x.size(); i++) if (x[i] & ~y[i]) return false; return true; }
int main(int argc, char** argv) {
    bool FAST = getenv("FAST") != NULL; int NEX = getenv("NEX") ? atoi(getenv("NEX")) : 3;
    B = atoi(argv[1]); if (B < 1 || B > 31) { fprintf(stderr, "B must be 1..31\n"); return 1; }
    W = 2 * B + 1; u64 base = (1ULL << B) - 1;
    // 1. all interface states (closure of the start under every letter), with successor lists
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
    // 2. situations
    auto add = [&](vector<u64>&& b, int s, int last, int par, int pe) {
        u64 h = hashbits(b, s, last); auto& v = seen[h];
        for (int id : v) if (sit[id].s == s && sit[id].last == last && bits[id] == b) return id;
        int id = sit.size(); v.push_back(id); int c = 0; for (u64 x : b) c += __builtin_popcountll(x);
        sit.push_back({s, last, par, pe}); bits.push_back(move(b)); nxt.push_back(vector<int>(W, -1)); cnt.push_back(c); return id;
    };
    add(vector<u64>{1}, 0, INT_MIN, -1, 0);
    long empty = 0; int firstempty = -1;
    for (size_t i = 0; i < sit.size(); i++) {
        Sit cur = sit[i];
        int lo = cur.last == INT_MIN ? 0 : max(-cur.s, cur.last - 1);
        for (int e = lo; e <= B - cur.s; e++) {
            int s2 = cur.s + e; vector<u64> T((lvl[s2].size() + 63) / 64, 0);
            const vector<u64>& S = bits[i]; const vector<int>& L = lvl[cur.s];
            for (size_t w = 0; w < S.size(); w++) for (u64 x = S[w]; x; x &= x - 1) {
                int g = L[w * 64 + __builtin_ctzll(x)]; long o = (long)g * W + (e + B);
                for (long k = off[o]; k < off[o + 1]; k++) T[succ[k] >> 6] |= 1ULL << (succ[k] & 63);
            }
            size_t before = sit.size(); int id = add(move(T), s2, e, i, e); nxt[i][e + B] = id;
            if (sit.size() > before && cnt[id] == 0) { empty++; if (firstempty < 0) firstempty = id; }
        }
    }
    int mx = 0; for (int c : cnt) mx = max(mx, c);
    printf("B = %d: %zu interface states, %zu situations, largest set %d; legal prefixes with empty reachable set: %ld%s\n", B, states.size(), sit.size(), mx, empty, empty ? "" : "  (every valid word with slacks <= B is solvable)");
    if (firstempty >= 0) { printf("  first empty prefix:"); for (int e : prefix(firstempty)) printf(" %d", e); printf("\n"); }
    fflush(stdout);
    if (argc > 2) {
        FILE* f = fopen(argv[2], "w");
        for (size_t i = 0; i < sit.size(); i++) {
            fprintf(f, "%zu %d %d %d %d %d :", i, sit[i].s, sit[i].last == INT_MIN ? 99 : sit[i].last, cnt[i], sit[i].par, sit[i].pe);
            for (int e = -B; e <= B; e++) if (nxt[i][e + B] >= 0) fprintf(f, " %d>%d", e, nxt[i][e + B]);
            fprintf(f, "\n");
        }
        fclose(f);
    }
    // 3. live states: thr[g] = largest 'last letter' after which state g can still be completed to the empty
    //    interface by a legal continuation with slacks <= B (INT_MIN: never; the empty interface: always)
    vector<int> thr(states.size(), INT_MIN); thr[0] = INT_MAX;
    for (bool ch = true; ch;) { ch = false;
        for (size_t g = 1; g < states.size(); g++) for (int e = B - slk[g]; e >= -slk[g] && e + 1 > thr[g]; e--) {
            long o = (long)g * W + (e + B); bool ok = false;
            for (long k = off[o]; k < off[o + 1] && !ok; k++) ok = thr[lvl[slk[g] + e][succ[k]]] >= e;
            if (ok) { thr[g] = e + 1; ch = true; break; }
        } }
    auto liveMissing = [&](int a, int b, int last) { int d = 0; const vector<int>& L = lvl[sit[a].s];
        for (size_t w = 0; w < bits[a].size(); w++) for (u64 x = bits[a][w] & ~bits[b][w]; x; x &= x - 1) d += thr[L[w * 64 + __builtin_ctzll(x)]] >= last;
        return d; };
    // 4. (SIM=1) the largest simulation on interface states of equal slack: s <= t if every move s -e-> s' is matched
    //    by a move t -e-> t' with s' <= t'.  Then every word that completes s also completes t.
    bool SIM = getenv("SIM") != NULL; vector<vector<u64>> R(states.size());
    if (SIM) {
        for (size_t g = 0; g < states.size(); g++) { size_t m = lvl[slk[g]].size(); R[g].assign((m + 63) / 64, ~0ULL); if (m & 63) R[g].back() = (1ULL << (m & 63)) - 1; }
        for (bool ch = true; ch;) { ch = false;
            for (size_t g = 0; g < states.size(); g++) { int sl = slk[g]; const vector<int>& L = lvl[sl];
                for (size_t w = 0; w < R[g].size(); w++) for (u64 x = R[g][w]; x; x &= x - 1) {
                    int ti = w * 64 + __builtin_ctzll(x), t = L[ti]; if (t == (int)g) continue; bool ok = true;
                    for (int e = -sl; e <= B - sl && ok; e++) { long o = (long)g * W + (e + B), o2 = (long)t * W + (e + B);
                        for (long k = off[o]; k < off[o + 1] && ok; k++) { const vector<u64>& Rs = R[lvl[sl + e][succ[k]]]; bool f = false;
                            for (long k2 = off[o2]; k2 < off[o2 + 1] && !f; k2++) f = Rs[succ[k2] >> 6] >> (succ[k2] & 63) & 1;
                            ok = f; } }
                    if (!ok) { R[g][w] &= ~(1ULL << (ti & 63)); ch = true; }
                } } }
        long pairs = 0, lp = 0, ls = 0, nlive = 0;
        for (size_t g = 0; g < states.size(); g++) { int c = -1; for (u64 x : R[g]) c += __builtin_popcountll(x); pairs += c; if (thr[g] > INT_MIN) { nlive++; lp += c; ls += c > 0; } }
        long nt = 0; for (auto& st : states) nt += st.r != st.c;
        printf("simulation: %ld pairs s <= t with s != t (%ld of them with s live); %ld of %ld live states are simulated by another state; %ld states differ from their transpose (transposition is always a simulation)\n", pairs, lp, ls, nlive, nt);
    }
    // number of live missing states of F(a) \ F(b) that are not simulated by any state of F(b)
    auto simMissing = [&](int a, int b, int last) { int d = 0; const vector<int>& L = lvl[sit[a].s];
        for (size_t w = 0; w < bits[a].size(); w++) for (u64 x = bits[a][w] & ~bits[b][w]; x; x &= x - 1) { int g = L[w * 64 + __builtin_ctzll(x)];
            if (thr[g] < last) continue; bool f = false; for (size_t k = 0; k < R[g].size() && !f; k++) f = R[g][k] & bits[b][k]; d += !f; }
        return d; };
    string line; long tot = 0, totbad = 0, totlive = 0, totsim = 0;
    while (getline(cin, line)) {
        size_t c = line.find(':'), bar = line.find('|'); if (c == string::npos || bar == string::npos) continue;
        string name = line.substr(0, c); vector<int> u, v; int x;
        { istringstream a(line.substr(c + 1, bar - c - 1)); while (a >> x) u.push_back(x); }
        { istringstream a(line.substr(bar + 1)); while (a >> x) v.push_back(x); }
        long t = 0, bad = 0, bad1 = 0, badL = 0, badS = 0; vector<int> ex;
        for (size_t i = 0; i < sit.size(); i++) {
            int a = follow(i, u), b = follow(i, v); if (a < 0 || b < 0) continue;
            t++;
            if (!subset(a, b)) { bad++; if ((int)ex.size() < NEX) ex.push_back(i); if (FAST) break; }
            if (FAST) continue;
            if (!subset(a, b)) { badL += liveMissing(a, b, sit[a].last) > 0; if (SIM) badS += simMissing(a, b, sit[a].last) > 0; }
            bool f1 = false;
            for (int e = -B; e <= B && !f1; e++) { int a2 = nxt[a][e + B], b2 = nxt[b][e + B]; if (a2 >= 0 && b2 >= 0 && !subset(a2, b2)) f1 = true; }
            bad1 += f1;
        }
        if (!t) continue;
        tot += t; totbad += bad; totlive += badL; totsim += badS;
        if (FAST) printf("%s tested %ld fails %ld", name.c_str(), t, bad); else { printf("%s tested %ld fails %ld fails1 %ld failsLive %ld", name.c_str(), t, bad, bad1, badL); if (SIM) printf(" failsSim %ld", badS); }
        if (!FAST) for (int i : ex) {
            int a = follow(i, u), b = follow(i, v); int d = 0;
            for (size_t k = 0; k < bits[a].size(); k++) d += __builtin_popcountll(bits[a][k] & ~bits[b][k]);
            printf("   [x ="); for (int e : prefix(i)) printf(" %d", e); printf("; slack %d; missing %d of %d, live %d]", sit[i].s, d, cnt[a], liveMissing(a, b, sit[a].last));
        }
        printf("\n"); fflush(stdout);
    }
    printf("total checks %ld, failures %ld, with a live missing state %ld", tot, totbad, totlive); if (SIM) printf(", not repaired by simulation %ld", totsim); printf("\n");
}
