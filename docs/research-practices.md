# Research practices

## Where things live
- **Claims graph:** `map/build.py` → `map/graph.json`, viewed in `map/index.html`. The rules are in `docs/claims-map-guide.md`.
- **Research state:** `docs/state.md`. This is canonical. When a result changes what we believe, edit the relevant line; don't append logs.
- **Experiments:** each one gets a folder under `agents/<name>/`, containing its code, its outputs and a short summary.
- **Side tasks:** `docs/delegation-queue.md`.

## Recording experiments
Record each experiment like this:
- **Question:** one sentence.
- **Method:** exactly what was enumerated or searched, the n range, whether it was exhaustive or sampled (with sample size and seed), and the key definitions. Watch the definitions: for example, a "minimal move" means the general cover relation, not only moves of stones 3 apart.
- **Result:** the numbers, plus the smallest counterexample or example.
- **Script:** the file name.

Then update the matching node in the claims graph: its status, its evidence, or a new red child.

## Keep it simple
- Prefer simple, understandable approaches.
- A rule that works 90% of the time and needs a correction for another 9% is probably a dead end. Look for the idea that covers everything.
- If an experiment can't be explained in a short paragraph, simplify it before running it.
- If an instruction turns out harder than it sounds, explain why instead of building a workaround.

## Standing reductions
- **Skip arrangements that split.** A tight proper prefix splits D into two smaller instances whose witnesses glue together (proved). So only D with no tight cut need work.
- **Mirror halving.** Transposing a witness negates D, so check only one of D and −D. Use as canonical the D whose x-ray vector is lexicographically ≥ its reverse. Reflecting across the anti-diagonal fixes the x-ray, so it is not a symmetry to use.

## Interactive labs
- Avoid big dropdowns. Use arrows, a randomize button, or a "random interesting case" button instead.
- Keep only UI with a logical purpose.
- Use a 45°-rotated board when the x-ray must line up under the matrix.
