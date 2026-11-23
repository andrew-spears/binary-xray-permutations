"""Theorem D of REPORT.md as a test.  viol(u, w): u = (lambda, mu) violates (D) for the word w (letters in word order, the last letter of w is the last step into u):
some p, q >= 0, k >= 1 with  (sum of the k letters before the last p + q letters) > k (p + q) + sum_{i <= k} (lambda_{p+i} + mu_{q+i})."""
def viol(u, w):
    lam, mu = u; e = w[::-1]; L = len(e); E = [0]
    for x in e: E.append(E[-1] + x)
    for t in range(L):
        if t and max(e) <= t: break                 # letters <= t: no violation with p + q >= t
        for p in range(t + 1):
            q = t - p; cap = 0
            for k in range(1, L - t + 1):
                cap += (lam[p + k - 1] if p + k - 1 < len(lam) else 0) + (mu[q + k - 1] if q + k - 1 < len(mu) else 0)
                if E[t + k] - E[t] > k * t + cap: return True
    return False

def excess(w):
    """young excess of the word w: y' = max(0, y + e - 1) along w (REPORT3 of agents/universal)"""
    y = 0
    for e in w: y = max(0, y + e - 1)
    return y

def inN(u, w):
    """the explicit family of Corollary N: a row longer than s - yhat or a column longer than s - y, yhat = excess of w without its last letter, y = excess of w"""
    lam, mu = u; s = sum(lam) + sum(mu); yh, y = excess(w[:-1]), excess(w)
    return max(lam[:1] + mu[:1] + (0,)) > s - yh or max(len(lam), len(mu)) > s - y
