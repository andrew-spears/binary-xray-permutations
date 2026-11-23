"""More global feature families (rule a = f(feature), feature may use Landau excesses e_k = sum_{i<=k} s_i - C(k,2)).
Uses check_family from families.py. Usage: python3 families2.py"""
import pickle
import families as F  # runs nothing heavy at import? (guarded below)
def s_(D): n=len(D); return [D[i]+n-1-i for i in range(n)]
def e_(D, k):  # excess after first k entries (k = 0..n)
    s=s_(D); return sum(s[:k]) - k*(k-1)//2
def jr(D,i): return sum(1 for x in D[:i] if x%2==D[i]%2)+1
FAM = {
 "k,p,e_k%2":    lambda D,i: (i, D[i]%2, e_(D,i+1)%2),
 "k,p,e_k-1%2":  lambda D,i: (i, D[i]%2, e_(D,i)%2),
 "k,p,both%2":   lambda D,i: (i, D[i]%2, e_(D,i)%2, e_(D,i+1)%2),
 "j,p,e_k%2":    lambda D,i: (jr(D,i), D[i]%2, e_(D,i+1)%2),
 "j,p,e_k-1%2":  lambda D,i: (jr(D,i), D[i]%2, e_(D,i)%2),
 "d,e_k":        lambda D,i: (D[i], e_(D,i+1)),
 "d,k,e_k":      lambda D,i: (D[i], i, e_(D,i+1)),
 "d,k,e_k-1,e_k":lambda D,i: (D[i], i, e_(D,i), e_(D,i+1)),
}
F.run(FAM, 8)
