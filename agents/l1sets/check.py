"""Checks of REPORT.md against enumeration, slack <= S (S = 18: 2 minutes).
 1. T(s) (structural: l1.in_T) = Central(s) minus G(s), G = largest slack-only family inside slack <= S (fam.gfp), for s <= S - 1; sizes.
 2. machine of l1.py (preds / succs on (lam, mu')) = machine of ../weights/maya.py, all states, s <= min(S, 9).
 3. Lemmas of REPORT.md, all states of slack <= min(S, L): Lemma 1 (counts and classes), Lemma 2 (at most one bad predecessor), Lemma 3.
  python3 check.py S [L]"""
import sys
from fam import *
import l1
L = int(sys.argv[2]) if len(sys.argv) > 2 else 12
def tol1(t): return (Mo.part(t[0]), l1.conj(Mo.part(t[1])))
G = gfp(); ok = True
for s in range(S):
    U = [tol1(t) for t in St[s]]
    Tset = {i for i, u in enumerate(U) if l1.central(u) and l1.in_T(u)}
    Gset = {i for i, u in enumerate(U) if G[s] >> i & 1}; cen = {i for i, u in enumerate(U) if l1.central(u)}
    good = (cen - Tset == Gset); ok &= good
    if Tset or not good: print(f"1. s {s}: central {len(cen)}, |T| {len(Tset)}, |G| {len(Gset)}, Central minus T = G: {good}   T minus SC: {' '.join(l1.name(U[i]) for i in sorted(Tset) if not l1.is_SC(U[i]))[:200]}", flush=True)
print(f"1. T(s) = Central(s) minus G(s) for all s < {S}: {ok};  |G(s)| = {[bin(G[s]).count('1') for s in range(S)]}")
for s in range(min(S, 9) + 1):
    for t in St[s]:
        u = tol1(t)
        for e in (-1, 0, 1):
            if s + e >= 0 and s + e <= S: assert sorted(tol1(v) for v in set(Mo.succ(t, e))) == sorted(v for k, v in l1.succs(u, e)), (u, e)
            if s - e >= 0 and s - e <= S:
                pr = {v for k, v in l1.preds(u, e)}
                assert all(u in [w for k, w in l1.succs(v, e)] for v in pr), (u, e)
print(f"2. l1.py machine = maya.py machine for all states of slack <= {min(S, 9)}")
cnt = [0, 0, 0]
for s in range(1, min(S, L) + 1):
    for t in St[s]:
        u = tol1(t); c = l1.cls(u)
        p1 = [v for k, v in l1.preds(u, 1)]; pm = [v for k, v in l1.preds(u, -1)]; p0 = l1.preds(u, 0)
        assert sum(1 for v in p1 if l1.is_SC(v) or l1.is_E0(v)) <= 1; cnt[0] += 1
        assert len(pm) >= 2 and not any(l1.is_SC(v) for v in pm) and sum(1 for v in pm if l1.is_E0(v)) <= 1; cnt[1] += 1
        ev = [v for k, v in p0 if k % 2 == 0]; od = [v for k, v in p0 if k % 2]
        assert len(ev) >= c and len(od) >= 1 - c and all(l1.cls(v) == 2 - c for v in ev) and all(l1.cls(v) == -c for v in od)
        assert all(l1.cls(v) == 1 - c for v in p1 + pm)
        assert sum(1 for v in od if l1.is_SC(v) or l1.is_E0(v)) <= 1
        if s % 4 == 0 and c == 0:
            cnt[2] += 1
            if len(od) == 1 and (l1.is_SC(od[0]) or l1.is_E0(od[0])): assert l1.in_T(u)
print(f"3. Lemma 1 (counts, classes) and Lemma 2 (a), (b), (c) on all {cnt[0]} states of slack 1..{min(S, L)}; Lemma 3 (a), (b) on {cnt[2]} central states with 4 | s: ok")
