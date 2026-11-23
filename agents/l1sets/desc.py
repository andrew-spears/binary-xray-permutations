"""Item 1 (tested): exact description of F(x) for L1 prefixes inside slack <= S.
 For every distinct (F(x), slack): F = Sat(s, Gamma) minus Ex, Gamma = set of classes c = a + b on F, Sat = all states of slack s with c in Gamma.
 Checks (i) the rule for Gamma on every edge:  +: 1 - Gamma;  -: (1 - Gamma) n feasible(s - 1);  0: (-Gamma u (2 - Gamma)) n feasible(s),
 feasible(s) = {c : m(m-1) <= s, c = s mod 2}, m = max(c, 1 - c);  (ii) Ex subset of SC u E0 u A-type, and prints the nodes where Ex is not
 exactly SC n Sat (after a last letter +) / empty (otherwise).
  python3 desc.py S"""
import sys
from cores import *
import l1
feas = lambda s: {c for c in range(-s - 1, s + 2) if (c - s) % 2 == 0 and max(c, 1 - c) * (max(c, 1 - c) - 1) <= s}
if __name__ == "__main__":
    tol1 = lambda t: (Mo.part(t[0]), l1.conj(Mo.part(t[1])))
    U = [[tol1(t) for t in L] for L in St]; SCm = [sum(1 << i for i, u in enumerate(L) if l1.is_SC(u)) for L in U]
    info = {}
    for (F, s) in seen:
        T, Pi = sat(F, s); info[F, s] = (T, {a + b for a, b in Pi})
        assert Pi == {p for p in set(ab[s]) if sum(p) in info[F, s][1]}
    edges = bad = 0; lastl = {}
    for (F, s) in seen:
        G = info[F, s][1]
        for e in (1, 0, -1):
            if not 0 <= s + e <= S: continue
            F2 = step(F, s, e); G2 = info[F2, s + e][1]; edges += 1; lastl.setdefault((F2, s + e), set()).add(e)
            want = ({1 - c for c in G} if e else {-c for c in G} | {2 - c for c in G}) & feas(s + e)
            bad += want != G2
    print(f"bound {S}: {len(seen)} distinct (F, slack); Gamma rule holds on {edges - bad} of {edges} edges; Gamma always contains the central class: {all(s % 2 in info[F, s][1] for F, s in seen)}")
    mx = 0; odd = []
    for (F, s), w in sorted(seen.items(), key=lambda kv: (kv[0][1], len(kv[1]), kv[1])):
        T = info[F, s][0]; ex = T & ~F; mx = max(mx, bin(ex).count("1")); ll = lastl.get((F, s), set())
        exs = [U[s][i] for i in range(len(U[s])) if ex >> i & 1]
        assert all(l1.is_SC(u) or l1.is_E0(u) or len(l1.preds(u, 1)) == 1 or s == 5 for u in exs), (s, w)
        expect = (T & SCm[s]) if ll == {1} else 0
        if ex != expect: odd.append(f"   s {s}, last letters {sorted(ll)}, x = {''.join('+0-'[1 - e] for e in w)}: Ex = {' '.join(l1.name(u) for u in exs)[:120]}" + ("  [SC n Sat expected]" if ll == {1} else ""))
    print(f"largest |Ex| = {mx}; nodes where Ex is not (SC n Sat after +, empty otherwise): {len(odd)}"); print("\n".join(odd))
