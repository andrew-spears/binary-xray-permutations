// For every arrangement D of size n (D = set of distinct values i + pi(i)), which patterns of length 4
// can a solution always avoid?  For each D we keep the set of "contained patterns" masks of its solutions
// (only the masks minimal under inclusion matter).  Usage: ./pat n
#include <bits/stdc++.h>
using namespace std;
int n; int pi_[16]; bool usedc[16]; bool usedd[40];
int patid[4][4][4][4]; vector<string> names;
unordered_map<unsigned long long, vector<unsigned>> M;
void add(unsigned long long D, unsigned m) {
    auto &v = M[D];
    for (unsigned x : v) if ((x & m) == x) return;            // an existing mask is at least as good
    v.erase(remove_if(v.begin(), v.end(), [&](unsigned x) { return (x & m) == m; }), v.end());
    v.push_back(m);
}
void rec(int i, unsigned long long D) {
    if (i == n) {
        unsigned m = 0;
        for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) for (int d = c + 1; d < n; d++) {
            int v[4] = {pi_[a], pi_[b], pi_[c], pi_[d]}, r[4];
            for (int x = 0; x < 4; x++) { r[x] = 0; for (int y = 0; y < 4; y++) r[x] += v[y] < v[x]; }
            m |= 1u << patid[r[0]][r[1]][r[2]][r[3]];
        }
        add(D, m); return;
    }
    for (int c = 0; c < n; c++) if (!usedc[c] && !usedd[i + c]) {
        usedc[c] = usedd[i + c] = true; pi_[i] = c; rec(i + 1, D | (1ull << (i + c)));
        usedc[c] = usedd[i + c] = false;
    }
}
int main(int argc, char **argv) {
    n = atoi(argv[1]);
    int p[4] = {0, 1, 2, 3}, k = 0;
    do { patid[p[0]][p[1]][p[2]][p[3]] = k++; string s; for (int x : p) s += char('1' + x); names.push_back(s); } while (next_permutation(p, p + 4));
    rec(0, 0);
    printf("n=%d arrangements with a solution: %zu\n", n, M.size());
    vector<int> ok1;
    for (int a = 0; a < 24; a++) {
        long bad = 0; for (auto &kv : M) { bool g = false; for (unsigned x : kv.second) if (!(x >> a & 1)) { g = true; break; } if (!g) bad++; }
        printf("  avoid %s: fails for %ld arrangements\n", names[a].c_str(), bad); if (!bad) ok1.push_back(a);
    }
    printf("  pairs that can always be avoided together:");
    for (int a : ok1) for (int b : ok1) if (a < b) {
        bool all = true; unsigned q = 1u << a | 1u << b;
        for (auto &kv : M) { bool g = false; for (unsigned x : kv.second) if (!(x & q)) { g = true; break; } if (!g) { all = false; break; } }
        if (all) printf(" %s+%s", names[a].c_str(), names[b].c_str());
    }
    printf("\n");
    // largest sets: greedy report of every maximal avoidable set among the single survivors (exhaustive over subsets if few)
    if (ok1.size() <= 16) {
        vector<unsigned> good;
        for (unsigned s = 1; s < (1u << ok1.size()); s++) {
            unsigned q = 0; for (size_t j = 0; j < ok1.size(); j++) if (s >> j & 1) q |= 1u << ok1[j];
            bool all = true;
            for (auto &kv : M) { bool g = false; for (unsigned x : kv.second) if (!(x & q)) { g = true; break; } if (!g) { all = false; break; } }
            if (all) good.push_back(q);
        }
        printf("  maximal sets avoidable together:");
        for (unsigned q : good) { bool mx = true; for (unsigned r : good) if (r != q && (r & q) == q) { mx = false; break; }
            if (mx) { printf(" {"); for (int a = 0; a < 24; a++) if (q >> a & 1) printf(" %s", names[a].c_str()); printf(" }"); } }
        printf("\n");
    }
}
