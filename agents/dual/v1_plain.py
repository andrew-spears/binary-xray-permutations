"""For passing boards (R={1..m}, C={1..m+h} minus h cols, non-tight sum test), top row r0=1:
 V1any  : exists passing a and top-row e with LP_a(board - e) feasible (a restricted)  [proves peel e]
 V1all  : for EVERY passing a such an e exists
 plainOK: every top-row e whose peeled board passes the PLAIN (unrestricted) LP also passes the parity test
          (i.e. a bad cell is always killed by the plain LP, never by parity alone)
 sumOK  : same with the sum test in place of the plain LP
Usage: python3 v1_plain.py m h"""
import sys, itertools, time
sys.path.insert(0, '/home/claude/agents/cell')
from core import cells_of, lp, passing, peel, passes, sumtest, tight


def run(m, h):
    R = tuple(range(1, m + 1)); cnt = dict(boards=0); ff = {}
    def fail(k, ex):
        cnt[k] = cnt.get(k, 0) + 1; ff.setdefault(k, ex)
    for dele in itertools.combinations(range(1, m + h + 1), h):
        C = tuple(c for c in range(1, m + h + 1) if c not in dele)
        for D in itertools.combinations(range(min(C) - m, max(C)), m):
            if not sumtest(R, C, D) or tight(R, C, D) or not passes(R, C, D): continue
            cnt['boards'] += 1
            T = [(1, 1 + d) for d in sorted(D) if 1 + d in C]
            good = {e: passes(*peel(R, C, D, e)) for e in T}
            ex = (C, D, {e[1] - 1: good[e] for e in T})
            plain = {e: lp(*peel(R, C, D, e)) is not None for e in T}
            st = {e: sumtest(*peel(R, C, D, e)) for e in T}
            if any(plain[e] and not good[e] for e in T): fail('plainOK', ex + ({e[1]-1: plain[e] for e in T},))
            if any(st[e] and not good[e] for e in T): fail('sumOK', ex)
            v1 = []
            for a in passing(R, C, D, first=False):
                v1.append(any(a[e[1] - 1] == 1 and lp(*peel(R, C, D, e), {d: a[d] for d in D if d != e[1] - 1})
                              is not None for e in T))
                if not v1[-1]: ff.setdefault('V1all', ex + (a,))
            if not any(v1): fail('V1any', ex)
            if not all(v1): cnt['V1all'] = cnt.get('V1all', 0) + 1
    return cnt, ff


if __name__ == "__main__":
    m, h = int(sys.argv[1]), int(sys.argv[2]); t = time.time()
    cnt, ff = run(m, h)
    print(f"m={m} h={h} {cnt} {time.time() - t:.0f}s")
    for k in ff: print(f"  {k}: {ff[k]}")
