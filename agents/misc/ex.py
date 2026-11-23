import itertools
def wit(n,D):
    out=[]
    for p in itertools.permutations(range(1,n+1)):
        if sorted(p[i]-(i+1) for i in range(n))==sorted(D): out.append(p)
    return out
def show(p):
    n=len(p); return "\n".join(" ".join("●" if p[i]==j+1 else "." for j in range(n)) for i in range(n))
for name,n,D in [("F1 a=3",6,[-3,-2,-1,1,2,3]),("F2 k=4 m=2",6,[-4,-3,-1,1,3,4])]:
    w=wit(n,D); inv=[p for p in w if all(p[p[i]-1]==i+1 for i in range(n))]
    print(name,len(w),"involutions",len(inv)); print((inv or w)[0]); print(show((inv or w)[0]))
print(show((5,4,6,2,1,3)))
