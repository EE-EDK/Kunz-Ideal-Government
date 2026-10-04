# Catalog: v2 recovery (2026-10-04)

On 2026-10-04, KunzPrime held a second, unrelated history of this repo, called v2 master. It carried design decisions that `data/layers.json` lacks, because `layers.json` was extracted from the v1 page of 2026-06-03. KunzPrime adopted `origin/main`. This catalog carries the lost decisions to the hub, where they are applied and published.

## Contents

| File | What it is |
|---|---|
| `DECISIONS.md` | Every change, its source, and the reasoning for each reconciliation. Read this first. |
| `layers.proposed.json` | `data/layers.json` with every change applied. It passes the builder's `load_data` validation (7 layers, 54 items, 30 resolved). |
| `build_proposed.py` | Regenerates `layers.proposed.json` from `data/layers.json` and `sources/v2_DATA.json`. stdlib only. |
| `sources/v2_DATA.json` | The full v2 `DATA` object: items plus axioms, core architecture, resolution log, priority queue and session rules. |
| `sources/GOVERNMENT_PROJECT_BRIEF.md` | Project brief v1.0 (2026-06-02) with the 2026-10-04 status note. |
| `sources/design-diff.txt` | Item-level diff between v2 and the v1-based `layers.json`. |

The founding conversation (2026-06-02, 84 KB) is not in this public repo. It lives on KunzPrime at `tools/desktop-rag/documents/claude-cloud-conversations/2026-06-02_Defining-the-ideal-government_ebd77a5a.md`. Every `[VERIFIED: 2026-06-02 transcript]` tag points there. The full v2 tree is kept on KunzPrime as the local tag `recovered/local-v2-2026-10-04`, plus a bundle under `recovery/`.

## Applying on kunz-ai-hub

1. `git pull --ff-only`
2. Read `DECISIONS.md`. Section C contains agent picks made under the owner's delegation. Items still open stay `inprogress` until the owner closes them. Do not promote them to `resolved`.
3. If `data/layers.json` changed since 2026-10-04, rerun `python3 catalog/2026-10-04-v2-recovery/build_proposed.py`. Then `cp catalog/2026-10-04-v2-recovery/layers.proposed.json data/layers.json`.
4. `python3 src/build_ideal_government.py --check`, then `python3 src/build_ideal_government.py`.
5. Render the page. Check that:
   - the counts read 54 items and 30 resolved;
   - c26 to c30 appear;
   - 6B is gone;
   - 1C lists the three carried sub-items;
   - item explanations show when an item is opened.
6. Commit `data/layers.json` and `ideal_government.html` together, then publish to kunzhub (`Self-Host/sites/kunzhub`, `scripts/add-page.sh`).
7. Optional: render the five v2 sections from `sources/v2_DATA.json`. Axioms and the resolution log are the most useful to readers.

Keep this folder after applying, as the record of where the decisions came from.
