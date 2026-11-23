# unimodal: working notes (branch devin/1795452588-unimodal, base devin/1795444188-two-marks; COUNT parked, PR #12 merged)
Task (parent): prove the conjecture for UNIMODAL words (letters >= 0 then letters <= 0), or a smaller infinite family
with unbounded slack, by hand.  Deliver agents/unimodal/REPORT.md (HIT/NOTHING), PR into devin/1795444188-two-marks,
do not touch map/build.py or docs/state.md.  Small runs only.  Items: (1) exact description of F(x) for nonnegative
prefixes (residue counts, staircases, 1^a 0^b, 2^a 1); (2) restricted universal states U+(s); (3) proof.
Conventions: word letter e_k = d_k - 2k, stones sorted by diagonal; brute-force helper ../runrule/countlib.py (solutions(n)).
## Ideas so far
- full run (a,..,1,0,-1,..,-a), n = 2a+1: cyclic shift sigma(i) = i + a mod n solves it (sums 2i+a and 2i-a-1).
- pure shift fails for staircase-zeros-staircase with j > 1 zeros (odd diagonals not contiguous).
- plan: print brute-force solutions of small members of families  1^a 0^j (-1)^a  and  (a..1) 0^j (-1..-a)  and look for a
  structured solution (centrally symmetric / block pattern), then prove by explicit formula.

## Hand work so far (nothing proved for a NEW family yet)
- 1^a 0 (-1)^a, n = 2a+1: the n-cycle sigma(i) = i+1, sigma(n) = 1 solves it (sums 2i+1 and n+1).  [same as the full-run shift idea]
- (1,1,0,0,-1,-1): sigma(i) = 2i mod 7.  Multiplication maps i -> c i mod (n+1) give other families (see agents/prime? check before claiming new).
- target family T(a,j) = 1^a 0^j (-1)^a (slack a unbounded): D = odds 3..2a+1, evens 2a+2..2a+2j, odds 2a+2j+1..4a+2j-1, n = 2a+j.
  skeleton 'up-steps (i,i+1) i<=a, down-steps (r,r-1) r>a+j, zeros in the middle' reduces to a j x j problem
  p + tau(p) + a[p=j] - a[tau(p)=1] = evens 2..2j, solvable by near-fixed-points only when j >= a+2 (needs p0 >= a+1, q <= j-a);
  skeleton with zeros as fixed points (a+t,a+t) and one cross pair works only when a = j+1 (e.g. (2,3,8,4,5,1,6,7) for a=3,j=2).
  small j needs another skeleton (j=1 cycle, a=j=2 doubling map).
- look.py prints (centrally symmetric) brute-force solutions of a word.
NEXT: (1) grep agents/prime, agents/blocks, docs/state.md for families already proved (linear maps, L_1, blocks) to avoid re-proving;
(2) search computationally for a uniform explicit construction for T(a,j) (all a,j <= 6): e.g. solutions made of up-steps, down-steps,
fixed points and O(1) long stones; print the 'step type' sequence of each solution and look for a pattern uniform in (a,j);
(3) alternatively items 1-2 of the task (F(x) for nonnegative prefixes, U+(s)) with ../interface machine (cstep / rewrite.machine);
(4) REPORT.md + PR.
