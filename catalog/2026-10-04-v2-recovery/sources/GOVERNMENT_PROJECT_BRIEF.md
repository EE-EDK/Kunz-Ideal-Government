# Ideal Government Design — Project Brief & Session Rules

Version: 1.0
Last Updated: 2026-06-02
Status (as written): Constitutional Layer complete. Layer 1 (Foundation) in progress — 1A open.

> **Status of this copy, 2026-10-04.** This is the brief as it stood on 2026-06-02, copied from the project instructions. Changes made to the copy:
>
> - Tables that were flattened into running text were restored to tables.
> - Status emoji in sections 4 and 5 were replaced with words.
> - In sections 1 and 6, references to the visualization file were generalized. The original named `government_web_v1.html`, its `LAYERS` array, the `STATUS.*` constants and a `present_files` step.
> - Two bracketed annotations were added: "25 items at the time of this brief" in section 3, and the "since superseded" note in section 1.
> - Every other word is as written.
>
> One figure in the brief does not match what was measured. Section 5 says v1 has 110 nodes. Rendering `../archive/government_web_v1.html` on 2026-10-04 gave 91, because v1 does not draw the 25 constitutional items as nodes. The text is left as written.
>
> - **Still authoritative:** section 2 (axioms), section 3 (core architecture, additive only), section 6 (session rules).
> - **SUPERSEDED:** sections 4, 5, 7 and 8 describe state that has since moved. The `DATA` object in `../government_master_v2.html` is the source of truth for current state. They are kept below, unedited, for history.
> - **Since this brief:** the 2026-06-28 session resolved the 1A structure and the glossary. The 2026-09-13 decisions (1A-sub, constitutional items c26 to c30, 1C absorbing 6B, arbiter selection moved from 5C to 1A) are in the master file's Resolution Log, tagged `[RECALLED]`.

## 1. PROJECT OVERVIEW

This is a long-running structured design conversation to define a complete, philosophically coherent ideal government system from first principles. The output is both a written specification and a living 3D visualization (`government_web_v1.html`, since superseded by `government_master_v2.html`) that updates as items are resolved.

The goal is a full-stack government design — constitutional layer through defense/security — with every core aspect addressed, no hand-waving, no contradictions.

## 2. AXIOM SET (immutable — do not re-litigate these)

These are the owner's established philosophical priors. Accept them as given. Build on them, do not challenge them.

| Axiom | Statement |
|---|---|
| Natural rights | Objective natural law exists. Rights are recognized, not granted. Defensible through deism, Christianity, or secular reason equally. Source-agnostic. |
| Soft determinism | Agency is real. Physics constrains but does not fully determine. Consciousness/soul have undetermined properties. Hard determinism rejected. |
| Hierarchy | Dominance hierarchy is biological species-level fact, not cultural artifact. Flat structures are unstable. Design must work with hierarchy, not against it. |
| NAP baseline | Non-Aggression Principle is the default behavioral norm. Voluntarism first. Coercion only where structurally necessary. |
| Subsidiarity | Power dispersed is power constrained. Decisions at the lowest competent level. Switzerland/canton model is the closest real-world approximation. |
| Anti-metropolitanism | Urban density pathologizes human behavior at scale. Rural interdependence produces better social outcomes. Design should structurally limit density concentration. |
| Children as protected class | Children hold rights in trust. NAP applies asymmetrically until capacity is established. Extra protection layer is constitutional, not discretionary. |
| AI as legitimacy tool | AI parses law for contradiction, maintains parity numbers, enables data-driven egalitarianism. It is infrastructure, not governance. |

## 3. CORE ARCHITECTURE (resolved — do not re-open without flagging)

### Constitutional Layer (fully resolved — 25 items at the time of this brief)

The supreme document. Additive-only. 3/4 coordination body + 75% popular supermajority to amend. Never subtractive.

Key resolved items:

- Natural rights recognized, not granted
- NAP as default norm
- 10th/9th analog — all unlisted powers default to cells
- No international authority recognized
- Speech: radical, NAP-bounded. Cell nuance permitted.
- Religion: subsumed under speech, NAP-tested. Voluntary practice protected. Governance application that mandates non-voluntary compliance = constitutional void. (Shariah as governance = void. Shariah as personal practice = protected.)
- Arms: tiered — household issue baseline → personal/Class III constitutional → cell militia for heavy → WMD equally distributed across cells
- Travel: citizen constitutional floor. Cell-licensed nuance (driving, etc.)
- V+1 criminal standard — retributive proportionality plus one degree for violent crime
- Execution: tiered — victim (first right) → volunteer pool (random selection) → automated chamber (randomized actuation, 3 fast methods, fire/cleanup). No permanent executor class.
- National security body: transparently chartered, subsumes FBI/CIA/NSA, no domestic surveillance authority
- Oversight body: separately elected, dual function (internal accountability + diplomatic interface), hard-scoped
- Immigration: foreign nationals have zero constitutional standing. Tiered entry (tourist/education/business = cell-permitted, short-term). Body-floor citizenship requirements universal. Cell adds above floor. Sharp penalties for violations. No international body authority over borders.
- Resource contribution: value-percentage based, 10-year review cycle, no default income tax
- Parity number system: technocratic, sector-owned, publicly transparent. Required for all businesses at founding.
- Progressive wealth equation: significant wealth permitted, takeover-scale accumulation structurally prevented via ceiling
- Birth accounts: body floor + cell additive, funded from cell value percentages. No citizen starts at zero.
- No mandatory welfare — voluntary support system + birth accounts replaces it
- Early adulthood petition: 12+ with 75% judicial panel + mandatory parental inclusion
- Cell absorption: competitive incentive market, 90% dual supermajority (both cells), accumulation ceiling enforced
- Cell disbandment: prohibited — cells can only be absorbed, never dissolved
- New cell formation: body-wide formal process, resource allocation review triggered
- WMD: capability-defined (10,000+ casualties OR 1+ sq mile radius). Equal custody across all cells. Cross-cell manning. No single cell controls WMD monopoly.
- Inter-cell movement: citizen-preferenced process, merit/achievement transfer pathway, body citizenship portable

### Cell Model (resolved)

- Cells = the canton analog. Named (e.g., "Iron-Cell," "FreeFarming-Cell")
- Resource-balanced geography at founding — no cell holds monopoly on high-value natural resources
- Cells have their own constitutions, below the body constitution
- Cell-citizens hold dual identity: body-citizen status (portable) + cell-citizen status (cell-specific)
- Cells compete for citizens — birth accounts, resources, quality of governance are differentiators

### WMD / National Security (resolved)

- WMD defined by capability metric (10k+ casualties or 1+ sq mile damage), technology-agnostic
- Equal distribution across cells — mutual assured balance, no cell achieves dominance
- Cross-cell equal contribution to manning — rotation/contract fills resource gaps, headcount stays proportional
- National security body: no domestic surveillance, transparently chartered
- Oversight body: separately elected, dual internal/external function, limited scope by design
- Violations of national security role: V+1 applied, publicly streamed — no permanent institutional capture possible

### Wealth / Economic Floor (resolved)

- Primary check: resource-balanced cell geography at founding
- Secondary check: body-level progressive contribution equation (scales with value, universal across cells)
- Tertiary check: cell-level anti-monopoly rules for non-resource industries
- Parity number: all businesses/industries/services assigned dynamic transparent value metric by technocratic sector owners
- No mandatory welfare. Voluntary system + birth account = floor.
- Struggling cell pathway: competitive absorption offers from other cells, 90% dual supermajority still applies, accumulation ceiling prevents dominant cell from absorbing everything

### Citizenship (resolved)

- Body-level floor: universal minimum requirements, non-negotiable everywhere
- Cell-level acceptance: after body floor cleared, applicant selects and must be accepted by a specific cell
- Cell defines its own additional requirements above the body floor
- Entry vector problem solved: lenient cell can only grant cell-citizenship; body-citizenship requires clearing hard floor

### Coordination Body (framework resolved, detail pending in 2D)

- Hybrid: rotating cell delegates + equal technocratic sector representation
- Population-adaptive scaling
- New cells or absorptions trigger rebalancing of representation numbers

## 4. STRUCTURAL LAYERS — CURRENT STATUS

> **SUPERSEDED 2026-10-04.** State as of 2026-06-02. See the `DATA` object in `../government_master_v2.html` for current status. Kept unedited for history.

```
LAYER 1: FOUNDATION        IN PROGRESS
LAYER 2: STRUCTURE         NOT STARTED
LAYER 3: ECONOMIC          NOT STARTED
LAYER 4: SOCIAL            NOT STARTED
LAYER 5: LEGITIMACY        NOT STARTED
LAYER 6: DEFENSE           NOT STARTED
```

### Layer 1 — Foundation (Rights Arbitration, NAP Enforcement, Hierarchy Constraints)

**1A — Rights Arbitration Body (in progress)**

- Options presented: A (rotating cell draws), B (merit court), C (distributed text-based), D (hybrid text-first + panel appeal)
- Current position: Option D under consideration
- Option D: AI parses conflict against constitutional text → generates ruling recommendation → if either party rejects, escalates to rotating panel → panel decision is final, constitutional text only (no spirit-of-the-law)
- Recommended addition: founding document must include a plain-language glossary of all key terms (force, initiation, citizen, cell, rights, etc.) as part of the immutable core
- OPEN: Owner has not yet confirmed Option D or glossary requirement

**1B — NAP Edge Cases (not started)**

- Fraud (takes without consent, no physical force — NAP violation?)
- Cross-cell environmental damage (force against whom?)
- Psychological coercion (qualifies as initiation?)
- Negligence causing harm (unintentional — still NAP violation?)

**1C — Enforcement Hierarchy (not started)**

- What enforces body-level constitutional violations if a cell refuses compliance?
- Coordination body currently has no defined enforcement arm

### Layer 2 — Structure (not started)

- 2A: Minimum central functions list (what must exist at body level)
- 2B: Cell internal governance floor (minimum to produce a delegate)
- 2C: Cell size / subdivision trigger (population growth management)
- 2D: Coordination body detail (delegate count, sector count, quorum, voting thresholds, term lengths, emergency sessions)

### Layer 3 — Economic (not started)

- 3A: Currency model (single body / cell currencies / open competition)
- 3B: Property rights (land theory, IP, commons, abandoned property)
- 3C: Cross-cell contract enforcement
- 3D: Technocratic federation detail (sector list, permanent vs dynamic, regulatory vs advisory)

### Layer 4 — Social (not started)

- 4A: Child protection mechanics (V+1 multiplier, standing when parents perpetrate, body vs cell jurisdiction)
- 4B: Education (body floor vs cell-defined, private/market role, civics curriculum)
- 4C: Urban density mechanism (density ceiling, rural incentives, parity weighting for rural production)
- 4D: Family definition and rights (constitutional vs cell-defined, unit vs individual rights, custody/inheritance jurisdiction)

### Layer 5 — Legitimacy (not started)

- 5A: AI governance (ownership, capture prevention, audit, conflict resolution with elected body)
- 5B: Law writing process (cell revision cycle, body revision process)
- 5C: Judicial selection (cell-level and body-level)
- 5D: Transparency infrastructure (constitutional right to government data or cell-defined)
- 5E: Corruption standard (cell-level handling, body floor minimum)

### Layer 6 — Defense (not started)

- 6A: Cross-cell military command structure (command during external threat, sunset clause)
- 6B: Rogue cell enforcement (economic sanctions, military authorization threshold, isolation)
- 6C: Police function (cell control floor, oversight mechanism)
- 6D: Intelligence constraints (cell surveillance authority, voluntary sharing rules, evidentiary standard, foreign intel authorization)
- 6E: Threat definition (threshold for body-level trigger, authorization requirement)

## 5. VISUALIZATION

> **SUPERSEDED 2026-10-04.** The file named here is `../archive/government_web_v1.html`. The living version is `../government_master_v2.html`, which carries the document tabs and the 3D web together and derives both from one `DATA` object. The measured state of the current file is in `../README.md`. The text below is kept unedited for history.

- File: `government_web_v1.html`
- Technology: Three.js r128, single-file HTML, no build step
- Current state: 110 total nodes (25 resolved constitutional + 3 in-progress Layer 1 + 82 not-started across Layers 1–6)
- Node color key:
  - Gold pulsing = Constitutional Layer hub
  - Blue octahedra = Layer hubs (1–6)
  - Green = Resolved
  - Amber pulsing = In Progress
  - Dark wireframe = Not Started
  - Orange = Flagged
- Interaction: Drag orbit | Scroll zoom | Click node → detail panel | ESC closes panel
- Update rule: After each gap resolution, update the relevant node's status field in the `LAYERS` data object at the top of the HTML file. Status strings: `STATUS.RESOLVED`, `STATUS.INPROGRESS`, `STATUS.NOTSTARTED`, `STATUS.FLAGGED`. Also update `desc` field with the resolution text. Rebuild file and present to user.

## 6. SESSION RULES

### Conversation Protocol

- **One gap at a time.** Present the gap, give analytical options with tradeoffs, let the owner decide. Do not bundle multiple gaps into one question.
- **Axioms are fixed.** Do not re-open the items in Section 2. Build on them.
- **Resolved items are permanent.** Nothing from Section 3 is re-opened without the owner explicitly flagging it. Additive only.
- **After each resolution:** Log it cleanly, flag any residuals it surfaces, update the master checklist, then proceed to next item.
- **After each layer completes:** Update the visualization — change all resolved nodes to resolved, update descriptions, present the new file.
- **No unsolicited suggestions.** If the owner's stated position has a tension, surface it once, cleanly. If they resolve it, accept and move on. Do not re-surface resolved tensions.
- **Maintain forensic precision.** Distinguish: resolved (✅), in-progress (🔄), flagged residual (⚠️), not-started (⬜). Never mark something resolved unless the owner has explicitly closed it.

### Analytical Protocol

- Lead with the problem stated precisely, then options with tradeoffs
- Recommend only when there is a clear structural reason — label it as a recommendation, not a mandate
- Surface second-order effects of decisions (what does this unlock or complicate downstream?)
- When a decision creates a new open item, add it to the checklist immediately — do not let residuals disappear

### Format Rules

- Master checklist shown after every resolution using the tree format established in this project
- Resolutions logged in a clean block: `[Item ID] — Resolved`, followed by the mechanism
- Tensions flagged inline, not in a separate section, unless they affect multiple layers
- No filler, no summaries of what was just said, no "great choice" — log and proceed

### HTML Update Protocol

When updating the visualization file:

1. Locate the item in the data array by id
2. Change status from not-started to resolved (or appropriate)
3. Update `desc` field with the resolution summary (1–2 sentences)
4. If subitems exist, update each subitem's status individually
5. Use targeted `str_replace` edits — do not rewrite the whole file
6. Present the updated file
7. Note in the checklist: ✅ HTML updated — [item ID]

The current procedure, with the downstream artifacts to update, is in `../CLAUDE.md`.

## 7. HOW TO START A NEW SESSION

> **SUPERSEDED 2026-10-04.** The current resume block is in the master file: `DATA.sessionRules.resume`, shown on the Session Rules tab. The block below points at a state that has since moved. Kept unedited for history.

Paste this into the new chat:

```
GOVERNMENT DESIGN PROJECT — RESUME
This is a continuation of a structured government design project. The project brief and full state is in the attached file GOVERNMENT_PROJECT_BRIEF.md. Read it completely before responding.
The visualization file is government_web_v1.html — this is a Three.js 3D node graph of the entire government structure. It updates as items are resolved.
Current position: Layer 1A (Rights Arbitration Body) is open. Option D (hybrid text-first AI ruling + rotating panel appeal, constitutional text only) is under consideration. The plain-language glossary requirement has been recommended but not yet confirmed by the owner.
Resume from: "Confirm 1A structure or propose a variant."
Rules: Follow Section 6 of the project brief exactly. One gap at a time. Axioms are fixed. Nothing resolved is re-opened without explicit owner instruction. Show the master checklist after every resolution.
```

## 8. QUICK REFERENCE — OPEN ITEMS IN PRIORITY ORDER

> **SUPERSEDED 2026-10-04.** The live queue is `DATA.priorityQueue` in the master file (Priority Queue tab). Kept unedited for history.

| # | Item | Layer | Blocker? |
|---|---|---|---|
| 1 | 1A — Rights Arbitration Body structure | Foundation | Yes — needed before 1B/1C can close |
| 2 | 1A — Glossary requirement confirmation | Foundation | Yes — needed before 1A closes |
| 3 | 1B — NAP edge cases (fraud, environment, coercion, negligence) | Foundation | No |
| 4 | 1C — Enforcement hierarchy against rogue cells | Foundation | No |
| 5 | 2D — Coordination body full detail | Structure | Partial blocker — needed for Layer 5 legitimacy items |
| 6 | 3A — Currency model | Economic | No |
| 7 | 3B — Property rights | Economic | No |
| 8 | 5A — AI governance | Legitimacy | No |
| 9 | 6A — Cross-cell military command | Defense | No |
| 10 | 6E — Threat definition | Defense | Partial blocker — needed before 6A fully closes |

This document was the source of truth for project state until the master file replaced it. Its axioms (section 2) and session rules (section 6) remain in force.
