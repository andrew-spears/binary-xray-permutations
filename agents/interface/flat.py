"""Does a run of letters e = 0 make every pair of partitions reachable?
For every DFA state of slack_dfa.py (max slack <= B): apply e = 0 repeatedly and record how many
zeros are needed until the reachable set is ALL pairs of partitions with sigma boxes (or that it never is).
Also the same starting from a single interface state.   Usage: python3 flat.py B"""
import sys
from slack_dfa import run
B = int(sys.argv[1])
bad, seen, nstates, maxset = run(B, verbose=False)
def step0(S):
    T = set()
    for rm, cm in S:
        for u in range(-B, B + 1):
            if rm >> (B + u) & 1 or cm >> (B - u) & 1: continue
            r2 = rm | 1 << (B + u); c2 = cm | 1 << (B - u)
            if r2 & 1 and c2 & 1: T.add((r2 >> 1, c2 >> 1))
    return frozenset(T)
def closure(S):
    """union of everything reachable with zeros = candidate full set"""
    A = set(S); fr = set(S)
    while fr:
        fr = set(step0(fr)) - A; A |= fr
    return A
full = {}; worst = {}; never = 0; single_worst = {}
for (eprev, S, sig) in seen:
    if sig == 0: continue
    if sig not in full: full[sig] = None
for sig in sorted(full):
    # all states of this slack = union over DFA states, closed under zeros
    A = set()
    for (eprev, S, s2) in seen:
        if s2 == sig: A |= S
    full[sig] = frozenset(closure(A))
for (eprev, S, sig) in seen:
    if sig == 0: continue
    T = S; t = 0
    while T != full[sig] and t < 4 * B + 5:
        T = step0(T); t += 1
    if T != full[sig]: never += 1
    else: worst[sig] = max(worst.get(sig, 0), t)
for sig in sorted(full):
    w = 0; nv = 0
    for x in full[sig]:
        T = frozenset([x]); t = 0
        while T != full[sig] and t < 4 * B + 5:
            T = step0(T); t += 1
        if T != full[sig]: nv += 1
        else: w = max(w, t)
    single_worst[sig] = (w, nv)
print(f"B={B}: DFA states that never become full: {never}")
for sig in sorted(full):
    print(f"  sigma={sig}: {len(full[sig])} pairs; zeros needed from a DFA state <= {worst.get(sig)}; from a single state <= {single_worst[sig][0]} (never: {single_worst[sig][1]})")
from slack_dfa import word_of
print("DFA states with last letter <= 1 (so e = 0 is allowed next) that never become full:")
cnt = 0
for st in seen:
    (eprev, S, sig) = st
    if sig == 0 or eprev is None or eprev > 1: continue
    T = S; t = 0; hist = [len(T)]
    while T != full[sig] and t < 4 * B + 5:
        T = step0(T); t += 1; hist.append(len(T))
    if T != full[sig]:
        cnt += 1
        if cnt <= 6: print("  word", word_of(seen, st), "sigma", sig, "sizes under zeros", hist[:8], "of", len(full[sig]))
print("  total:", cnt)
