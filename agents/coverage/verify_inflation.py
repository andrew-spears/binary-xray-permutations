"""Check the inflation offset formula: build tau[B1..Bk] from real witnesses and compare diagonals."""
import random, sys
sys.argv=['x','1']
from inflation import offsets, compositions
from common import *
random.seed(1); bad=0; tot=0
for tau in [(2,4,1,3),(3,1,4,2),(2,4,1,5,3),(2,5,3,1,4)]:
    for n in range(len(tau), 13):
        for sizes in random.sample(list(compositions(n,len(tau))), min(5, len(list(compositions(n,len(tau)))))):
            parts=[]
            for m in sizes:
                D=random.choice(enum_valid(m)); parts.append((D, find_witness(D,m)))
            if any(w is None for _,w in parts): continue
            k=len(tau); rs=[sum(sizes[:i]) for i in range(k)]
            inv=sorted(range(k),key=lambda i:tau[i]); cs=[0]*k; acc=0
            for i in inv: cs[i]=acc; acc+=sizes[i]
            p=[]
            for i in range(k): p += [cs[i]+x for x in parts[i][1]]
            assert sorted(p)==list(range(1,n+1))
            offs=offsets(tau,sizes)
            pred=tuple(sorted(d+o for (D,_),o in zip(parts,offs) for d in D))
            tot+=1; bad+= diags(tuple(p))!=pred
print("checked",tot,"mismatches",bad)
