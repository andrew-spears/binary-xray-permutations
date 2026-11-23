from exlib import wits, Pn
def splice(top,bot,s):
    """top over bottom; bottom's highest column slides right past s of the top's lowest columns"""
    a,b=len(top),len(bot); n=a+b
    # column order word: B*(b-1), T*s, B, T*(a-s)
    word="B"*(b-1)+"T"*s+"B"+"T"*(a-s)
    Tc=[i+1 for i,ch in enumerate(word) if ch=="T"]; Bc=[i+1 for i,ch in enumerate(word) if ch=="B"]
    return tuple(Tc[c-1] for c in top)+tuple(Bc[c-1] for c in bot), word
def D(p): return sorted(p[i]-i-1 for i in range(len(p)))
if __name__=="__main__":
    p,w=splice((3,1,4,2),(2,4,1,3),2); print("Q8 check",p,w,D(p))
    def Q(n):
        P=list(Pn(n))
        if n%2: P[P.index(-2)]=-1; P[P.index(2)]=1
        else: P[P.index(-1)]=0; P[P.index(3)]=2
        return sorted(P)
    for n in (7,8,9,10,11,12):
        tgt=Q(n); hits=[]
        for a in range(3,n-2):
            b=n-a
            T=[tuple(x) for x in wits(Pn(a))] if a>=4 else [(1,3,2),(2,1,3)]
            B=[tuple(x) for x in wits(Pn(b))] if b>=4 else [(1,3,2),(2,1,3)]
            for t in T:
                for bb in B:
                    for s in range(1,a+1):
                        p,w=splice(t,bb,s)
                        if D(p)==tgt: hits.append((a,t,bb,s,p))
        print(f"Q{n} = {tgt}: {len(hits)} splices", hits[:3])
