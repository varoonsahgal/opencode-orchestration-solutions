# Panic Pantry — Solutions

Reference solutions for **Orchestration Fundamentals for Agentic Development** (OpenCode 1.18.33).

Fell behind, or want to compare your work? Each branch holds a finished solution, so you can start the next exercise from a known-good state.

> **Try the exercise yourself first.** You learn this material by making the decisions, not by reading someone else's. Use a solution to catch up, or to compare once you're done.

## What's on each branch

The branches build on each other: each one includes everything from the branches before it.

| Branch | Solution to | Adds | Start this next |
|---|---|---|---|
| `main` | — | The untouched Panic Pantry shop (same as the course's `starter` tag) | Module 0 |
| `module-1-solution` | Module 1, Split the Job | `workshop/plan.md`, `workshop/cards/builder.md`, `workshop/cards/breaker.md` | Module 2 |
| `module-2-solution` | Module 2, Build the Crew | `.opencode/agents/` (implementer, breaker, reviewer, lead), `.opencode/commands/review-ticket.md` | Module 3 (and Module 4) |
| `module-3-solution` | Module 3, Execute the Crew | `src/panic_pantry/importer.py`, `tests/test_promo_import.py`, `workshop/integration-notes.md` | Module 5 |

## How to use a solution in your course setup

You already have the course set up: `sandbox/panic-pantry` plus the two worktrees that `setup.sh` made. Don't replace any of that. Instead, add this repo as a second remote and copy a solution's files into the folder where the next exercise runs.

You don't switch branches with `git checkout <branch>`, because your folders must stay on the course's own `starter` commit for the Module 0 vs Module 3 comparison to be fair. `git restore --source=<branch>` copies just the files you name from that branch into your folder and leaves everything else alone.

### Step 1: add the solutions remote (once)

From the course root:

```bash
cd sandbox/panic-pantry
git remote add solutions https://github.com/varoonsahgal/opencode-orchestration-solutions.git
git fetch solutions
```

Both worktrees share this repository, so the remote works in `sandbox/worktrees/orchestrated` too.

### Step 2: copy in the solution you need

> ⚠️ These commands **overwrite** any file with the same name. If you have your own version you want to keep, copy it somewhere first.

**Starting Module 2** (you need the Module 1 plan and cards). In `sandbox/panic-pantry`:

```bash
git restore --source=solutions/module-1-solution -- workshop/plan.md workshop/cards
```

**Starting Module 3 or Module 4** (you need the plan, cards and agents). In `sandbox/panic-pantry`:

```bash
git restore --source=solutions/module-2-solution -- workshop/plan.md workshop/cards .opencode
```

Then follow Module 3 as written: step A2 copies the agents and cards into the orchestrated worktree for you.

**Starting Module 5** (you need the finished Module 3 run). In `sandbox/worktrees/orchestrated`:

```bash
git restore --source=solutions/module-3-solution -- \
  workshop/plan.md workshop/cards .opencode \
  src/panic_pantry/importer.py tests/test_promo_import.py workshop/integration-notes.md
git add src/panic_pantry/importer.py tests/test_promo_import.py
```

The `git add` stages only the product files, as Module 3 step B4 does. Keep `.opencode/` and `workshop/` unstaged: they're the experiment harness, not the product.

### Step 3: check it worked

```bash
git status --short                  # the new files appear
python3 -m unittest discover -s tests -v
```

After the Module 3 solution, also run the gates:

```bash
bash scripts/gate.sh builder
bash scripts/gate.sh breaker
bash scripts/gate.sh integration    # all three should print PASS
```

## Just want to look?

Browse a branch on GitHub with the branch menu, or clone the repo and switch between branches:

```bash
git clone https://github.com/varoonsahgal/opencode-orchestration-solutions.git
cd opencode-orchestration-solutions
git checkout module-3-solution
python3 -m unittest discover -s tests -v
```

Compare two branches to see exactly what one module added:

```bash
git diff module-1-solution module-2-solution --stat
```

## Notes on the solutions

- **Module 1:** the cards are the course's revealed answers plus two Stranger Test fixes. The header rule is now part of the shared contract (in the plan and both cards), and the Breaker card says how to detect a direct write to the JSON store.
- **Module 2:** the agents enforce the capability matrix from Module 2. Lead can delegate only to the three specialists. `review-ticket.md` is the optional Level up command.
- **Module 3:** `importer.py` passes all 9 contract tests and creates every promotion through `PromotionService.create_promotion`. It never compares a discount to 20 itself. `test_promo_import.py` was written from the ticket alone and skips every test while `importer.py` is missing. `integration-notes.md` shows a real gate log from this solution. Its scorecard rows for model, interventions and time are left for you to fill in, because they come from your own run.
- Model output varies from run to run. Your crew's code won't match this code line for line, and that's fine. What matters is that it passes the same gates.

## Running the shop

Pure Python 3, standard library only, fully offline:

```bash
python3 -m unittest discover -s tests -v   # run every test
bash scripts/reset.sh                      # restore seed data, remove the importer
bash scripts/score.sh                      # the scorecard's measured rows
```
