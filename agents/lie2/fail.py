"""Part B: the regular dominant weights mu <= 2 rho that are not conjugate to rho + w rho, with data.
Usage: python3 fail.py TYPE rank"""
import sys
from rs import *
T, n = sys.argv[1], int(sys.argv[2]); R = RS(T, n); rho = R.rho
O = R.orbit(rho); prv = {}
for v in O:
    d = R.dom(tuple(a + b for a, b in zip(rho, v))); prv[d] = prv.get(d, 0) + 1
B = R.below(tuple(2 * x for x in rho)); reg = sorted(m for m in B if min(m) >= 1)
print(f"{T}{n}: d = {[str(x) for x in R.d]} rho_l = {[str(x) for x in R.rho_l]} rho_s = {[str(x) for x in R.rho_s]} |rho|^2 = {R.ip(rho, rho)}")
for m in reg:
    lam = tuple(a - 1 for a in m)
    print("  mu", m, "PRV x%d" % prv[m] if m in prv else "NOT PRV", "|mu|^2 =", R.ip(m, m), " 2rho - mu =", [str(x) for x in R.coords(tuple(2 - a for a in m))])
