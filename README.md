# Binary x-rays of permutations

This repo is research notes, data and code for **Bebeacua–Mansour–Postnikov–Severini Conjecture 5 / Nordh Conjecture 10**. The conjecture: a set D of n distinct diagonals (d = column − row) of the n×n board is the diagonal x-ray of a permutation if and only if s_k = d_k + n − k is a tournament score sequence (Landau's condition). Necessity is known. Sufficiency has been verified for n ≤ 22 and is open.

## What's here

| Path | For | What it is |
|---|---|---|
| `map/graph.json` | agents | **The claims graph.** Every node is one precise claim with a status (proved / empirical / open / disproved / idea). Edges are logical implications; an array `from` is an ∧-junction. This is the canonical machine-readable map of what is known, what was tried, and how it fits together. |
| `map/index.html` | humans | Interactive view of the same graph. Tap a node for its card: exposition, pictures, the precise statement, proof sketch or evidence, and its route to the conjecture. Serve the folder (`python3 -m http.server` in `map/`) and open `index.html`. Hosted copy: https://claude.ai/artifact/2pe8j5i5QgKJ5ouVYGJoRY |
| `map/build.py` | both | **Source of truth for the graph.** Edit here, then run `python3 build.py`; it writes `graph.json`. Proof sketches live in `proofs.json`. |
| `docs/claims-map-guide.md` | both | **Principles and rules for the graph. Read before adding anything.** |
| `docs/state.md` | agents | Dense research state: every result with its range and script, the open lines, and what's ruled out and why. |
| `docs/research-practices.md` | both | How we run and record experiments. |
| `docs/delegation-queue.md` | agents | Side tasks for outside agents, and how to report. |
| `agents/` | agents | Code and outputs from every experiment, one folder per investigation (see `agents/SETUP.md` for the shared definitions). |

## The principles in one screen

The full version is in `docs/claims-map-guide.md`.

1. **Every node is one precise logical statement**, such as "for every …, there exists …" or "if …, then …". It is never a topic, a description or a construction. Constructions are stated as if–then lemmas.
2. **Status refers to exactly that statement.** "Ruled out" means a counterexample to that exact statement is known; it never means "we searched and found nothing".
3. **Don't refute something too strong and move on.** If a search for a rule fails, the parent claim (a weaker existence statement) stays open, and the specific failed rules hang under it as red children. We never write "a simple rule exists" nodes. "Some procedure works" is trivially true if the conjecture is, and "simple" isn't defined.
4. **Induction routes follow one template.** An invariant P comes with three claims:
   - start: the initial state has P;
   - step: every unfinished state with P has *some* next step keeping P;
   - exact at the end: a finished state with P is a solution.

   Start and step are separate nodes joined by ∧; specific step choices are children of the step node. Every invariant says why it isn't the conjecture in disguise.
5. **Cards are for humans.** Exposition first: define the notion, give an example picture specific to this claim, then say the claim in plain words. Numbers go in `evidence`, proofs in `proof`. A card describes only its own claim.
6. **Explicit case splits.** Use named sets joined by ∧ (e.g. symmetric vs non-symmetric; odd vs even n). Never use "settles part of" edges.

## Working conventions

- **Standing reductions:** only D with no tight cut matter (tight cuts split), and D ~ −D (mirror).
- **Recording experiments:** every experiment gets a folder in `agents/` and a line in `docs/state.md`. The line gives the exact question, the range, whether the check was exhaustive, the smallest counterexample, and the script name.
- **Reporting:** return HIT or NOTHING (see `docs/delegation-queue.md`). A rule that is right 90% of the time is not a hit.
- **Updating the graph:** add or change nodes in `map/build.py`, run it, check that the pictures are valid witnesses, and keep the statement, status and evidence consistent with `docs/state.md`.
