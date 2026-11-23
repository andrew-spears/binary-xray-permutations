import sys, random; sys.path.insert(0,'/home/claude/agents/tourn')
from tourn import *
random.seed(1)
for n in range(1,int(sys.argv[1])+1):
    W=witnesses(n); bad=0; badd=0
    for phi in W:
        T=gamma(phi)
        if svec(T)!=scores_of(phi): bad+=1
    # delta round trip on a sample
    for phi in random.sample(W, min(300,len(W))):
        T=gamma(phi); ph=delta(T)
        if ph is None or scores_of(ph)!=svec(T): badd+=1
    print(n, len(W), "gamma score mismatches:",bad, " delta(gamma) failures (sample):",badd, flush=True)
