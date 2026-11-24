"""Which odd states are joined?  python3 stats.py N
For each triple (s1, m, s2) from valid words of length <= N: is all of Odd'(s2) reached from Odd(1^s1); does every state of Odd(1^s1)
reach Odd'(s2); do the one-row / one-column states (s1|-), (-|s1) alone reach Odd'(s2).  Also checks the rim-hook description of Odd(1^s)."""
import sys
N = int(sys.argv[1]); sys.argv[1] = "0"
exec(open("oddbridge.py").read().split('if sys.argv[1] == "pairs"')[0])
def rim(s):
    """pairs reached an odd number of times by adding rim hooks of sizes 2^j (bits of s, increasing) to either diagram: beads move up by 2^j."""
    P = {E: 1}
    for j in range(s.bit_length()):
        if not (s >> j) & 1: continue
        h = 1 << j; Q = {}
        for u, c in P.items():
            for side in (0, 1):
                d = len(u[side]) + h + 2; bs = l1.beads(u[side], d); B = set(bs)
                for b in bs:
                    if b + h not in B:
                        v = l1.part([x for x in bs if x != b] + [b + h]); w = (v, u[1]) if side == 0 else (u[0], v)
                        Q[w] = Q.get(w, 0) ^ c
        P = {u: 1 for u, c in Q.items() if c}
    return frozenset(P)
for s in range(0, 14): assert rim(s) == odd_fwd(s), s
print("Odd(1^s) = rim-hook set for s <= 13")
for n in range(5, N + 1):
    seen = set(); full = each = row = col = 0
    for w in words(n):
        t = split(w)
        if t is None or t in seen: continue
        seen.add(t); s1, m, s2 = t
        if s1 not in OF: OF[s1] = odd_fwd(s1)
        if s2 not in OB: OB[s2] = odd_bwd(s2)
        def go(F):
            for e in m: F = frozenset(v for u in F for k, v in l1.succs(u, e))
            return F & OB[s2]
        full += go(OF[s1]) == OB[s2]; each += all(go([u]) for u in OF[s1])
        row += bool(go([((s1,) if s1 else (), ())])); col += bool(go([((), (s1,) if s1 else ())]))
    print(f"n = {n}: triples {len(seen)}; all of Odd' reached {full}; every odd start works {each}; start (s1|-) works {row}; start (-|s1) works {col}")
