"""A_lp(D): all parity choices a (mask over sorted stones, bit k = a(d_k)) with the
parity-restricted fractional LP feasible.  Usage: python3 lpsets.py n  -> lp_n.txt
Line format: d_0 ... d_{n-1} | hexbitset (same encoding as wit_n.txt)."""
import sys
sys.path.insert(0, '/home/claude/agents/start')
from common import landau_D, lp, counts_ok
from multiprocessing import Pool

n = int(sys.argv[1])

def work(D):
    S = 0
    for m in range(1 << n):
        a = {d: (m >> k) & 1 for k, d in enumerate(D)}
        if counts_ok(n, D, a) and lp(n, D, a):
            S |= 1 << m
    return D, S

if __name__ == '__main__':
    Ds = landau_D(n)
    W = ((1 << n) + 63) // 64
    with Pool(2) as p, open(f'/home/claude/agents/paritydata/lp_{n}.txt', 'w') as f:
        for D, S in p.imap(work, Ds, chunksize=4):
            words = ''.join('%016x' % ((S >> (64 * w)) & ((1 << 64) - 1)) for w in range(W))
            f.write(' '.join(map(str, D)) + ' | ' + words + '\n')
            f.flush()
