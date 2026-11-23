"""Bounded-slack automaton (see README.md in this folder).

Stones are placed in increasing order.  Flip rows (r' = n+1-r): stone k gets a cell
(r', c) with r' + c = 2k + e_k, where e_k = s_k - (k-1).  After k stones the used rows
R' and used columns C are k-subsets of [n]; excess(R') + excess(C) = sigma_k (the Landau
slack of the prefix), where excess(X) = sum(X) - k(k+1)/2.  So a witness is a walk on pairs
of k-subsets, and with sigma <= B every hole/extra is within B of k: a finite automaton,
translation invariant in k and independent of n.

Valid words: e_{k+1} >= e_k - 1 (d strictly increasing), partial sums sigma_k >= 1 inside
(no tight cut), sigma_n = 0.  This script determinizes the automaton over all valid words
with max sigma <= B and reports whether every valid word is accepted.

Usage: python3 slack_dfa.py B [--tight]   (--tight also allows sigma_k = 0 inside)
"""
import sys
from collections import deque

def run(B, allow_tight=False, verbose=True):
    W = 2 * B                      # window: positions k-B+1 .. k+B  <-> bits 0 .. 2B-1
    base = (1 << B) - 1            # positions <= k all used, none above
    def succ_masks(mask):
        """all (u, newmask) from adding position k+1+u, then re-centring on k+1"""
        out = []
        for u in range(-B, B + 1):
            bit = B + u
            if mask >> bit & 1: continue
            m = mask | (1 << bit)
            if not (m & 1): continue      # hole would fall out of the window: excess > B
            out.append((u, m >> 1))
        return out
    cache = {}
    def sm(mask):
        r = cache.get(mask)
        if r is None: r = cache[mask] = succ_masks(mask)
        return r
    start = (None, frozenset([(base, base)]), 0)
    seen = {start: None}
    dq = deque([start])
    bad = None; nstates = 0; maxset = 0
    while dq:
        st = dq.popleft(); nstates += 1
        eprev, S, sig = st
        lo = 0 if eprev is None else eprev - 1
        for e in range(max(lo, -sig), B - sig + 1):
            sig2 = sig + e
            if sig2 == 0 and sig == 0: continue          # e = 0 at sigma = 0: tight cut / trivial
            T = set()
            for (rm, cm) in S:
                for (u, rm2) in sm(rm):
                    v = e - u
                    if v < -B or v > B: continue
                    bit = B + v
                    if cm >> bit & 1: continue
                    c2 = cm | (1 << bit)
                    if not (c2 & 1): continue
                    T.add((rm2, c2 >> 1))
            T = frozenset(T)
            if sig2 == 0:
                if not T:
                    bad = (st, e); break
                if not allow_tight: continue             # word ends
            nxt = (e, T, sig2)
            if nxt not in seen:
                if not T:
                    # empty set: a rejection iff the prefix can be completed inside the bound
                    if sig2 + max(e, 0) * max(e - 1, 0) // 2 <= B:
                        bad = (st, e); break
                    continue
                seen[nxt] = (st, e); dq.append(nxt)
                if len(T) > maxset: maxset = len(T)
        if bad: break
    return bad, seen, nstates, maxset

def word_of(seen, st):
    w = []
    while seen[st] is not None:
        st, e = seen[st]; w.append(e)
    return w[::-1]

if __name__ == "__main__":
    B = int(sys.argv[1]); tight = "--tight" in sys.argv
    bad, seen, nstates, maxset = run(B, tight)
    print(f"B={B} dfa_states={nstates} max_set={maxset}", "ALL ACCEPTED" if bad is None else "REJECTED")
    if bad:
        st, e = bad
        print("rejected word e =", word_of(seen, st) + [e])
