# northstar

[简体中文](README.md) | English

> The Chinese [README.md](README.md) is the source of truth; this English version is a projection and may lag.

A Claude Code plugin marketplace. **The README is the single, timeless source of target-state truth; tests are its executable projection; history is traceable but never authoritative.**

This framework concentrates all firepower on one thing: **declaring the requester's intent completely in the README** (rationale: see "Design philosophy · Two bottlenecks collapse into one"). The loop is split by **activity**: contract dialogue (brainstorming) → derive guards (write-test) → independent review (audit) → turn red green (implement) → the wrap-up chain (simplify → code-review); defects enter through the diagnose attribution gate. **All seven skills and six execution subagents are self-authored with zero external plugin dependencies (no superpowers or any other engine); it runs standalone once installed. Subagents are split by context-isolation need, not one-per-skill** — brainstorming and write-test are human dialogue and in-place derivation, run in the main session with no subagent dispatched.

## Install

```bash
/plugin marketplace add qwang07/northstar
/plugin install northstar@northstar
```

After install, the seven skills appear namespaced: `northstar:brainstorming` / `:write-test` / `:audit` / `:implement` / `:simplify` / `:diagnose` / `:code-review`; on the Claude Code side, six execution subagents register with the plugin: `ns-scout` / `ns-diagnostician` / `ns-auditor` / `ns-implementer` / `ns-simplifier` / `ns-reviewer`.

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
│   │   ├── simplify/SKILL.md           wrap-up chain, first pass: simplify this round's diff with zero authoring memory
│   │   ├── diagnose/SKILL.md           defect entry: attribution before any fix, exits routed back into the loop
│   │   └── code-review/SKILL.md        wrap-up chain, last pass: zero-context code-quality review
│   └── agents/
│       ├── ns-scout.md                 read-only retrieval (haiku)
│       ├── ns-diagnostician.md         diagnose-phase attributor (opus)
│       ├── ns-auditor.md               audit-phase zero-context reviewer (opus)
│       ├── ns-implementer.md           implement-phase module executor (sonnet)
│       ├── ns-simplifier.md            wrap-up chain simplification pass (opus)
│       └── ns-reviewer.md              code-review-phase zero-context reviewer (opus)
├── .codex-plugin/plugin.json           Codex plugin manifest (its skills field points at the shared dogma layer above)
├── .agents/plugins/marketplace.json    Codex marketplace manifest
├── .codex/agents/                      Codex binding layer: six agent TOMLs (ship with the repo, copied once into the user's directory)
├── docs/codex-install.md               Codex install guide (tested commands + pinned-model table)
├── tests/structure.py                  project-level structure tests (topology shape / binding tiers / forbidden-word invariant / reference integrity)
├── README.md
└── README.en.md
```

## Rhythm

```
(defect) ──▶ diagnose ── attribute & route ─▶┐
(new need) ─────────────────────────────────▶ brainstorming ──▶ write-test ──▶ audit ──▶ human gate ──▶ implement ──▶ wrap-up chain
                                              (contract·README)  (tests/checklist) (zero-context)        (red→green)  simplify → code-review
                                                 ▲     ▲               ▲                                     │      (no authoring memory) (zero-context)
                                                 │     └─ contract-gap kickback ┴─ test-gap / simplify-turned-red ◀───┴──── finding kickback ◀┘
                                                 └──────────── close-out (project exit gate) ◀── wrap-up chain done · all modules done
```

- **The split axis is activity; the round is defined by its goal**: contract dialogue / test writing / review / implementation each own a phase. Contract clauses land at their authoritative layer — project-level (topology and boundaries) / cross-cutting layer (constraints shared by multiple modules, existing on demand) / module-level (internal behavior); altitude is a landing result, not an entry parameter.
- **Granularity valve**: if this round's goal requires expanding the internal contracts of more than one module → the round stops at decomposition (sub-goal list + project-level / cross-cutting clauses); each sub-goal becomes its own later round of `brainstorming → write-test → audit → implement → wrap-up chain`.
- **Test-free branch**: pure one-off operations (migrations / backfills / one-shot scripts) get no derived tests; write-test instead produces a **mechanically decidable verification checklist**, audited alongside the README; implement's completion criterion is passing the checklist item by item.
- **Two audit checkpoints**: after brainstorming finalizes the README (cross-module goals: audit the contract first, saving derivation rework) + after write-test completes (README + tests / checklist reviewed together); single-module goals may merge into one combined review.
- **Wrap-up chain**: once implement's exit gate passes, two passes are **mandatory** — `simplify` (simplify this round's diff with zero authoring memory; wording only, never behavior) → `code-review` (the zero-context quality cut). Both **hard-require dispatching a subagent**; if the environment can't, BLOCKED (rationale: the three hard dependencies in the Plugin boundary section). simplify's scope is decided **per code, not per branch** — both the criterion and the condition for skipping it entirely live in `simplify`'s "scope" section; not restated here.
- **Close-out**: all modules done (each with its wrap-up chain complete) → return to brainstorming to close out — architecture structure tests all green + a re-run of the business-flow walkthrough = the project-level exit gate (loop terminal).
- **Loop convergence valve**: any back-edge retriggering on the **same gap** up to a threshold (default 3) without converging → BLOCKED: stop auto-kickback, escalate to a human, attach that gap's kickback history (process-state routed out, never into the contract).
  **The round / standing-debt split belongs to audit alone**: only its verdict is two-tier, so only gaps introduced by the current round are counted (attribution criterion in `audit`'s verdict section). Every other phase's valve follows the general rule above and makes **no** round / standing distinction — their back-edges produce no standing-debt report.
  The threshold is **deliberately restated** in five dogma files: brainstorming · write-test · audit · implement · code-review. Rationale: dogma is not re-read after loading and cross-file jumps often fail to happen late in a long loop, so this is an **explicit exception to "one authoritative statement + pointers", and the exception is exactly that enumeration**; a structure test must assert **the enumerated set is complete and all values identical** (a missing copy or a differing value is red). diagnose carries two valves of its own (defect-fix rounds / evidence stalling) and is not in this set.

## Usage

Advance one scope at a time; describe your intent in chat to trigger the matching skill:

- **New project**: `brainstorming` (a cross-module goal) designs the topology (module list + dependencies + interface contracts), gated by `audit`, then per module `brainstorming → write-test → audit → implement → wrap-up chain`; when all are done, `brainstorming` closes out.
- **Existing project**: `brainstorming` first distills the existing structure and asks whether to adjust; once the target state is set, proceed as above.
- **Bug fix**: an unexplained red or production defect first enters `diagnose` for attribution, then routes by exit (implementation wrong → implement; contract gap → brainstorming; test wrong / weak assertion → write-test).
- **Small change**: a pure-implementation small change goes straight to `implement` in-session; a change that touches the contract goes back to `brainstorming` for the README and `write-test` for the tests first, then implement. **Scale only picks implement's execution shape; it never exempts the wrap-up chain** — small changes go through simplify → code-review too.

Division of labor: in the contract and test phases, **the human** interrogates the requester's intent to completeness and confirms the contract; **the skills** turn the contract into guards and the red green. In one line — **the human defines the contract, the AI turns red to green.**

## The seven skills

| skill | phase | responsibility | output |
|---|---|---|---|
| `brainstorming` | contract · sole README write entry | open with the goal, interrogate intent to completeness (one question at a time); distill existing code before asking to adjust; business-flow walkthrough before finalizing; close out when all modules are done | README clauses landed by goal: project-level (module list + topology [each edge carries an interface contract] + boundary interfaces, **no internals**) / cross-cutting layer (constraints shared by multiple modules, on demand) / module-level (responsibility & boundary / expected features / interface contract / edge cases & invariants, **internals only**) |
| `write-test` | test · derivation | branch decision (needs lasting guarding → tests; one-off → verification checklist); test intent, not implementation; strong-assertion discipline | standalone test files (initially red: business-intent tests + structure tests [modules exist / interfaces visible / lasting invariants]) or a mechanically decidable checklist |
| `audit` | review · independent | **zero-context (hard requirement, must dispatch a subagent)** review of design artifacts; two checkpoints; gaps routed back upstream | **Two-tier verdict**: round verdict (did this round's changes introduce new incoherence — the release criterion) + standing-debt report (pre-existing debt; routed out, does not block handoff). Five checks: completeness · contract↔test consistency · boundary hygiene · internal consistency · **assertion strength** |
| `implement` | implementation · scale-adaptive | full micro-loop: verify-red→green→verify-green(regression)→refactor → contract gate → verify (edit in session / dispatch one executor / parallel orchestration, by scale); test-free branch: see Rhythm | implementation code |
| `simplify` | wrap-up chain · first pass | simplify this round's diff with **zero authoring memory**: wording only, never behavior; one change at a time, staying green; bounded against implement's inner-loop refactor by a **granularity + independence** dual criterion | simplified code + list of simplifications + **two report classes**: ① turned-red kickbacks → write-test (only after proving behavioral equivalence for that change; unprovable ⇒ the change was wrong, revert and close, **no kickback produced**) ② suspected bugs / contract gaps (report only, never touch; dispatcher applies the three-way handling) |
| `diagnose` | defect entry | attribution before any fix; evidence → pattern comparison → hypothesis testing → routing | reproducing red test (→implement) / contract gap (→brainstorming) / test-fix list (→write-test) / external-issue record |
| `code-review` | wrap-up chain · last pass | zero-context code-quality review (latent bugs / silent failures / maintainability), anchored to the module README as spec; finding handling: verify → satisfy / kick back / rebut with evidence | severity-ranked findings + explicit verdict (ready to wrap up / fix first) |

## Design philosophy (core axioms)

- **Two bottlenecks collapse into one**: AI implementation is production-ready; the real problems are ① system design ② test completeness, both equivalent to "declaring intent completely in the README." All skill firepower goes here.
- **Split by activity, the goal defines the round**: contract dialogue, test writing, review, and implementation are four activities, each owning a phase; the round is defined by its goal (what to achieve, what counts as achieved), and project-level / cross-cutting / module-level are merely the layers where clauses land. One activity is never split into two skills by altitude — that breeds the mirror tax.
- **Sole README write entry**: only brainstorming may write READMEs; **every other phase is read-only**, kicking gaps back. Companion rule: one authoritative statement + pointers, no restating across READMEs (the sole exception, and how it is guarded, lives in the Rhythm section's convergence-valve entry).
- **Temporal-semantics layering**: target-state (README + tests, bounded, sole truth) vs process-state (git log / GitHub Issues / memory tools, monotonically growing, traceable but not authoritative).
- **Target-state splits into two properties**: timeless (describes the current should-be state, not a changelog — **kept**) ≠ history-less (destroying decision rationale — **rejected**). Rationale is process-state, routed out rather than deleted; a load-bearing constraint keeps a **one-token marker** (`[承重·勿删]`) in the hot doc, while the rationale itself goes to the workflow (memory/issues).
- **Zero overlap across layers**: the README tree is layered by the project's real structure — the project level owns topology (module set + dependency edges, pure structure), cross-cutting layers own constraints shared by multiple modules (existing on demand), the module level owns behavior (given input, output matches intent); every clause is declared once at its authoritative layer, lower layers receive it by pointer. The same information at two layers = a seed of drift.
- **Seam closure**: every topology edge carries an interface contract I; I is declared once at the project level, and the upstream output test and downstream input test both target the same I → semantic compatibility is locked from both sides, **no separate integration layer needed**. Structure tests verify only "modules exist + interfaces visible + lasting invariants," **not the real dependency graph and not runtime wiring**; the latter is the integration layer — YAGNI by default, done only when the README explicitly declares system-level intent as integration behavior tests.
- **Business-flow walkthrough**: each phase owns one segment; nobody naturally owns walking a business flow end to end — broken links (swallowed-error loops, signals with no consumer, dangling states) are invisible to any single phase. So brainstorming, at finalize and close-out, treats the README contract web as a state machine and walks every flow's forward, reverse, and exception paths looking for the receiving contract at each step.
- **Strong-assertion discipline**: a test whose assertion is vacuous has zero discriminating power — worse than no test (it fakes coverage). write-test bans vacuous assertions / status-code-only checks / loose enum matching / unlocked precision; audit's fifth check targets assertion strength.
- **Two-level exit gates**: module-level = implement's contract-conformance gate (implementation exactly == module contract); project-level = brainstorming's close-out gate (structure tests all green + business-flow walkthrough passes = loop terminal).
- **Loop convergence valve**: no infinite kickback — the same gap failing to converge trips the breaker and escalates to a human (threshold and mechanics: see the Rhythm section).
- **Test-scope iron rule**: go by the intent declared in the README. Implementation details are **not tested** by default (implementation is free); only when the README explicitly promotes an implementation constraint to a requirement is it tested. The criterion is not "is this implementation?" but "did the README declare it?"
- **Anti-cheat gate (implement invariants)**: tests and review findings are read-only to the execution loop — no tampering, no pre-judging, no softening; a wrong test is kicked back upstream, never silently patched in the loop.
- **Two kinds of independence**: the loop needs a fresh pair of eyes in three places, but not the same pair — **zero-context** (audit / code-review) = unaware of the design conversation, so it can't paper over contract gaps from memory, and it is **read-only**; **zero authoring memory** (simplify) = unaware of how the code came to be, so "I remember this had to be written this way" can't hide a detour, and it **edits**. Same root, different use: treating simplify as a third zero-context cut feeds it the wrong dispatch input — it needs the tests to run its "one change at a time, stay green" rhythm.
- **Attribution before fixing**: no defect gets fixed without attribution; "it looks like X, so change X" is what diagnose exists to eliminate. Fixes always happen in implement; diagnose only produces handoff artifacts.

## Cross-platform topology: single-source dogma, dual-written bindings

northstar ships for two platforms, Claude Code and Codex CLI. Three layers, connected by interface contracts:

```
Dogma layer    plugins/northstar/skills/ seven SKILL.md — single source, platform-agnostic
   ▲ via the I-platform-capability table
Binding layer  Claude Code: plugins/northstar/agents/*.md (frontmatter pins opus/sonnet/haiku)
               Codex: agents TOML (per the platform agent schema, pinning concrete models + reasoning-effort tiers)
   ▲
Distribution   Claude Code: .claude-plugin/ marketplace
               Codex: in-repo plugin manifest (per the platform convention .codex-plugin/plugin.json + marketplace manifest .agents/plugins/marketplace.json); agents ship with the repo (not in the plugin) + one-time install guide
```

Binding layer = agent definitions + a **platform execution note** (one per platform: the item-by-item delivery declaration for the capability table, the platform-specific execution details extracted from the dogma, and platform prerequisites all live here; dogma text references it by pointer, location is implementation freedom). The criterion for "platform-specific": a platform's **named forms** of the three execution shapes ("edit in session / dispatch one executor / orchestrate parallel executors") and their isolation mechanics are extraction targets; cross-platform abstract concepts (subagent, dispatch, read-only retrieval) stay in the dogma.

**I-platform-capability table** (the dogma↔binding interface contract): dogma text expresses platform actions only in abstract verbs; each binding layer declares, item by item, how its platform delivers —
1. Dispatch a zero-context subagent (the two cuts: audit / code-review)
2. Dispatch a module-level executor (implement) and an attributor (diagnose)
3. Read-only retrieval
4. Dispatch a **zero-authoring-memory** simplification executor (simplify) — it edits code, unlike the read-only cuts of item 1
5. Model / reasoning-effort tiering: judgment high (review / attribution / simplification), execution medium, retrieval low

**Cross-cutting constraints (shared by both bindings)**:
- Dogma text must contain no platform-specific names (tool names / config fields / invocation syntax) — enforced as a mechanically assertable lasting invariant
- Each binding delivers every item of the capability table; any undeliverable item = that step explicitly unavailable on that platform, silent degradation forbidden (every item resting on a hard subagent dependency — the two zero-context cuts and the zero-authoring-memory simplifier — defers to the BLOCKED axiom in the next section, pointer not restatement)
- Loop orchestration is always "main session → one layer of subagents"; no skill may require a subagent to dispatch further subagents
- The Codex binding pins concrete models: the install guide must state the required models and note that users may change models / tiers in their local copies; the release process includes "verify pinned models are still valid" `[load-bearing, keep]`

## Plugin boundary: dogma + execution bindings (three hard subagent dependencies)

The plugin = seven skills (dogma, tool-agnostic) + six subagents (execution bindings: per-phase executors and model tiering; shipped with the plugin on the Claude Code side, and as the same definitions in TOML shipped with the repo on the Codex side — see the Cross-platform topology section; both under version control, no longer stray files). **Three hard platform dependencies** (all native capabilities, but dependencies nonetheless): `audit` and `code-review` must dispatch a **zero-context subagent** (the in-session agent remembers the design conversation and can't be truly zero-context); `simplify` must dispatch a **zero-authoring-memory executor** (the in-session agent remembers how the code came to be, so simplifying it yourself is playing amnesiac). The distinction between the two is in the Design philosophy entry of the same name. When the environment can't dispatch one, that step is not executable — BLOCKED to a human, never downgraded to self-review. Everything else below stays **out of the plugin** and is the user's personal global CLAUDE.md workflow config:

- **Process-state routing** (where rationale / todos / history go): bind memory tools / GitHub Issues / git. Skills only declare "process-state stays out of the contract, routed out," not where to.
- **Contract-conformance review** (does the implementation exactly == the contract) is the opposite — it's framework dogma, self-issued by `implement`'s exit gate, not outsourced.

## Independence: self-contained, no external engine

All seven skills and six subagents are self-authored, **depending on / reusing / pinning no external plugin** (including superpowers and other official engines; `simplify`'s simplification discipline was digested from the official code-simplifier and re-authored, with a source line kept in its SKILL.md). northstar runs standalone once installed.

**Why no external engine**: borrowing an off-the-shelf TDD / review engine was considered and dropped after a fit assessment — "don't reinvent the wheel" holds only when it's "redundant and unnecessary," and northstar needs things an external engine can't give:

- the "test itself is wrong → kick back to brainstorming / write-test to regenerate" loop, plus subagent model-tiering — generic engines lack these;
- "test before implementation" is already **structurally guaranteed** by the pipeline order (README → tests → implementation), making the engine's core value redundant here.

So each skill self-authors a thin layer that nails only its own loop and invariants, without rebuilding an engine. Absorbed external methodology (the brainstorming / write-test dialogue and derivation paradigms, systematic-debugging → diagnose, receiving-code-review → code-review's handling section, code-simplifier → simplify's simplification discipline, writing-skills' naive-agent pressure test → this repo's acceptance gate for skill texts) is credited in a provenance line at the end of each SKILL.md — traceable, not vendored.

### Claude Code plugin mechanism facts (measured)

- **Skill discovery = pure directory convention**: `plugin.json` doesn't list skills; dropping in `skills/<name>/SKILL.md` makes it discoverable. Adding a skill only creates a directory — no manifest change.
- **Skill cross-calling = semantic relevance + the platform Skill tool**, not hard paths. The loop (implement kicks back to write-test, audit kicks back to brainstorming) just needs to name them in prose — no dependency declaration.
- **Override priority = user instructions (CLAUDE.md) > plugin skill > default**: your CLAUDE.md naturally outranks any plugin skill; conflicts are resolved by mechanism.
- **Version pinning** relies on the `gitCommitSha` recorded at install time (`~/.claude/plugins/installed_plugins.json`), not at the marketplace.json level.
