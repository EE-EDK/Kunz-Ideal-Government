# Decision log: v2 recovery, 2026-10-04

## Provenance tags

| Tag | Meaning |
|---|---|
| `[VERIFIED: 2026-06-02 transcript]` | In the founding conversation (2026-06-02 to 06-03), in the owner's words. |
| `[VERIFIED via transcript]` (2026-06-28) | The v2 master records it as checked against that session's transcript. That transcript is not in this catalog. |
| `[RECALLED: 2026-09-13 memory log]` | Owner-stated, recorded from a memory log. No transcript has been found. |
| `[DELEGATED 2026-10-04]` | Picked by an agent under the owner's instruction to "pick the most logical decision based on my source information". Each pick is grounded in the sources below. Open items stay `inprogress` until the owner closes them. |

## A. Restored from the v2 master

These decisions were lost when `data/layers.json` was extracted from the v1 page.

| Id | Change | Source |
|---|---|---|
| 1A | Structure resolved (Option D augmented: structured statements + committee-scoped RAG record → AI recommendation → rotating panel, final, text only, no precedent) | 2026-06-28, verified |
| 1A | Glossary resolved: immutable core; companion annotations only; amendment threshold above 3/4 + 75%, exact figure at 2D | 2026-06-28, verified |
| 1A-sub | Judiciary committee: AI evidentiary rubric by default; contest with counsel to a sortition committee bound by the same rubric | 2026-09-13, recalled |
| c26 to c30 | Military posture, cell justice detail, emergency tax, project funding entities, service incentives | see section C |
| 1C ← 6B | Rogue-cell enforcement merged into 1C; 6B node removed, text kept in 1C's explanation | 2026-09-13, recalled |
| 5C → 1A | Body-level arbiter selection moved into 1A's qualification sub-item | 2026-09-13, recalled |
| 5A | AI-role principle: always contestable; infrastructure, not governance; can be phased out | 2026-09-13, recalled |
| 2D | New sub-item: glossary amendment threshold | 2026-06-28 |
| 1B, 2A to 2C, c7, c11 to c14, c21, c24 | Fuller labels and descriptions from the brief | brief v1.0 |

## B. Detail restored from the founding transcript

The one-line summaries dropped detail the owner stated. It is now in each item's `explanation` field (the builder already renders it): c5, c8, c10, c12, c13, c14, c15, c16, c17, c18, c20, c21, c23, c24 and c25. Every entry is tagged `[VERIFIED: 2026-06-02 transcript]`. Examples:

- the oversight body as ambassadors and local judges with prosecution authority;
- the two-part self-correcting structure;
- the 5% steel contribution example;
- competitive absorption with a resource ceiling;
- cell size shrinking where high-value resources cluster;
- the citizenship path (service, language, time in a cell's culture).

## C. Conflicts resolved

### C1. c26 military posture against universal service

- **Source conflict.**
  - On 2026-06-02 the owner said: "a mandatory service period of all eligible men and women with caveats for disability etc. Even physical disability will be utilized" and "Training and upkeep will happen at all times, but given all citizens are potential troops, there is no need for a … standing army." `[VERIFIED]`
  - The recalled c26 text says: "No standing army, no universal service … Volunteers first; conscription only at grave trigger points." `[RECALLED]`
- **Pick.** Keep universal service as a training and readiness term, and read the 2026-09-13 text as rules for **deployment**: volunteers first, conscription at grave triggers.
- **Why.**
  - The verified decision wins over a recalled one.
  - The constitution is additive-only, so a resolved item cannot be removed.
  - Both texts agree on no standing army and on citizen activation.
  - c30's incentives only make sense if volunteering for deployment is something extra to reward.
- **Kept.** The c26 recalled original, verbatim: "No standing army, no universal service. Cell militias for local events. Large-scale conflict is pre-committed by cell-to-body agreements with preordained cell specializations. Volunteers first; conscription only at grave trigger points (merit/numbers-based, with perks, fixed rotations, escalating multi-cell override to extend). Body may run an outward-facing intelligence and development service funded by cell contracts. (2026-09-13)"
- **Also reconciled.** c26's "outward-facing intelligence service" is assigned to the existing national security body (c12), which already covers the CIA function. The 2026-09-13 addition is that cell contracts fund it.
- **Residual.** A new sub-item under 6E: conscription trigger points.

### C2. c27 to c30 provenance

These were decided on 2026-06-02 `[VERIFIED]`. The v1 page left them out of its 25 constitutional items, and 2026-09-13 only confirmed them. They are re-tagged to show this. Items that had more detail in the transcript got it back: votes at cell or body level, funding to the cohort's estimate, the 10% promotion-weighting example. The AI-assisted jury in c27 stays `[RECALLED]`.

### C3. 1A-sub: one body or two

- **Ambiguity.** The recalled log names both a "sortition-drawn committee" and a "rotating arbiter panel".
- **Pick.** These are two bodies at two stages. The committee rules on the factual record (scoping the evidence). The panel rules on the merits and its ruling is final.
- **Why.**
  - The verified 2026-06-28 structure already puts a judiciary committee at the evidence stage ("factual record, filtered and scoped by a judiciary committee").
  - That structure separately puts the rotating panel at the appeal stage.
  - 1A-sub was opened to define that committee.
- **Second pick.** The sortition committee is drawn equally per cell.
  - This matches Option A (each cell contributes).
  - It also matches equal-per-cell WMD manning and rotating cell delegates. `[VERIFIED]`
- **Residual.** A new 1A sub-item covers who writes and amends the evidentiary rubric. The rubric is now the point where capture would happen, and no source answers this.

### C4. AI audit gap (5A)

- **Gap.** "Audited only when contested" catches an error only in the case someone contests. A bias that runs through every case goes unseen. The founding gap list asked "who audits AI outputs for systematic bias?"
- **Pick.**
  - Every AI output is published.
  - Any cell has standing to contest a pattern of outputs, not only a single case.
- **Why.**
  - This keeps the owner's "audited when contested" rule.
  - Transparency recurs throughout the sources: public streaming, open charters, publicly readable parity numbers, "the system itself should be readily accessible".
- **Status.** `inprogress` until the owner closes it.

### C5. AI against the elected body (5A)

- **Pick.** The human body prevails. An AI output stands only while it is uncontested.
- **Why.**
  - Axiom 8 says AI "is infrastructure, not governance".
  - In 1A, AI gives only a recommendation and the panel's ruling is final.
- **Status.** `inprogress`.

### C6. AI phase-out fallback (5A)

- **Pick.**
  - 1A runs as its rotating panel directly (the Option A structure already inside Option D).
  - Parity numbers are maintained by the sector owners who already set them (c16).
- **Why.** Both fallbacks already exist in the design. Removing the AI loses speed but no authority.
- **Status.** `inprogress`.

## D. Open questions the catalog does not answer

- The 2026-09-13 items stay `[RECALLED]` until checked against a session transcript.
- The v2 sections `axioms`, `coreArchitecture`, `resolutionLog`, `priorityQueue` and `sessionRules` are in `sources/v2_DATA.json`. The builder does not render them yet.
