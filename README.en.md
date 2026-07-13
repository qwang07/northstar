# northstar

[简体中文](README.md) | English

> The Chinese [README.md](README.md) is the source of truth; this English version is a projection and may lag.

A Claude Code plugin marketplace. **The README is the single, timeless source of target-state truth; tests are its executable projection; history is traceable but never authoritative.**

The AI bottleneck has moved up from "implementation" to "design + test completeness." This framework concentrates all firepower on one thing: **declaring the requester's intent completely in the README** — the design and test bottlenecks collapse into this single act. The loop is split by **activity**: contract dialogue (brainstorming) → derive guards (write-test) → independent review (audit) → turn red green (implement); defects enter through the diagnose attribution gate, and code-review delivers the closing quality cut. **All six skills and six execution subagents are self-authored with zero external plugin dependencies (no superpowers or any other engine); it runs standalone once installed.**

## Install

```bash
/plugin marketplace add qwang07/northstar
/plugin install northstar@northstar
```

After install, the six skills appear namespaced: `northstar:brainstorming` / `:write-test` / `:audit` / `:implement` / `:diagnose` / `:code-review`; on the Claude Code side, six execution subagents register with the plugin: `ns-scout` / `ns-diagnostician` / `ns-auditor` / `ns-implementer` / `ns-simplifier` / `ns-reviewer`.

Codex CLI side: skills install via the in-repo plugin manifest; agents are in-repo TOML files, copied once into the user's agents directory per the install guide (`docs/codex-install.md`, with tested commands and the pinned-model table — clauses in the Cross-platform topology section).

## Structure

```
northstar/
├── .claude-plugin/marketplace.json     Claude Code catalog
├── plugins/northstar/
│   ├── .claude-plugin/plugin.json      manifest
│   ├── skills/
│   │   ├── brainstorming/SKILL.md      contract phase: dialogue into README (sole write entry, clauses land at their authoritative layer)
│   │   ├── write-test/SKILL.md         test phase: derive tests or a verification checklist from the README
│   │   ├── audit/SKILL.md              independent review: zero-context audit (two checkpoints)
│   │   ├── implement/SKILL.md          turn red green: means chosen by scale
│   │   ├── diagnose/SKILL.md           defect entry: attribution before any fix, exits routed back into the loop
│   │   └── code-review/SKILL.md        closing quality cut: zero-context code-quality review
│   └── agents/
│       ├── ns-scout.md                 read-only retrieval (haiku)
│       ├── ns-diagnostician.md         diagnose-phase attributor (opus)
│       ├── ns-auditor.md               audit-phase zero-context reviewer (opus)
│       ├── ns-implementer.md           implement-phase module executor (sonnet)
│       ├── ns-simplifier.md            wrap-up simplification pass (opus)
│       └── ns-reviewer.md              code-review-phase zero-context reviewer (opus)
├── <Codex distribution & binding>      in-repo plugin manifest + agents TOML + install guide (manifest path & TOML schema follow Codex platform conventions; directory layout is implementation freedom)
├── README.md
└── README.en.md
```

## Rhythm

```
(defect) ──▶ diagnose ── attribute & route ─▶┐
(new need) ─────────────────────────────────▶ brainstorming ──▶ write-test ──▶ audit ──▶ human gate ──▶ implement ──▶ wrap-up
                                              (contract·README)  (tests/checklist) (zero-context)        (red→green)   (simplifier→code-review)
                                                 ▲     ▲               ▲                                     │
                                                 │     └─ contract-gap kickback ┴── test-gap kickback ◀──────┘
                                                 └──────────── close-out (project exit gate) ◀── all modules done
```

- **The split axis is activity; the round is defined by its goal**: contract dialogue / test writing / review / implementation each own a phase. Contract clauses land at their authoritative layer — project-level (topology and boundaries) / cross-cutting layer (constraints shared by multiple modules, existing on demand) / module-level (internal behavior); altitude is a landing result, not an entry parameter.
- **Granularity valve**: if this round's goal requires expanding the internal contracts of more than one module → the round stops at decomposition (sub-goal list + project-level / cross-cutting clauses); each sub-goal becomes its own later round of `brainstorming → write-test → audit → implement`.
- **Test-free branch**: pure one-off operations (migrations / backfills / one-shot scripts) get no derived tests; write-test instead produces a **mechanically decidable verification checklist**, audited alongside the README; implement's completion criterion is passing the checklist item by item.
- **Two audit checkpoints**: after brainstorming finalizes the README (cross-module goals: audit the contract first, saving derivation rework) + after write-test completes (README + tests / checklist reviewed together); single-module goals may merge into one combined review.
- **Close-out**: all modules done → return to brainstorming to close out — architecture structure tests all green + a re-run of the business-flow walkthrough = the project-level exit gate (loop terminal).
- **Loop convergence valve**: any back-edge retriggering on the **same gap** up to a threshold (default 3) without converging → BLOCKED: stop auto-kickback, escalate to a human, attach that gap's kickback history (process-state, goes to git/Linear, never into the contract).

## Usage

Advance one scope at a time; describe your intent in chat to trigger the matching skill:

- **New project**: `brainstorming` (a cross-module goal) designs the topology (module list + dependencies + interface contracts), gated by `audit`, then per module `brainstorming → write-test → audit → implement`; when all are done, `brainstorming` closes out.
- **Existing project**: `brainstorming` first distills the existing structure and asks whether to adjust; once the target state is set, proceed as above.
- **Bug fix**: an unexplained red or production defect first enters `diagnose` for attribution, then routes by exit (implementation wrong → implement; contract gap → brainstorming; test wrong / weak assertion → write-test).
- **Small change**: a pure-implementation small change goes straight to `implement` in-session; a change that touches the contract goes back to `brainstorming` for the README and `write-test` for the tests first, then implement.

Division of labor: in the contract and test phases, **the human** interrogates the requester's intent to completeness and confirms the contract; **the skills** turn the contract into guards and the red green. In one line — **the human defines the contract, the AI turns red to green.**

## The six skills

| skill | phase | responsibility | output |
|---|---|---|---|
| `brainstorming` | contract · sole README write entry | open with the goal, interrogate intent to completeness (one question at a time); distill existing code before asking to adjust; business-flow walkthrough before finalizing; close out when all modules are done | README clauses landed by goal: project-level (module list + topology [each edge carries an interface contract] + boundary interfaces, **no internals**) / cross-cutting layer (constraints shared by multiple modules, on demand) / module-level (responsibility & boundary / expected features / interface contract / edge cases & invariants, **internals only**) |
| `write-test` | test · derivation | branch decision (needs lasting guarding → tests; one-off → verification checklist); test intent, not implementation; strong-assertion discipline | standalone test files (initially red: business-intent tests + structure tests [modules exist / interfaces visible / lasting invariants]) or a mechanically decidable checklist |
| `audit` | review · independent | **zero-context (hard requirement, must dispatch a subagent)** review of design artifacts; two checkpoints; gaps routed back upstream | pass / gap list (gates handoff). Five checks: completeness · contract↔test consistency · boundary hygiene · internal consistency · **assertion strength** |
| `implement` | implementation · scale-adaptive | full micro-loop: verify-red→green→verify-green(regression)→refactor → contract gate → verify (edit in session / dispatch one executor / parallel orchestration, by scale); test-free branch completes by passing the checklist item by item | implementation code |
| `diagnose` | defect entry | attribution before any fix; evidence → pattern comparison → hypothesis testing → routing | reproducing red test (→implement) / contract gap (→brainstorming) / test-fix list (→write-test) / external-issue record |
| `code-review` | wrap-up · quality cut | zero-context code-quality review (latent bugs / silent failures / maintainability), anchored to the module README as spec; finding handling: verify → satisfy / kick back / rebut with evidence | severity-ranked findings + explicit verdict (ready to wrap up / fix first) |

## Design philosophy (core axioms)

- **Two bottlenecks collapse into one**: AI implementation is production-ready; the real problems are ① system design ② test completeness, both equivalent to "declaring intent completely in the README." All skill firepower goes here.
- **Split by activity, the goal defines the round**: contract dialogue, test writing, review, and implementation are four activities, each owning a phase; the round is defined by its goal (what to achieve, what counts as achieved), and project-level / cross-cutting / module-level are merely the layers where clauses land. One activity is never split into two skills by altitude — that breeds the mirror tax.
- **Sole README write entry**: only brainstorming may write READMEs; audit / write-test / implement / diagnose treat them as read-only and kick gaps back. Companion rule: one authoritative statement + pointers, no restating across READMEs.
- **Temporal-semantics layering**: target-state (README + tests, bounded, sole truth) vs process-state (git log / Linear / memory tools, monotonically growing, traceable but not authoritative).
- **Target-state splits into two properties**: timeless (describes the current should-be state, not a changelog — **kept**) ≠ history-less (destroying decision rationale — **rejected**). Rationale is process-state, routed out rather than deleted; a load-bearing constraint keeps a **one-token marker** (`[承重·勿删]`) in the hot doc, while the rationale itself goes to the workflow (memory/issues).
- **Zero overlap across layers**: the README tree is layered by the project's real structure — the project level owns topology (module set + dependency edges, pure structure), cross-cutting layers own constraints shared by multiple modules (existing on demand), the module level owns behavior (given input, output matches intent); every clause is declared once at its authoritative layer, lower layers receive it by pointer. The same information at two layers = a seed of drift.
- **Seam closure**: every topology edge carries an interface contract I; I is declared once at the project level, and the upstream output test and downstream input test both target the same I → semantic compatibility is locked from both sides, **no separate integration layer needed**. Structure tests verify only "modules exist + interfaces visible + lasting invariants," **not the real dependency graph and not runtime wiring**; the latter is the integration layer — YAGNI by default, done only when the README explicitly declares system-level intent as integration behavior tests.
- **Business-flow walkthrough**: each phase owns one segment; nobody naturally owns walking a business flow end to end — broken links (swallowed-error loops, signals with no consumer, dangling states) are invisible to any single phase. So brainstorming, at finalize and close-out, treats the README contract web as a state machine and walks every flow's forward, reverse, and exception paths looking for the receiving contract at each step.
- **Strong-assertion discipline**: a test whose assertion is vacuous has zero discriminating power — worse than no test (it fakes coverage). write-test bans vacuous assertions / status-code-only checks / loose enum matching / unlocked precision; audit's fifth check targets assertion strength.
- **Two-level exit gates**: module-level = implement's contract-conformance gate (implementation exactly == module contract); project-level = brainstorming's close-out gate (structure tests all green + business-flow walkthrough passes = loop terminal).
- **Loop convergence valve**: any back-edge retriggering on the same gap up to a threshold (default 3) without converging → BLOCKED, escalate to a human, attach kickback history (process-state, routed out); no infinite kickback.
- **Test-scope iron rule**: go by the intent declared in the README. Implementation details are **not tested** by default (implementation is free); only when the README explicitly promotes an implementation constraint to a requirement is it tested. The criterion is not "is this implementation?" but "did the README declare it?"
- **Anti-cheat gate (implement invariants)**: tests and review findings are read-only to the execution loop — no tampering, no pre-judging, no softening; a wrong test is kicked back upstream, never silently patched in the loop.
- **Attribution before fixing**: no defect gets fixed without attribution; "it looks like X, so change X" is what diagnose exists to eliminate. Fixes always happen in implement; diagnose only produces handoff artifacts.

## Cross-platform topology: single-source dogma, dual-written bindings

northstar ships for two platforms, Claude Code and Codex CLI. Three layers, connected by interface contracts:

```
Dogma layer    plugins/northstar/skills/ six SKILL.md — single source, platform-agnostic
   ▲ via the I-platform-capability table
Binding layer  Claude Code: plugins/northstar/agents/*.md (frontmatter pins opus/sonnet/haiku)
               Codex: agents TOML (per the platform agent schema, pinning concrete models + reasoning-effort tiers)
   ▲
Distribution   Claude Code: .claude-plugin/ marketplace
               Codex: in-repo plugin manifest (per the platform convention .codex-plugin/plugin.json); agents ship with the repo (not in the plugin) + one-time install guide
```

Binding layer = agent definitions + a **platform execution note** (one per platform: the item-by-item delivery declaration for the capability table, the platform-specific execution details extracted from the dogma, and platform prerequisites all live here; dogma text references it by pointer, location is implementation freedom). The criterion for "platform-specific": a platform's **named forms** of the three execution shapes ("edit in session / dispatch one executor / orchestrate parallel executors") and their isolation mechanics are extraction targets; cross-platform abstract concepts (subagent, dispatch, read-only retrieval) stay in the dogma.

**I-platform-capability table** (the dogma↔binding interface contract): dogma text expresses platform actions only in abstract verbs; each binding layer declares, item by item, how its platform delivers —
1. Dispatch a zero-context subagent (the two cuts: audit / code-review)
2. Dispatch a module-level executor (implement) and an attributor (diagnose)
3. Read-only retrieval
4. Wrap-up simplification pass
5. Model / reasoning-effort tiering: judgment high (review / attribution / simplification), execution medium, retrieval low

**Cross-cutting constraints (shared by both bindings)**:
- Dogma text must contain no platform-specific names (tool names / config fields / invocation syntax) — enforced as a mechanically assertable lasting invariant
- Each binding delivers every item of the capability table; any undeliverable item = that step explicitly unavailable on that platform, silent degradation forbidden (the zero-context item defers to the BLOCKED axiom in the next section, pointer not restatement)
- Loop orchestration is always "main session → one layer of subagents"; no skill may require a subagent to dispatch further subagents
- The Codex binding pins concrete models: the install guide must state the required models and note that users may change models / tiers in their local copies; the release process includes "verify pinned models are still valid" `[load-bearing, keep]`

## Plugin boundary: dogma + execution bindings (two zero-context cuts share one platform primitive)

The plugin = six skills (dogma, tool-agnostic) + six subagents (execution bindings: per-phase executors and model tiering; shipped with the plugin on the Claude Code side, and as the same definitions in TOML shipped with the repo on the Codex side — see the Cross-platform topology section; both under version control, no longer stray files). Platform dependency: `audit` and `code-review` must dispatch a **zero-context subagent** (a native capability, but still a dependency — the in-session agent remembers the design conversation and can't be truly zero-context); when the environment can't dispatch one, that step is not executable — BLOCKED to a human, never downgraded to self-review. Everything else below stays **out of the plugin** and is the user's personal global CLAUDE.md workflow config:

- **Process-state routing** (where rationale / todos / history go): bind memory tools / Linear / git. Skills only declare "process-state stays out of the contract, routed out," not where to.
- **Contract-conformance review** (does the implementation exactly == the contract) is the opposite — it's framework dogma, self-issued by `implement`'s exit gate, not outsourced.

## Independence: self-contained, no external engine

All six skills and six subagents are self-authored, **depending on / reusing / pinning no external plugin** (including superpowers and other official engines; the ns-simplifier pass was digested from the official code-simplifier and re-authored, with a source line kept in its definition file). northstar runs standalone once installed.

**Why no external engine**: borrowing an off-the-shelf TDD / review engine was considered and dropped after a fit assessment — "don't reinvent the wheel" holds only when it's "redundant and unnecessary," and northstar needs things an external engine can't give:

- the "test itself is wrong → kick back to brainstorming / write-test to regenerate" loop, plus subagent model-tiering — generic engines lack these;
- "test before implementation" is already **structurally guaranteed** by the pipeline order (README → tests → implementation), making the engine's core value redundant here.

So each skill self-authors a thin layer that nails only its own loop and invariants, without rebuilding an engine. Absorbed external methodology (the brainstorming / write-test dialogue and derivation paradigms, systematic-debugging → diagnose, receiving-code-review → code-review's handling section, writing-skills' naive-agent pressure test → this repo's acceptance gate for skill texts) is credited in a provenance line at the end of each SKILL.md — traceable, not vendored.

### Claude Code plugin mechanism facts (measured)

- **Skill discovery = pure directory convention**: `plugin.json` doesn't list skills; dropping in `skills/<name>/SKILL.md` makes it discoverable. Adding a skill only creates a directory — no manifest change.
- **Skill cross-calling = semantic relevance + the platform Skill tool**, not hard paths. The loop (implement kicks back to write-test, audit kicks back to brainstorming) just needs to name them in prose — no dependency declaration.
- **Override priority = user instructions (CLAUDE.md) > plugin skill > default**: your CLAUDE.md naturally outranks any plugin skill; conflicts are resolved by mechanism.
- **Version pinning** relies on the `gitCommitSha` recorded at install time (`~/.claude/plugins/installed_plugins.json`), not at the marketplace.json level.
