"""Part B, norm test: mu = u rho + v rho forces |mu|^2 = 2|rho|^2 + 2 (rho, w rho).
For each type: the norms of regular dominant mu <= 2 rho, the norms of the weights rho + w rho, the regular mu whose
norm is not attained, and the regular mu that are not PRV although their norm is attained.   Usage: python3 norm.py TYPE rank"""
import sys
from rs import *
def run(T, n):
    R = RS(T, n); rho = R.rho
    prv = {}
    for v in R.orbit(rho):
        d = R.dom(tuple(a + b for a, b in zip(rho, v))); prv[d] = prv.get(d, 0) + 1
    norms = {R.ip(m, m) for m in prv}
    B = R.below(tuple(2 * x for x in rho)); reg = sorted(m for m in B if min(m) >= 1)
    regn = {R.ip(m, m) for m in reg}
    miss = [m for m in reg if m not in prv]
    bad_norm = [m for m in reg if R.ip(m, m) not in norms]
    print(f"{T}{n}: regular {len(reg)}, not PRV {len(miss)}, regular with norm not attained {len(bad_norm)}, not PRV with attained norm {len([m for m in miss if R.ip(m, m) in norms])}")
    print("   norms of regular mu not attained by any rho + w rho:", sorted(str(x) for x in regn - norms), " not PRV:", miss)
    return R, prv, reg
if __name__ == "__main__": run(sys.argv[1], int(sys.argv[2]))
