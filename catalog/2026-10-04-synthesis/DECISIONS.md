# Decision log: master synthesis applied, 2026-10-04

Source: `sources/MASTER-SYNTHESIS.md` (owner's consolidated state, dated 2026-10-04). The synthesis follows the decision log up to 2026-09-13. Where it conflicts with an earlier agent pick, the synthesis wins. Where it is silent, the earlier record stands.

## A. Changed to match the synthesis

| Change | Where | Synthesis section |
|---|---|---|
| c26 now rejects universal service. Explanation rewritten to "No standing army and no universal service…". Supersedes the C1 pick in `catalog/2026-10-04-v2-recovery/DECISIONS.md`, which kept universal service as a training term. | `data/layers.json` c26 | Constitutional c26; Dropped table ("Rejected in c26") |
| The 2026-06-02 quote about mandatory service stays in `data/ledger.json`, untouched. It is provenance, not design. | `data/ledger.json` (unchanged) | n/a |
| Constitutional explanations filled in for c1 to c30 where the page had none, and sharpened where it was thin: c4, c18, c21, c24, c27, c28, c29, c30 among them. Wording follows the brief where the brief has it, otherwise the synthesis. | `data/layers.json` | Constitutional layer table |
| c21 now reads "Needs 90% in both cells", replacing "the target keeps a 90% veto". | c21 | c21 |
| Item descriptions added for 1C, 2A, 2B, 2C, 3A, 3C, 3D, 5B, 5C, 5D, 5E, 6A and 6E. | `data/layers.json` | Layer 1 to 6 tables |
| 5C now records that it is not known whether c27 closes the cell-level half of 5C. | 5C description | "What already bears on it", 5C |
| 6A now carries "c26 sets who fights, not who commands." | 6A description | Layer 6 table |
| Priority queue: 6E before 6A (the synthesis says 6E is needed before 6A closes). A catch-all row for the remaining layer items was added. | `priority_queue` | Open items in priority order |
| New reference sections on the page: working principles, dropped and superseded, gaps in the record. | `data/layers.json` keys `working_principles`, `dropped`, `gaps`; `src/build_ideal_government.py` | Working principles; Dropped and superseded; Questions this synthesis could not answer |
| Version v2.3; `_source` updated; resolution log entry dated 2026-10-04. | `data/layers.json` | n/a |
| README status and publishing text corrected (25 of 50, "served privately" were stale). AGENTS.md item 5 corrected to match the owner-approved public exception in `CLAUDE.md`. | `README.md`, `AGENTS.md` | n/a |

## B. Left alone on purpose

- **Statuses are unchanged.** 54 items, 30 resolved. Nothing in the synthesis closes a new item, and nothing it lists as open has been marked resolved.
- **Axioms are unchanged.** The synthesis calls the eight axioms "fixed … none open for debate". Its table is a condensation of the brief's wording. The "Consciousness/soul" clause in Soft determinism is in the brief and in v2, and the synthesis does not say to drop it. Omission in a summary is not a removal decision.
- **Core architecture is unchanged.** It matches the synthesis point for point.
- **Delegated picks in 1A-sub and 5A stay `inprogress`.** The synthesis neither confirms nor contradicts them. See section C.

## C. Still open: agent picks the synthesis does not settle

These come from `catalog/2026-10-04-v2-recovery/DECISIONS.md` and remain `inprogress` until the owner closes them.

1. **One committee or two (1A-sub).** The synthesis describes one "judiciary committee", sortition-drawn, bound by the rubric, and reached on contest. The v2-recovery pick treats it as two bodies at two stages: an evidence-stage committee and an escalation committee. The synthesis's step 1 ("filtered by a judiciary committee") and step 3 ("a committee drawn by lot") could be read either way. Owner to confirm.
2. **Equal draw per cell (1A-sub).** The v2-recovery pick draws the committee equally per cell. The synthesis says only "sortition-drawn". The per-cell rule is not in the synthesis, so it is not removed, but it is not confirmed.
3. **Publish every AI output (5A).** The v2-recovery pick requires publication of all AI outputs, with standing to contest a pattern. The synthesis says "audited only when contested" and does not mention publication. Owner to confirm.
4. **Evidentiary rubric authorship (1A residual).** Still open. The synthesis does not address it, and the working principle that loose ends are logged, not dropped, keeps it on the page.

## D. Publishing

- The kunzhub page `pages/public/ideal-government/index.html` is this repo's `ideal_government.html` plus the kunzhub frame block. The frame is spliced back in before `</body>`, and the publish commit touches only that path.
- `Self-Host/sites/ideal-government` is a second checkout of this repo, pinned in the Self-Host submodule tree at `bd4c02e`. Nothing reads it for the live page. The inbox service runs from this repo (`WorkingDirectory` in `deploy/ideal-government-inbox-api.service`), so it is current on push. The Self-Host pointer was not bumped.
