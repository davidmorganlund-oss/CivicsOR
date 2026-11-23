"""Turn probe results into candidate sources for trial.py.

python tools/gen_candidates.py probe.jsonl tools/candidates.yml [kind]
probe.jsonl holds one probe.py result per line (the PROBE lines from the
"Find calendars" run). kind is "city", "county" or "school" and sets the area.
"""
import json, re, sys
from urllib.parse import unquote
import yaml

CIVIC = re.compile(r"council|commission|board|committee|planning|hearing|meeting|budget|advisory|"
                   r"agenda|public|government|city|urban renewal|district|authority|task force", re.I)
NOT_CIVIC = re.compile(r"recreation|library program|story ?time|event|festival|concert|class|camp|sport|"
                       r"museum|holiday|closure|community events|parks? (?:and|&) rec|senior center activities", re.I)


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


LIB_DISTRICT = re.compile(r"district|county|cooperative|network|regional|services", re.I)
LIB_CITY = re.compile(r"\s*(public|city|community|memorial|carnegie)?\s*(public\s*)?(/school\s*)?library.*$", re.I)


def area_for(r, kind):
    if kind == "library":
        return "countywide" if LIB_DISTRICT.search(r["name"]) else LIB_CITY.sub("", r["name"]).strip() or "countywide"
    if kind == "county" or r["name"].endswith(" County"):
        return "countywide"
    if kind == "school":
        return "countywide"
    return r["name"]


def candidates(r, kind):
    name, county, out = r["name"], r["county"], []
    base = {"county": county, "area": area_for(r, kind)}
    title = f"City of {name}" if kind == "city" and not name.endswith("County") else name
    sid = slug(name if kind != "school" else name.replace(" SD ", " sd "))
    f = r.get("found", {})
    if kind == "library":
        title = name
        for h in f.get("libcal", [])[:1]:
            out.append({"id": sid, "name": title, "type": "libcal", "host": h, "civic_only": True, **base,
                        "category": "library", "homepage": f"https://{h}/calendar"})
        for t in f.get("bibliocommons", [])[:1]:
            if not out:
                out.append({"id": sid, "name": title, "type": "bibliocommons", "library": t,
                            "searches": ["board", "trustee", "voter", "citizenship", "civic", "town hall"], **base,
                            "category": "library", "homepage": f"https://{t}.bibliocommons.com/v2/events"})
    for t in f.get("legistar", [])[:1]:
        out.append({"id": sid, "name": title, "type": "legistar", "client": t, **base,
                    "homepage": f"https://{t}.legistar.com/Calendar.aspx"})
    for t in f.get("civicclerk", [])[:1]:
        out.append({"id": sid, "name": title, "type": "civicclerk", "tenant": t, **base,
                    "homepage": f"https://{t}.portal.civicclerk.com/"})
    for t in f.get("primegov", [])[:1]:
        out.append({"id": sid, "name": title, "type": "primegov", "tenant": t, **base,
                    "homepage": f"https://{t}.primegov.com/public/portal"})
    for t in f.get("civicweb", [])[:1]:
        out.append({"id": sid, "name": title, "type": "civicweb", "tenant": t, **base,
                    "homepage": f"https://{t}.civicweb.net/Portal/MeetingSchedule.aspx"})
    for t in f.get("iqm2", [])[:1]:
        out.append({"id": sid, "name": title, "type": "iqm2_rss", **base,
                    "url": f"https://{t}.iqm2.com/Services/RSS.aspx?Feed=Calendar",
                    "homepage": f"https://{t}.iqm2.com/Citizens/Calendar.aspx"})
    for t in f.get("municode", [])[:1]:
        out.append({"id": sid, "name": title, "type": "municode", **base,
                    "url": f"https://{t}.municodemeetings.com/", "homepage": f"https://{t}.municodemeetings.com/"})
    for g in f.get("granicus", [])[:1]:
        m = re.match(r"([a-z0-9-]+)\.granicus\.com/ViewPublisher\.php\?view_id=(\d+)", g, re.I)
        if m:
            out.append({"id": sid, "name": title, "type": "granicus", "tenant": m.group(1), "view_id": int(m.group(2)),
                        **base, "homepage": f"https://{g}"})
    if not out:
        cp = r.get("civicplus") or {}
        cats = [int(c) for c, label in cp.get("cats", []) if CIVIC.search(label) and not NOT_CIVIC.search(label)]
        if cats:
            out.append({"id": sid, "name": title, "type": "civicplus", "site": cp["root"], "categories": cats,
                        **base, "drop_uncategorized": True, "homepage": cp["root"] + "/Calendar.aspx"})
    if not out and (r.get("fs_calendars") or {}).get("ids"):
        fs = r["fs_calendars"]
        ids = sorted({i for chunk in fs["ids"] for i in chunk.split(",") if i})
        q = "&".join(f"calendar_ids[]={i}" for i in ids)
        out.append({"id": sid, "name": title, "type": "ics", **base,
                    "url": f"{fs['root']}/fs/calendar-manager/events.ics?{q}", "homepage": r["final"]})
    if not out and (r.get("apptegy_info") or {}).get("feeds"):
        m = re.search(r"/api/v\d/o/(\d+)/", r["apptegy_info"]["feeds"][0])
        if m:
            out.append({"id": sid, "name": title, "type": "apptegy", "org": int(m.group(1)), **base,
                        "homepage": r["final"]})
    if not out and r.get("wordpress"):
        root = re.match(r"https?://[^/]+", r["final"]).group(0)
        out.append({"id": sid, "name": title, "type": "ics", **base, "url": f"{root}/events/?ical=1",
                    "include": "council|commission|board|committee|hearing|meeting|session|workshop",
                    "homepage": f"{root}/events/"})
    if not out:
        for g in f.get("gcal", [])[:2]:
            cid = unquote(g).split("&")[0]
            if "@" in cid or "group.calendar" in cid:
                out.append({"id": sid + ("" if not out else "-2"), "name": title, "type": "ics", **base,
                            "url": f"https://calendar.google.com/calendar/ical/{cid.replace('@', '%40')}/public/basic.ics",
                            "drop_uncategorized": True, "homepage": r["final"]})
    if not out:
        for u in r.get("ics", [])[:1]:
            u = u.replace("&amp;", "&").replace("webcal://", "https://")
            if u.startswith("/"):
                u = re.match(r"https?://[^/]+", r["final"]).group(0) + u
            if u.startswith("http"):
                out.append({"id": sid, "name": title, "type": "ics", "url": u, **base,
                            "drop_uncategorized": True, "homepage": r["final"]})
    if kind == "library":
        for s in out:
            s.setdefault("category", "library")
            if s["type"] == "ics":
                s["include"] = r"\bboard\b|trustee|budget committee|public hearing|advisory committee"
                s.pop("drop_uncategorized", None)
    if kind == "school":
        for s in out:
            s["include"] = r"\bboard\b|budget committee|public hearing"
            s["category"] = "school"
            s.pop("drop_uncategorized", None)
    return out


if __name__ == "__main__":
    kind = sys.argv[3] if len(sys.argv) > 3 else "city"
    rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
    out = []
    for r in rows:
        k = "county" if r["name"].endswith(" County") and kind == "city" else kind
        out += candidates(r, k)
    seen = {}
    for s in out:
        n = seen.get(s["id"], 0)
        seen[s["id"]] = n + 1
        if n:
            s["id"] = f"{s['id']}-{n + 1}"
    yaml.safe_dump({"sources": out}, open(sys.argv[2], "w"), sort_keys=False, allow_unicode=True, width=200)
    print(len(out), "candidates from", len(rows), "sites")
