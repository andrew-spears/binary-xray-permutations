"""Local check of the steps out of A(4m^2+1), m = 1..MMAX (no enumeration of states; slack up to 4 MMAX^2 + 2).
 A = l1.A_set(m): 4 states, central, each with exactly one 1-pred, which is in E0; in (lam, mu') form the two diagrams differ by one box.
 (O4) every 1-successor u of a in A has a 1-pred outside A.
 (O5) every a in A has exactly one (-1)-successor, and it is in SC u E0.
 (O6) every central 0-successor u of a in A, u not in A, has a central 0-pred outside A.
 Also prints the least number of 1-preds / central 0-preds over those successors (the proof needs > 4 for large m).
  python3 local.py MMAX"""
import sys, l1
for m in range(1, int(sys.argv[1]) + 1):
    A = l1.A_set(m); s = 4 * m * m + 1
    assert len(A) == 4 and all(l1.slack(a) == s and l1.central(a) for a in A)
    for a in A:
        p = l1.preds(a, 1); assert len(p) == 1 and l1.is_E0(p[0][1])
        assert abs(sum(a[0]) - sum(a[1])) == 1 and all(x <= y for x, y in zip(*sorted(a, key=sum))) and len(min(a, key=sum)) <= len(max(a, key=sum))
    n4 = n6 = 10 ** 9; c4 = c6 = 0
    for a in A:
        for k, u in l1.succs(a, 1):
            pr = [v for j, v in l1.preds(u, 1)]; assert any(v not in A for v in pr); n4 = min(n4, len(pr)); c4 += 1
        sm = l1.succs(a, -1); assert len(sm) == 1 and (l1.is_E0(sm[0][1]) or l1.is_SC(sm[0][1])) and l1.in_T(sm[0][1])
        for k, u in l1.succs(a, 0):
            if not l1.central(u) or u in A: continue
            pr = [v for j, v in l1.preds(u, 0) if l1.central(v)]; assert any(v not in A for v in pr); n6 = min(n6, len(pr)); c6 += 1
    print(f"m {m} (slack {s}): A = {' '.join(sorted(l1.name(a) for a in A))[:150]}; O4 ok ({c4} successors, least number of 1-preds {n4}); O5 ok; O6 ok ({c6} successors, least number of central 0-preds {n6})", flush=True)
