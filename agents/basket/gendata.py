import json, pickle, itertools
import basket2
from exlib import valid, wits, Pn
from recursive import run as rrun, decompose
def canon(D): return tuple(sorted(-x for x in D))>=tuple(D)
def prim(loose, allw, w12, comp=False, N=9):
    basket2.WITH12=w12
    out=basket2.run(N,loose=loose,allw=allw,verbose=False,comp=comp)
    return {n:[{"D":list(D),"W":W,"w":list(add[0]),"nt":valid(D),"mir":not canon(D)} for D,W,add in out[n]] for n in range(3,N+1)}
E=[]
E.append(dict(id="valid1",title="One widen per step, every board valid",short="Basket = 21 + one witness per prime. Each step widens one point into a basket block; every board along the way must be a valid witness.",
  long="Start from the 1×1 board. A step replaces one point by a block from the basket. Every board produced must use each diagonal at most once. After all boards of size n are built, every valid arrangement of size n with no built witness is a prime; its dictionary-first witness joins the basket.",
  kind="primes", data=prim(False,False,False)))
E.append(dict(id="valid_all",title="One widen per step, every board valid, primes add all witnesses",short="As above, but each prime puts all of its witnesses in the basket.",
  long="Same as the first experiment, except that a prime contributes every one of its witnesses to the basket, not just one.",kind="primes",data=prim(False,True,False)))
E.append(dict(id="comp",title="Composite blocks in the basket",short="Every witness built so far joins the basket, not just primes.",
  long="Every valid witness found at size n (built or prime) becomes a basket block. Widening one point into a composite block such as 321 is the same as several widens at once, so this lets the search pass through invalid boards.",kind="primes",data=prim(False,False,False,comp=True)))
E.append(dict(id="loose1",title="Invalid boards allowed in between",short="Boards along the way may repeat a diagonal; only the final board must be valid. One witness per prime.",
  long="Same steps, but intermediate boards may repeat diagonals; an arrangement counts as built if some valid board of that size was produced. Primes contribute one witness.",kind="primes",data=prim(True,False,False)))
E.append(dict(id="loose_all",title="Invalid boards allowed, primes add all witnesses",short="As above, with every witness of each prime in the basket.",long="As the previous experiment, with all witnesses of each prime added.",kind="primes",data=prim(True,True,False)))
E.append(dict(id="loose12",title="Invalid boards allowed, plus the 12 frame",short="Adds 12 (two points on the main diagonal) to the basket so corner gluing (direct sums) is possible.",
  long="12 repeats diagonal 0, so it is never a witness and was never in the basket; without it no direct sum can be built. Here it is added as a frame-only block. One witness per prime.",kind="primes",data=prim(True,False,True)))
E.append(dict(id="loose12_all",title="Invalid boards allowed, 12 frame, primes add all witnesses",short="The most permissive basket search.",long="Invalid intermediates, 12 in the basket, every witness of each prime added.",kind="primes",data=prim(True,True,True)))
# robust expansion
res=pickle.load(open("../expand/res_9.pkl","rb"))
rob={}
for n in range(4,10):
    items=[]
    for D in itertools.combinations(range(-n+1,n),n):
        if not valid(D) or not canon(D): continue
        L=res.get(tuple(D),[])
        r=[x for x in L if x[2]=="robust"]
        if not r:
            items.append({"D":list(D),"W":len(wits(D)),"w":list(sorted(wits(D))[0]),"why":"no block shrinks to a valid smaller witness" if not L else "every candidate collides or splits"})
    rob[n]=items
E.append(dict(id="robust",title="Robust expansion",short="Does D have a smaller arrangement D′ with marked stones such that every witness of D′ expands to a witness of D?",
  long="Blocks 21, 132, 213, 321. For each smaller arrangement D′ and choice of marked stones, expand every witness of D′. Robust: all of them give witnesses of the same D. Listed: arrangements (no tight cut, up to mirror) with no robust expansion.",kind="primes",data=rob))
# frame set
frames=[(1,2),(2,4,1,3),(4,2,5,1,3),(4,6,2,5,1,3),(5,2,6,4,1,3),(2,5,3,1,4),(5,7,3,6,1,4,2),(3,6,2,5,1,4),(6,3,7,5,1,4,2),(5,7,2,6,4,1,3),(5,7,2,4,6,1,3),(6,8,4,7,2,5,1,3),(3,1,5,2,4),(5,1,3,6,4,2),(3,6,1,4,2,5),(2,6,3,5,1,4),(5,2,6,3,1,4),(7,5,8,2,6,4,1,3),(5,2,4,6,1,3),(6,2,5,7,4,1,3),(5,7,3,1,6,4,2),(7,4,8,6,2,5,1,3),(6,8,3,7,5,1,4,2)]
cov=[102,51,33,14,12,9,8,5,4,4,4,4,3,3,3,3,2,2,1,1,1,1,1]
fr={}
for f,c in zip(frames,cov):
    d=[f[i]-i-1 for i in range(len(f))]
    fr.setdefault(len(f),[]).append({"w":list(f),"cov":c,"bin":len(set(d))==len(d)})
E.append(dict(id="frames",title="Smallest frame set (greedy)",short="Which block-free outer permutations (frames) are needed so every arrangement except P_n is some frame with blocks filled in? n ≤ 9.",
  long="Every permutation is uniquely a frame with blocks filled in (frames 12/21 for corner gluing). For every no-tight-cut arrangement except P_n with n ≤ 9, collect the frames of its witnesses, then pick frames greedily (most arrangements covered first) until all are covered. Grouped by frame size; 'covers' = arrangements newly covered when picked. Frames that repeat a diagonal are marked.",kind="frames",data=fr))
r=rrun(frames)
rec={n:[{"D":list(D),"W":W,"w":list(p)} for D,W,p in v["miss"]] for n,v in r.items()}
E.append(dict(id="recursive",title="Recursive build from the frame set",short="Using only the frame set (plus 12, 21) at every level, which arrangements get built?",
  long="A witness is buildable if its frame is in the set (or 12/21) and each of its blocks is buildable, recursively. An arrangement is reached if some witness is buildable. Listed: arrangements (no tight cut, up to mirror) not reached. Block counts are over witnesses whose top frame is in the set.",kind="primes",data=rec,
  stats={n:{"reached":len(v["reach"]),"missed":len(v["miss"]),**v["blk"]} for n,v in r.items()}))
json.dump(E,open("library.json","w"),ensure_ascii=False)
for e in E: print(e["id"], {n:len(v) for n,v in e["data"].items()})
