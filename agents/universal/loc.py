"""Local obstruction of a tail, read off the Maya diagrams (coordinates of ../l1sets: M = M(lam), B = M(nu), beads lam_i - i).
A 2-predecessor t_k of u (k in M, k - 1 not in B) is central or not according to the parity of k only; so
    Loc_2(s) = central states of slack s with no central 2-predecessor = {u : every bead k of M with k = p(u) mod 2 has k - 1 in B}.
python3 loc.py S : for s <= S checks that rule, and prints |Central(s)|, |Loc_2(s)|, and |Central(s) minus T minus step_2(G(s-2))|
(G = Central minus T, the proved family for letters -1, 0, 1), i.e. what a letter 2 after a saturated prefix excludes."""
import sys
sys.path.insert(0, "../l1sets")
import l1, exc
S = int(sys.argv[1])
for s in range(2, S + 1):
    cen = [u for u in exc.states(s) if l1.central(u)]; loc = 0; rule = True; bad = 0; par = {}
    for u in cen:
        pr = l1.preds(u, 2); a = l1.c0(u[0]); good = [k for k, t in pr if l1.central(t)]
        for k, t in pr:
            key = (a % 2, s % 2, k % 2)                       # does the parity of k decide whether t_k is central?  (per parity of a and s)
            if par.setdefault(key, l1.central(t)) != l1.central(t): rule = False
        if not good: loc += 1
        if not l1.in_T(u) and not any(not l1.in_T(t) for k, t in pr if l1.central(t)): bad += 1
    print(f"slack {s:2d}: Central {len(cen):5d}  Loc_2 {loc:4d}  G(s) minus step_2 G(s-2) {bad:4d}   parity rule {'ok' if rule else 'FAILS'} {sorted(k for k, v in par.items() if v)}")
