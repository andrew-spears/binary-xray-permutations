"""T(s) = Central(s) minus G(s) for the largest slack-only family G inside slack <= S (fam.gfp), against SC and E0.
  python3 tset.py S"""
import sys
from fam import *
from cores import c0, ab
if __name__ == "__main__":
    G = gfp()
    for s in range(S + 1):
        cen = sum(1 << i for i in range(len(St[s])) if sum(ab[s][i]) == s % 2)
        SC = sum(1 << i for i, t in enumerate(St[s]) if Mo.part(t[0]) == conj(Mo.part(t[1]))) if s else 0
        assert G[s] & ~cen == 0
        T = cen & ~G[s]; rest = T & ~SC
        print(f"s {s}: central {bin(cen).count('1')}, |G| {bin(G[s]).count('1')}, |T| {bin(T).count('1')}, SC in T: {bin(T & SC).count('1')} of {bin(SC & cen).count('1')}; T minus SC [{bin(rest).count('1')}]: {names(rest, s)[:300]}", flush=True)
