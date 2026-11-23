# Instructions for agents (Devin, Claude, others)

1. Read, in this order:
   - `README.md`
   - `docs/claims-map-guide.md` (the principles; mandatory)
   - `docs/state.md`
   - `map/graph.json`
2. Before starting a line of work, find its node in `map/graph.json`. Check its status, its evidence, and its red children: specific attempts that already failed, with counterexamples. Don't redo a red child without a new idea.
3. Report each task as **HIT** or **NOTHING**, using the format in `docs/delegation-queue.md`. A HIT states a precise claim, its exact range, and a recheck command that runs in under 10 minutes.
4. If you change the graph:
   - edit `map/build.py` and run `python3 map/build.py`;
   - make every new node a single precise statement, with exposition first and the claim at the end of `intuition`;
   - when an attempted rule fails, add it as a red child; leave the parent open;
   - follow the invariant / start / step template for inductions;
   - make sure every board picture is a valid witness of its D;
   - update the matching line in `docs/state.md`.
5. Put code and outputs in `agents/<task-name>/`. Shared definitions and helper code are listed in `agents/SETUP.md`.
6. Definitions that are easy to get wrong:
   - **Minimal move:** stones at a < b, with a+1 and b−1 empty and every mark strictly between occupied, move to a+1 and b−1. Moves with b = a+3 alone reach nothing from the start.
   - **Valid:** Landau holds, with equality at k = n.
   - **No tight cut:** strict inequality for every k < n.
   - **Mirror:** D ~ −D.
