# Which move rule makes "every-other-mark reaches exactly the valid D" true?
import sys; sys.argv=[sys.argv[0],'1']; from g1step import valid_Ds
def moves(D,g3):
    S=set(D)
    for a in D:
        for b in D:
            if b-a<3 or (g3 and b-a!=3): continue
            if a+1 in S or b-1 in S or any(z not in S for z in range(a+2,b-1)): continue
            yield tuple(sorted(S-{a,b}|{a+1,b-1}))
for n in range(3,11):
    V=set(valid_Ds(n)); start=tuple(range(-(n-1),n,2))
    for g3 in (0,1):
        seen={start}; st=[start]
        while st:
            for E in moves(st.pop(),g3):
                if E not in seen: seen.add(E); st.append(E)
        print(n,"gap3-only" if g3 else "general", len(seen), "valid", len(V), seen==V)
