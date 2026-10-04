"""Owner's own words, attached to the design items they answer.

Every quote is a verbatim substring of one of the owner's messages in the
2026-06-02 founding conversation. `verify()` checks each one against the
transcript, so a paraphrase or a typo cannot reach the page.

Run:  python3 src/owner_notes.py --transcript PATH          # verify only
      python3 src/owner_notes.py --transcript PATH --apply  # write into data/layers.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "layers.json"

T1 = "2026-06-02 01:58:41"  # foundations
T2 = "2026-06-02 03:01:42"  # constitution, cells, travel, economy
T3 = "2026-06-02 03:13:14"  # weapons of mass destruction, national security
T4 = "2026-06-02 03:33:34"  # execution, resources, welfare, parity, citizenship
T5 = "2026-06-02 04:22:52"  # parity, birth accounts, movement, absorption
T6 = "2026-06-02 04:31:06"  # absorption balance

# (item id, message timestamp, verbatim passage)
NOTES: list[tuple[str, str, str]] = [
    ("c1", T2, "Adding requires a 3/4 vote by some form of yet to be defined leadership and  a 75 percent popular vote if grassroots defined."),
    ("c1", T2, "This document can be added to but never taken away from."),
    ("c2", T1, "I believe there is an objective natural law of rights that can be defended through deism, Christianity, or several other secular means as well"),
    ("c3", T1, "the nonaggression principle is a good place to start"),
    ("c3", T1, "I would say that I try to lead voluntarists first."),
    ("c4", T1, "I would say Switzerland and its loosely affiliated cantons with individual constitutions is pretty close."),
    ("c4", T2, "The 10th US amendment will apply in combination with the 9th but directly clearly pointed to the cells."),
    ("c5", T2, "We won't recognize international authority, working with NATO etc. but only as needed to address true global threats or worldwide economy crashes etc."),
    ("c6", T2, "Next would be a radical freedom of speech based on NAP. Rules for handling nuance are held by the cells."),
    ("c7", T2, "Freedom of religion will wrap under speech but caveat issues like Islamism under NAP that have ANY rules that directly violate freedoms noted in cells without a method of voluntary following. It would effectively make shariah law for example a non-starter."),
    ("c8", T2, "Weapons will be issued per defined household for all cells."),
    ("c8", T2, "conceal carry and self manufacture are core items up to class III which is automatic infantry weapons. Explosives, missiles, tanks, etc. are reserved for individual militias of cells, but can be accessed with difficult restrictive processes."),
    ("c9", T2, "Freedom of travel applies to a base set of elements like search and seizure everywhere, but cell constitutions can regulate nuance like licenses or training requirements for driving etc."),
    ("c9", T2, "There will be no DMV though, either it is private or small and localized to centers of authority within the cells."),
    ("c10", T2, "Core obvious rights would be eye for eye on violent crimes +1 , maybe call it V+1 , which means robbing and beating someone to death would mean a slower beating of that individual to death--massive deterrent against violent crimes that aren't just fights or threats etc. but multi fact battery, murder, rape, torture."),
    ("c11", T4, "The execution of the sentence will be given to the victim when there is a clear one for choice."),
    ("c11", T4, "After that, there will be a body of volunteers willing to pool a random selection, and on the rare event that an entire cell is against volunteering at all, we will use technology as a failsafe."),
    ("c11", T4, "This whole system only matters if the victim and all others don't participate."),
    ("c12", T3, "cell-citizens will share the burden of maintaining and handling the national security elements for the body"),
    ("c12", T3, "These groups do not have unique powers to spy on citizenry or use their information access to benefit etc."),
    ("c12", T3, "Discovery of such issues results in long painful and publicly streamed death."),
    ("c13", T3, "There actually should be a small dedicated group also separately elected by the cells to be the oversight for this group"),
    ("c13", T3, "but they will have very limited scope to prevent building any possible level of leverage or militaristic capability that threatens the whole."),
    ("c14", T2, "Also, for the right to travel, this only applies to citizens. Foreign actors have zero constitutional backing."),
    ("c14", T2, "They will be strictly controlled in the country borders and the only path to citizenship is a grueling set of requirements that involve social/military service, learning the language, completing a longer amount of time in the culture of choice with a cell, but there will be sharp penalties for violations of immigration law."),
    ("c14", T4, "Just applying to and gaining the first steps is body-wide."),
    ("c14", T4, "the individual must select and be accepted by a representative of a cell."),
    ("c14", T4, "The cell defines all rules for citizenship for itself as a cell-citizen (likely the name like Iron-citizen or FreeFarming-citizen)."),
    ("c15", T2, "Any items required for national level or external facing items for all cells will be funded by a clear dynamic value based system. This can be actual product, or profit percentages of product."),
    ("c15", T2, "As an example, the infrastructure sector in a cell that is manufacturing heavy could have a 5% value share that means giving 5% of its steel production for beams to build a federal building for international trade etc."),
    ("c15", T2, "These will be agreed upon by all cells and can be adjusted as new markets open or change every 10 years (long economic cycle)."),
    ("c16", T5, "The parity system has to be a technocratic item. It should be jointly set and controlled by the generators and owners of value. The system itself should be readily accessible."),
    ("c16", T4, "Even SaaS or other items can be given a parity number, in fact that will be a requirement for all items of work or industry or service etc."),
    ("c16", T4, "One core item for a new business is to work with authorities to develop a parity number that balances the value output based on a central understanding of transparent worth that is dynamic."),
    ("c17", T4, "Balance should be based on resource control primarily, and there can be basic anti monopoly rules set by cells for items like software or service etc."),
    ("c17", T4, "Wealth will not be prevented though."),
    ("c17", T4, "That will not prevent doing 'really' well but will stop takeover level wealth or levels of poverty that are untenable."),
    ("c18", T5, "Birth accounts come from value percentages in each cell."),
    ("c18", T5, "there is a smaller floor by body then a cell governed additive."),
    ("c18", T4, "there will also be a starting bank of sorts for all citizens at birth that can grow or be used for a variety of items and it's up to the citizen to handle it appropriately when of age"),
    ("c19", T4, "That said there will be no mandatory social system like welfare, instead, a voluntary system will be setup and marketed by the body level for needs"),
    ("c20", T4, "btw one can petition at any age above 12 for adulthood based on a convening of judicial hearing details set by cell--but parents are always a part of it, and it is expected to be a strict 75% agreement of the hearing group."),
    ("c20", T4, "This allows genius level mature rare kids to secure power early enough to make an outsized difference while healthy and young."),
    ("c21", T5, "absorption requires 90 percent of both affected cells to agree."),
    ("c21", T6, "A poor cell should still have a relative balance of resources. Whatever those are still matters to the body."),
    ("c21", T6, "Absorbing interests can offer incentives for initial absorption to drive a level of competition."),
    ("c21", T6, "That said, resource balancing still exists so a cell can't absorb all cells for control. There needs to be a rebalancing that incentivizes the absorber but limits overall accumulation."),
    ("c22", T5, "Disbandment is not allowed."),
    ("c23", T5, "New cells setup will follow formal processes involving all cells like in the beginning of resource allocation on instantiation of the country."),
    ("c23", T4, "There should be no cell that has the richest of all sources of say uranium, platinum, gold, tantalum all in one area."),
    ("c24", T3, "all weapons of mass destruction that become accessible...defined by some body metric like capable of 10000 or more death or more than a square mile of damage or something"),
    ("c24", T3, "will be equally shared between all cells out of mutual survival and need to balance the extreme nature."),
    ("c24", T3, "This means a body-wide clearance system with strict vetting that sources equal numbers of participants across sectors based on needed resources."),
    ("c25", T5, "The new item is whether citizens of cells can move cells. This can be a process similar to immigration but preference given to citizens. Also perks could allow transfer due to accomplishment, award, etc."),
    ("c26", T2, "a mandatory service period of all eligible men and women with caveats for disability etc. Even physical disability will be utilized though."),
    ("c26", T2, "Training and upkeep will happen at all times, but given all citizens are potential troops, there is no need for a wasteful federal government backed standing army."),
    ("c26", T2, "only external threats pull federal-like military action together."),
    ("c27", T2, "The assumption is that cells will set bail and punishment rules, trial by what type of jury etc. to maintain a diverse and localized system that more closely reflects those close to the rules."),
    ("c28", T2, "If needed, a tax can be levied, but it will be voted either at cell or body level and will always be a flat limited tax with clear rules and uniquely with hard stops."),
    ("c28", T2, "This prevents infinite systems that justify their existence with fraud or abuse by never fixing streets or never cutting costs etc."),
    ("c29", T2, "If a cell based government like entity is setup to tackle ...lets say a blight, they will be given the needed amounts estimated by their cohort to get scientists, international assistance, production of any chemical agents needed etc."),
    ("c29", T2, "and then when the blight is gone or finished, the group is either refocused, or disbanded and absorbed back into another role"),
    ("c30", T2, "would likely require some level of benefit for their volunteering to assist an internal problem...like a 10% weight toward promotion or position or something...or maybe a reduction in taxes required for future efforts)."),
    ("2a", T3, "So balance instead of a 3 part government here is based on a 2 part self-hosted self correcting national security structure."),
    ("2c", T2, "The cells can exist of their own interest or charter, but primarily they would be initially formed based on the technocratic federation idea to maximize resource handling."),
    ("2c", T4, "If resources are close then cells are smaller."),
    ("2d", T4, "This should be a hybrid that adjusts with population. If new cells are added or one is absorbed by 90% decree etc. then population can change the numbers."),
    ("2d", T4, "Otherwise, cells will elect delegates on a rotating basis from their governmental structure, but the core technocratic authorities (CEOs or corps etc) will have an equal represntation."),
    ("3d", T1, "I'm also a fan of certain capitalistic or, let's say, federation state styles that maybe would help split items out more so you could have federation states as subgroups within the hierarchy that control certain aspects of, let's say, a certain industry, but not in a way that's tied to some central government, more a technocratic element."),
    ("4a", T1, "then I would say children come next as they're a unique element that deserves an extra level of protection as well as, let's say, a censorship or a careful handling of their rights before they're able to properly understand and exercise them."),
    ("4c", T1, "there is a clear problem with mental health, autonomy, and even just being generally nice to fellow humans that I don't see in many rural areas where people are forced to survive on their own"),
    ("4c", T1, "So whatever can maximize spreading out these centers of power that create a hive mind of infantilized people who rely on a bunch of systems and generally lead to high taxes and eventually degradation, high crime, etcetera."),
    ("5a", T1, "I also think AI plays a role in the future for determining certain things, especially when you can now parse thousands of lines of laws and other elements and see where they contradict what makes sense, more understanding of data. And so I think that egalitarianism is going to become partly data driven."),
    ("6c", T3, "Almost all other items, even environmental or police corruption etc. are handled by cells."),
]


def _transcript_messages(path: Path) -> dict[str, str]:
    """Map a user message timestamp to its body text."""
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"^### \*\*(User|Claude)\*\* \(([^)]+)\)\s*$", text, flags=re.M)
    out: dict[str, str] = {}
    for i in range(1, len(parts), 3):
        if parts[i] == "User":
            out[parts[i + 1]] = parts[i + 2]
    return out


def verify(transcript: Path) -> list[str]:
    """Return a list of problems; empty means every quote is verbatim."""
    msgs = _transcript_messages(transcript)
    problems = []
    for item, at, quote in NOTES:
        body = msgs.get(at)
        if body is None:
            problems.append(f"{item}: no user message at {at}")
        elif quote not in body:
            problems.append(f"{item}: not verbatim at {at}: {quote[:70]!r}")
    return problems


def apply(data: dict) -> dict:
    """Attach notes to items as data['layers'][i]['items'][j]['notes']."""
    by_id: dict[str, dict] = {}
    for layer in data["layers"]:
        for item in layer["items"]:
            by_id[item["id"]] = item
    for item in by_id.values():
        item.pop("notes", None)
    for item_id, at, quote in NOTES:
        if item_id not in by_id:
            raise KeyError(f"note for unknown item {item_id!r}")
        by_id[item_id].setdefault("notes", []).append({"at": at, "quote": quote})
    return data


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcript", type=Path, required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args(argv)
    problems = verify(args.transcript)
    if problems:
        print("NOT VERBATIM:")
        for p in problems:
            print("  -", p)
        return 1
    print(f"ok: {len(NOTES)} owner quotes verbatim")
    if args.apply:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        DATA_FILE.write_text(json.dumps(apply(data), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote notes into {DATA_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
