# northstar

[简体中文](README.md) | English

A Claude Code plugin marketplace. **The README is the single, timeless source of target-state truth; tests are its executable projection; history is traceable but never authoritative.**

The AI bottleneck has moved up from "implementation" to "design + test completeness." This framework concentrates all firepower on one thing: **declaring the requester's intent completely in the README** — the design and test bottlenecks collapse into this single act. Implementation is handed to a scale-adaptive execution form; code-quality chores are left to the workflow and stay out of the plugin. **All four skills are self-authored with zero external plugin dependencies (no superpowers or any other engine); it runs standalone once installed.**

## Install

```bash
/plugin marketplace add TODO-your-account/northstar
/plugin install northstar@northstar
```

After install, the four skills appear namespaced: `northstar:architect` / `:module` / `:audit` / `:implement`.

## Structure

```
northstar/
├── .claude-plugin/marketplace.json     catalog
├── plugins/northstar/
│   ├── .claude-plugin/plugin.json      manifest
│   └── skills/
│       ├── architect/SKILL.md          architecture layer: topology design + structure test (re-entrant)
│       ├── module/SKILL.md             module layer: internal behavior contract + intent tests (loop)
│       ├── audit/SKILL.md              independent review: zero-context audit of design artifacts
│       └── implement/SKILL.md          turn red green: means chosen by scale
└── README.md
```

## Rhythm

Start with `architect` → `audit` (project-level, once) → then loop per module `(module → audit → implement)`.

```
architect ─▶ audit ─▶ module ─▶ audit ─▶ implement ─▶ next module
            (project)          (module)                    │
    ▲          │        ▲          │                       │
    │ bad boundary /    │ incomplete /        test wrong   │
    │ incomplete        │ contract defect     = defect     │
    └──── kick back ◀───┴───── kick back ◀──────────────────┘
```

All modules done → **architect closes out by confirming the architecture structure test is all-green = the project-level exit gate** (supplying the project terminal the loop originally lacked).

**Loop convergence valve**: any back-edge (architect re-entry / module kickback / implement test kickback) that retriggers on the **same gap** up to a threshold (default 3, aligned with CLAUDE.md §33a) without converging → BLOCKED: stop auto-kickback, escalate to a human, and attach that gap's kickback history (what each prior attempt's gap was and how it was fixed; process-state, goes to git/Linear, never into the contract).

## Usage

Advance one scope at a time; describe your intent in chat to trigger the matching skill:

- **New project**: start from `architect` — design the system topology (module list + dependencies + interface contracts), gate through `audit`, then loop each module `module → audit → implement`; `architect` closes out when all are done.
- **Existing project**: `architect` first distills the existing structure and asks whether to adjust; once the target state is set, proceed as above.
- **Bug fix / small change**: a pure-implementation small change goes straight to `implement` inline; a change that touches the contract goes back to `architect` / `module` to revise README + tests first, then implement.

Division of labor: in the architect/module phases, **the human** interrogates the requester's intent to completeness and confirms the contract; **the skills** turn the contract into tests and the red green. In one line — **the human defines the contract, the AI turns red to green.**

## The four skills

| skill | layer | responsibility | output | tests |
|---|---|---|---|---|
| `architect` | arch · re-entrant | new: design topology / existing: distill + ask to adjust | project README (module list + dependency topology [each edge carries an interface contract] + boundary interfaces, **no internals**) | architecture structure test (modules exist as units + declared public interface visible, **pure structure · tool-agnostic**; does not verify the real dependency graph — edge semantics already covered by seam contracts) |
| `module` | module · loop | design module-internal behavior contract + derive tests | module README (**internals only**) | business-intent behavior tests (**pure behavior**) |
| `audit` | review · independent | **zero-context (hard requirement, must dispatch a subagent)** audit of design artifacts | pass / gap list (gates handoff) | audit: completeness · contract↔test consistency · boundary hygiene · internal consistency |
| `implement` | implementation · scale-adaptive | complete micro-loop: verify-red→green→verify-green(regression)→refactor → contract gate → verify (inline / subagent / workflow by scale) | implementation code | module-level exit gate self-issues the "contract conformance" check + empirical verification |

## Design philosophy (core axioms)

- **Two bottlenecks collapse into one**: AI implementation is production-ready; the real problems are ① system design ② test completeness, both equivalent to "declaring intent completely in the README." All skill firepower goes here.
- **Temporal-semantics layering**: target-state (README + tests, bounded, sole truth) vs process-state (git log / Linear / memory tools, monotonically growing, traceable but not authoritative).
- **Target-state splits into two properties**: timeless (describes the current should-be state, not a changelog — **kept**) ≠ history-less (destroying decision rationale — **rejected**). Rationale is process-state, routed out rather than deleted; a load-bearing constraint keeps a **one-token marker** (`[load-bearing·do-not-delete]`) in the hot doc, while the rationale itself goes to the workflow (memory/issues).
- **Two layers, zero overlap**: the architecture layer owns topology (module set + inter-module edges, pure structure); the module layer owns behavior (given input, output matches intent, pure behavior). The dividing line is the module boundary itself. The same information in both layers = a seed of drift.
- **Seam closure**: every topology edge carries an interface contract I; I is declared once at the architecture layer, and the upstream output test and downstream input test both target the same I → semantic compatibility is locked from both sides, **no separate integration layer needed**. The architecture structure test verifies only "modules exist + interface visible," **not the real dependency graph and not runtime wiring** (A actually calling B ≠ each being stub-compatible); the latter is the integration layer — YAGNI by default, done only when the README explicitly declares system-level intent as integration behavior tests. What isn't declared isn't tested; to test it, declare it in the README first.
- **Two-level exit gates**: module-level = implement's contract-conformance gate (implementation exactly == module contract); project-level = architect's close-out gate (architecture structure test all-green = loop terminal). The state machine's two terminals are symmetric.
- **Loop convergence valve**: any back-edge retriggering on the same gap up to a threshold (default 3, aligned with CLAUDE.md §33a) without converging → BLOCKED, escalate to a human, attach kickback history (process-state, routed out); no infinite kickback.
- **Test-scope iron rule**: go by the intent declared in the README. Implementation details are **not tested** by default (implementation is free); only when the README explicitly promotes an implementation constraint to a requirement is it tested. The criterion is not "is this implementation?" but "did the README declare it?"
- **Anti-cheat gate (implement invariants)**: tests and review findings are read-only to the execution loop — no tampering, no pre-judging, no softening; a wrong test is kicked back upstream, never silently patched in the loop.

## Plugin boundary: pure dogma, tool-agnostic (audit uses one platform primitive)

The plugin = four skills, **dogma-level tool-agnostic and distributable**. The only platform dependency: `audit` must dispatch a **zero-context subagent** (a native capability, but still a dependency — the in-session agent remembers the design conversation and can't be truly zero-context); when the environment can't dispatch a subagent, audit is not executable — BLOCKED to a human, never downgraded to self-audit. Everything else below stays **out of the plugin** and is the user's personal global CLAUDE.md workflow config:

- **Code quality / simplification** (contract-agnostic engineering hygiene): bind code-simplifier, code-review, etc., wired into the post-implement wrap-up.
- **Process-state routing** (where rationale / todos / history go): bind memory tools / Linear / git. Skills only declare "process-state stays out of the contract, routed out," not where to.
- **Contract-conformance review** (does the implementation exactly == the contract) is the opposite — it's framework dogma, self-issued by `implement`'s exit gate, not outsourced.

## Independence: self-contained, no external engine

All four skills are self-authored, **depending on / reusing / pinning no external plugin** (including superpowers and other official engines). northstar runs standalone once installed.

**Why no external engine**: borrowing an off-the-shelf TDD / review engine was considered and dropped after a fit assessment — "don't reinvent the wheel" holds only when it's "redundant and unnecessary," and northstar needs things an external engine can't give:

- the "test itself is wrong → kick back to architect/module to regenerate" loop, plus subagent model-tiering — generic engines lack these;
- "test before implementation" is already **structurally guaranteed** by the pipeline order (README → tests → implementation), making the engine's core value redundant here.

So each skill self-authors a thin layer that nails only its own loop and invariants, without rebuilding an engine. Contract-agnostic generic hygiene such as code quality / simplification is what gets handed to the workflow's off-the-shelf tools (see the previous section).

### Claude Code plugin mechanism facts (measured)

- **Skill discovery = pure directory convention**: `plugin.json` doesn't list skills; dropping in `skills/<name>/SKILL.md` makes it discoverable. Adding a skill only creates a directory — no manifest change.
- **Skill cross-calling = semantic relevance + the platform Skill tool**, not hard paths. The loop (implement kicks back to module, audit kicks back to architect) just needs to name them in prose — no dependency declaration.
- **Override priority = user instructions (CLAUDE.md) > plugin skill > default**: your CLAUDE.md naturally outranks any plugin skill; conflicts are resolved by mechanism.
- **Version pinning** relies on the `gitCommitSha` recorded at install time (`~/.claude/plugins/installed_plugins.json`), not at the marketplace.json level.

> All `TODO-` placeholders must be replaced with your real account/email before pushing to GitHub.
