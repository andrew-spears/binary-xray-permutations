import sys, itertools
sys.path.insert(0, "../intervals")
from poset import multisets
from lib import values
n = int(sys.argv[1]); got = set()
for k in itertools.product(*[range(t) for t in range(1, n + 1)]):
    got.add(tuple(sorted(values(k))))
M = set(multisets(n))
miss = sorted(M - got)
print(n, len(M), len(miss))
for d in miss[:int(sys.argv[2])]: print("  ", d)
