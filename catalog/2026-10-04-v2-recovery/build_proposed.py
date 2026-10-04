"""Build layers.proposed.json: data/layers.json plus the v2 decisions, the
transcript detail and the 2026-10-04 delegated reconciliations.

    python3 catalog/2026-10-04-v2-recovery/build_proposed.py

Inputs: ../../data/layers.json (the live design) and sources/v2_DATA.json.
Output: layers.proposed.json next to this script. stdlib only.
"""
import copy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

VERIFIED = "[VERIFIED: 2026-06-02 transcript]"
RECALLED = "[RECALLED: 2026-09-13 memory log]"
DELEGATED = "[DELEGATED 2026-10-04: agent pick under owner instruction, awaiting owner close]"

live = json.loads((ROOT / "data" / "layers.json").read_text(encoding="utf-8"))
v2 = json.loads((HERE / "sources" / "v2_DATA.json").read_text(encoding="utf-8"))
out = copy.deepcopy(live)

items = {i["id"]: i for layer in out["layers"] for i in layer["items"]}
layer_of = {i["id"]: layer for layer in out["layers"] for i in layer["items"]}
v2_items = {i["id"]: i for i in v2["constitutional"]["items"]}
v2_items.update({i["id"]: i for layer in v2["layers"] for i in layer["items"]})


def take_v2(item_id, *fields):
    for f in fields:
        items[item_id][f] = copy.deepcopy(v2_items[item_id][f])


# 1. v2 text that is richer than the v1 extraction.
for cid in ["c7", "c11", "c12", "c13", "c14", "c21", "c24"]:
    take_v2(cid, "desc")
for lid in ["1a", "1b", "1c", "2d", "5c"]:
    take_v2(lid, "label", "desc", "subitems")
for lid in ["2a", "2b", "2c"]:
    take_v2(lid, "label")

# 2. Founding-conversation detail the one-line summaries dropped.
EXPLAIN = {
    "c5": "Cooperation with NATO and similar bodies only as needed for true global threats or worldwide economic crashes.",
    "c8": "Concealed carry and self-manufacture are constitutional up to Class III (automatic infantry weapons). Explosives, missiles and armor are reserved to cell militias, reachable by individuals only through difficult, restrictive processes. Making, buying and selling carry cell nuance.",
    "c10": "Owner's framing: robbing and beating someone to death would mean a slower beating to death. Applies to multi-factor battery, murder, rape and torture, not to fights or threats.",
    "c12": "Cell-citizens share the burden of staffing national security (the FBI, CIA and NSA functions). Workers have no special power to spy on citizens or profit from access. Discovered abuse means long, painful, publicly streamed death.",
    "c13": "A small group elected separately by the cells. It acts as ambassadors and as local judges with prosecution authority over national-security workers, with scope kept narrow so it can build no leverage or military capability. With the national-security body it forms a two-part, self-correcting structure in place of three branches.",
    "c14": "First steps toward citizenship are body-wide. After the body requirements are met, the applicant must choose a cell and be accepted by a cell representative. The cell sets its own citizenship rules and names (e.g. Iron-Citizen, FreeFarming-Citizen). The path involves social or military service, learning the language and a longer period living in the chosen cell's culture.",
    "c15": "Owner's example: a manufacturing-heavy cell's infrastructure sector with a 5% value share gives 5% of its steel beams to a body building for international trade. Contributions are product or profit percentages, agreed by all cells, adjustable as markets open or change, reviewed every 10 years.",
    "c16": "Jointly set and controlled by the generators and owners of value. A new business works with authorities to develop its parity number. Values are dynamic and can change at any time. It is up to owners to enhance their number. The system is readily accessible.",
    "c17": "A tag on the percentage of value generated, scaling to a clear degree regardless of cell. It allows doing very well but stops takeover-level wealth and untenable poverty.",
    "c18": "A smaller body floor plus a cell-governed additive amount.",
    "c20": "Hearing details are set by the cell. Parents are always part of the hearing. Passing needs a strict 75% agreement of the hearing group.",
    "c21": "Struggling cells (below the floor threshold for a defined period) become eligible for absorption offers. Competing absorbers offer incentive packages (birth accounts, resource access, transfer perks, reduced contributions). The target keeps a 90% veto. No cell may exceed a set share of the total body resource base; approaching the ceiling ends eligibility to absorb, and the excess goes to new-cell formation or a struggling-cell recovery fund.",
    "c23": "Founding geography: no cell holds the richest sources of several high-value resources (uranium, platinum, gold, tantalum) together. Where resources sit close together, cells are smaller.",
    "c24": "A body-wide clearance system with strict vetting draws equal numbers of participants across sectors. Where a function needs more people, representatives from other cells serve rotations or contracts, but headcount stays equal.",
    "c25": "Transfers follow a process like immigration, with preference to existing citizens. Accomplishments and awards can unlock transfer.",
}
for cid, text in EXPLAIN.items():
    items[cid]["explanation"] = f"{text} {VERIFIED}"

# 3. c26 to c30. c26 reconciled with the verified universal-service decision.
const_items = layer_of["c1"]["items"]
const_items += [
    {
        "id": "c26",
        "label": "Military posture",
        "status": "resolved",
        "desc": "No standing army. Universal service stays: a training and readiness term for all eligible men and women, disability-inclusive by role. Cell militias handle local events. Large-scale conflict is pre-committed by cell-to-body agreements with preordained cell specializations. Deployment beyond training is volunteers first; conscription only at grave trigger points (merit- and numbers-based, with perks, fixed rotations, escalating multi-cell override to extend). The national security body (c12) runs the outward-facing intelligence and development service, funded by cell contracts.",
        "explanation": (
            f"Universal service and citizen activation {VERIFIED}. Volunteer-first deployment, conscription triggers and "
            f"pre-committed specializations {RECALLED}. Reconciled {DELEGATED}: the recalled text said "
            "'no universal service', which would reverse a resolved item under an additive-only constitution. "
            "Read as no universal deployment. Original wording is kept in the catalog decision log."
        ),
    },
    {
        "id": "c27",
        "label": "Justice detail — cell jurisdiction",
        "status": "resolved",
        "desc": "Bail, jury and punishment detail are cell jurisdiction. Diverse cell justice systems are necessary, like biological cells. AI may assist jury and peer processes.",
        "explanation": f"Cell jurisdiction over bail, jury and punishment {VERIFIED}. AI assistance {RECALLED}.",
    },
    {
        "id": "c28",
        "label": "Emergency tax",
        "status": "resolved",
        "desc": "Flat, voted at cell or body level, hard-capped, hard-stopped. Sunset clauses are constitutional.",
        "explanation": f"Decided {VERIFIED}; confirmed {RECALLED}. Purpose in the owner's words: prevents infinite systems that justify their existence by never fixing streets or never cutting costs.",
    },
    {
        "id": "c29",
        "label": "Project-based funding entities",
        "status": "resolved",
        "desc": "Scoped, funded to their cohort's estimate, then refocused, disbanded or absorbed at completion.",
        "explanation": f"Decided {VERIFIED} (owner's example: a body formed to beat a blight); confirmed {RECALLED}.",
    },
    {
        "id": "c30",
        "label": "Voluntary-service incentives",
        "status": "resolved",
        "desc": "Volunteering for internal problems earns benefits such as tax reduction or promotion weighting (owner's example: 10%).",
        "explanation": f"Decided {VERIFIED}; confirmed {RECALLED}. Pairs with c26: volunteer deployment is what earns these.",
    },
]

# 4. 1A: 1A-sub clarified, new residual, AI fallback.
for sub in items["1a"]["subitems"]:
    if sub["label"].startswith("1A-sub"):
        sub["label"] = "1A-sub: Judiciary committee — evidence-stage body, AI rubric by default, contest to a sortition committee drawn equally per cell"
items["1a"]["subitems"].append(
    {"label": "Evidentiary rubric — who writes and amends it", "status": "notstarted"}
)
items["1a"]["explanation"] = (
    f"1A-sub {RECALLED}, clarified {DELEGATED}: the sortition committee and the rotating arbiter panel are two bodies "
    "at two stages. The committee rules on the factual record (evidence scope); the panel rules on the merits and is "
    "final. The committee is drawn equally per cell, matching Option A and the equal-per-cell pattern used for WMD "
    "manning and delegates. Residual: the rubric is now the capture point, so its authorship and amendment are open."
)

# 5. 1C absorbs 6B. 6B removed as a node; its text is kept in the decision log.
l6 = layer_of["6b"]
l6["items"] = [i for i in l6["items"] if i["id"] != "6b"]
items["1c"]["explanation"] = (
    "Absorbed 6B on 2026-09-13 (" + RECALLED + "). 6B original text: \"If a cell violates the body constitution and "
    "refuses compliance, what is the enforcement mechanism?\" Option list from the founding conversation: economic "
    "sanctions by other cells, military action authorized by coordination-body supermajority, automatic resource "
    "reallocation, isolation with loss of representation and body-citizen protections until compliant."
)

# 6. 5A: AI principle plus delegated picks. Stays inprogress until the owner closes it.
a5 = items["5a"]
a5["status"] = "inprogress"
a5["explanation"] = (
    f"Principle {RECALLED}: AI is always contestable and audited when contested; it is infrastructure, governance only "
    "where it fills bureaucratic holes and proves long-run utility; it can be phased out if too contestable. "
    f"Picks {DELEGATED}: (1) every AI output is published, and any cell has standing to contest a pattern of outputs, "
    "not only a single case; this keeps 'audited when contested' and catches systematic bias. (2) In a conflict, the "
    "human body prevails; an AI output stands only while uncontested (axiom 8). (3) Phase-out fallback: 1A runs as its "
    "rotating panel directly, and parity numbers are maintained by the sector owners who already set them (c16)."
)
for sub in a5["subitems"]:
    if sub["label"] == "Audit mechanism":
        sub["label"] = "Audit mechanism — all outputs published; any cell may contest a pattern"
        sub["status"] = "inprogress"
    elif sub["label"] == "AI vs elected body conflict resolution":
        sub["label"] = "AI vs elected body — human body prevails; AI output stands only uncontested"
        sub["status"] = "inprogress"
a5["subitems"].append(
    {"label": "Phase-out fallback — 1A panel hears directly; sector owners maintain parity", "status": "inprogress"}
)

# 7. New residual from c26.
items["6e"]["subitems"].append(
    {"label": "Conscription trigger points (from c26)", "status": "notstarted"}
)

out["version"] = "v2.2"
out["_source"] = (
    "v1 extraction (government_web_v1.html, 2026-06-03) merged on 2026-10-04 with the v2 master decisions "
    "(2026-06-28 verified, 2026-09-13 recalled), founding-transcript detail and delegated reconciliations. "
    "See catalog/2026-10-04-v2-recovery/DECISIONS.md."
)

(HERE / "layers.proposed.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
total = sum(len(layer["items"]) for layer in out["layers"])
resolved = sum(i["status"] == "resolved" for layer in out["layers"] for i in layer["items"])
print(f"wrote layers.proposed.json: {len(out['layers'])} layers, {total} items, {resolved} resolved")
