#!/usr/bin/env python3
"""Build schedule.json from the approved LinkedIn drafts in linkedin/posts/.

Slots (Thailand time, +07:00): jil 10:00, morning 13:00, evening 20:00.
Only items with a '## Text' section are scheduled; comment-only days are skipped.
Items already published from the earlier scheduler are listed in KNOWN_POSTED with their LinkedIn URN,
so the poster never publishes them again.
Run: python3 linkedin/poster/build_schedule.py
"""
import json, pathlib, re

REPO = pathlib.Path(__file__).resolve().parents[2]
POSTS = REPO / "linkedin" / "posts"
OUT = pathlib.Path(__file__).resolve().parent / "schedule.json"
SLOT_TIME = {"jil": "10:00", "morning": "13:00", "evening": "20:00"}

KNOWN_POSTED = {
    "2026-10-19-morning": "urn:li:share:7517647345912610816",
    "2026-10-20-morning": "urn:li:share:7518115955336597504",
    "2026-10-20-evening": "urn:li:share:7518287617659080706",
    "2026-10-22-morning": "urn:li:share:7518840683907112960",
    "2026-10-22-evening": "urn:li:share:7519013943005052928",
    "2026-10-23-jil": "urn:li:share:7519231495966785538",
    "2026-10-23-morning": "urn:li:share:7519276801857187840",
    "2026-10-23-evening": "urn:li:share:7519382986547429376",
    "2026-10-25-jil": "urn:li:share:7519956272004329472",
    "2026-10-25-evening": "urn:li:share:7520107360317566976",
    "2026-10-26-jil": "urn:li:share:7520318621571715072",
    "2026-10-26-morning": "urn:li:share:7520363921246011392",
    "2026-10-26-evening": "urn:li:share:7520472664872861698",
    "2026-10-27-jil": "urn:li:share:7520680904571199488",
    "2026-10-27-morning": "urn:li:share:7520726373926088704",
    "2026-10-27-evening": "urn:li:share:7520832207368683520",
    "2026-10-29-jil": "urn:li:share:7521405841372135424",
    "2026-10-29-morning": "urn:li:share:7521451433733398530",
    "2026-10-29-evening": "urn:li:share:7521562852332326912",
    "2026-10-30-jil": "urn:li:share:7521768278986326016",
    "2026-10-30-morning": "urn:li:share:7521814500493430784",
    "2026-10-30-evening": "urn:li:share:7521920662836334593",
    "2026-11-01-jil": "urn:li:share:7522492806242967552",
    "2026-11-01-morning": "urn:li:share:7522538137592578048",
    "2026-11-01-evening": "urn:li:share:7522643985870491648",
    "2026-11-02-jil": "urn:li:share:7522855263616389120",
    "2026-11-02-morning": "urn:li:share:7522900604613124096",
    "2026-11-02-evening": "urn:li:share:7523008646679646208",
}
# Morning post of 25 Oct was never published (502 during the scheduled run); its slot has passed.
KNOWN_MISSED = {"2026-10-25-morning"}

TEXT_RE = re.compile(r"^## Text[^\n]*\n\n(.*?)\n+## Evidence check", re.S | re.M)


def kind_of(path):
    if path.parent.name == "jil":
        return "jil"
    if path.parent.name == "evening":
        return "evening"
    return "morning"


def build():
    items = []
    for path in sorted(list(POSTS.glob("2026-*.md")) + list(POSTS.glob("evening/2026-*.md")) + list(POSTS.glob("jil/2026-*.md"))):
        kind = kind_of(path)
        date = path.stem
        match = TEXT_RE.search(path.read_text(encoding="utf-8"))
        if not match:
            continue  # comment-only day
        item_id = f"{date}-{kind}"
        item = {
            "id": item_id,
            "at": f"{date}T{SLOT_TIME[kind]}:00+07:00",
            "kind": kind,
            "source": str(path.relative_to(REPO)),
            "text": match.group(1).strip(),
        }
        if item_id in KNOWN_POSTED:
            item["urn"] = KNOWN_POSTED[item_id]
        if item_id in KNOWN_MISSED:
            item["missed"] = True
        items.append(item)
    items.sort(key=lambda i: i["at"])
    OUT.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return items


if __name__ == "__main__":
    items = build()
    pending = [i for i in items if "urn" not in i and not i.get("missed")]
    print(f"wrote {OUT} with {len(items)} items; {len(pending)} pending")
