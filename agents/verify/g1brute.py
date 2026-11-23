# Sanity: every valid D (n<=9) has a witness with pi(1) = 1 + d_n (largest diagonal in row 1).
import itertools
for n in range(2,10):
    have=set(); good=set()
    for p in itertools.permutations(range(1,n+1)):
        ds=[p[i]-i-1 for i in range(n)]
        if len(set(ds))==n:
            D=tuple(sorted(ds)); have.add(D)
            if p[0]==1+D[-1]: good.add(D)
    print(n,len(have),len(good),have==good)
