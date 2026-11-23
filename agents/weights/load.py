"""Loader for the output of ./dump (states as pairs of partitions, minimal reachable / completable sets, transitions)."""
import numpy as np
from math import factorial
def part(s): return () if s == "-" else tuple(int(a) for a in s.split(","))
def conj(l): return tuple(sum(1 for a in l if a > i) for i in range(l[0])) if l else ()
def flam(l):
    """number of standard Young tableaux of shape l (hook length formula)"""
    c = conj(l); h = 1
    for i, a in enumerate(l):
        for j in range(a): h *= a - j + c[j] - i - 1
    return factorial(sum(l)) // h
class Data:
    def __init__(self, path, trans=True):
        lines = open(path + ".txt").read().split("\n"); raw = np.fromfile(path + ".bin", dtype=np.uint64)
        self.lev = []; self.F = {}; self.A = {}; i = 0; p = 0
        while i < len(lines) and lines[i]:
            h = lines[i].split(); i += 1
            if h[0] == "L":
                n = int(h[2]); self.lev.append([tuple(part(a) for a in lines[i + k].split("|")) for k in range(n)]); i += n
            else:
                d, s, l, n, w = map(int, h[1:]); words = [tuple(int(a) for a in lines[i + k].split()) for k in range(n)]; i += n
                bits = raw[p:p + n * w].reshape(n, w); p += n * w
                (self.F if d > 0 else self.A)[(s, l)] = (bits, words)
        self.B = len(self.lev) - 1; self.idx = [{t: k for k, t in enumerate(L)} for L in self.lev]
        if trans:
            tr = np.fromfile(path + ".tr", dtype=np.uint32); q = 0; self.off = []; self.dat = []
            for s in range(self.B + 1):
                n = tr[q]; self.off.append(tr[q + 1:q + 1 + n].astype(np.int64)); q += 1 + n
                n = tr[q]; self.dat.append(tr[q + 1:q + 1 + n].astype(np.int64)); q += 1 + n
    def sets(self, d, s, l):
        """0/1 matrix (minimal sets x states of slack s) of the reachable (d = 1) or completable (d = -1) sets at (s, l)"""
        bits = (self.F if d > 0 else self.A)[(s, l)][0]
        return np.unpackbits(bits.view(np.uint8), axis=1, bitorder="little")[:, :len(self.lev[s])]
    def letters(self, d, s): return sorted(l for (s2, l) in (self.F if d > 0 else self.A) if s2 == s)
    def T(self, s, e):
        """sparse 0/1 matrix of the letter e from slack s to slack s + e: T[i, j] = 1 if state j is an e-successor of
        state i (one entry per placement of the stone, so products of these matrices count placements)"""
        from scipy.sparse import csr_matrix
        n = len(self.lev[s]); m = len(self.lev[s + e]); B = self.B; k = np.arange(n) * (B + 1) + e + s
        lo = self.off[s][k]; hi = self.off[s][k + 1]
        cols = np.concatenate([self.dat[s][a:b] for a, b in zip(lo, hi)]) if n else np.zeros(0, int)
        return csr_matrix((np.ones(len(cols)), cols, np.concatenate([[0], np.cumsum(hi - lo)])), shape=(n, m))
    def sigma(self, s, f):
        """permutation of the states of slack s induced by f on pairs of partitions"""
        return np.array([self.idx[s][f(t)] for t in self.lev[s]])
