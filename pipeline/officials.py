"""Build site/data/officials.json: who holds each Oregon legislative and
congressional seat, for the "Who represents you" lookup.

Sources (both public and meant for reuse):
  - Open States current-legislators file for Oregon (public domain data,
    gathered from the Oregon Legislature's member pages)
  - unitedstates/congress-legislators (public-domain roster of Congress)

Oregon has 30 Senate districts and 60 House districts. Each Senate district
is two House districts put together (Senate District 1 is House Districts 1
and 2), so a voter has one senator and one representative.

Never fails the nightly run: if a source is down, the last good file is kept.
"""
from __future__ import annotations

import csv
import io
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

OUT = Path(__file__).resolve().parent.parent / "site" / "data" / "officials.json"
UA = "CivicsOR/0.1 (BarNone nonprofit civic calendar; contact via barnoneinc.org)"
LEGISLATORS = "https://data.openstates.org/people/current/or.csv"
CONGRESS = "https://raw.githubusercontent.com/unitedstates/congress-legislators/gh-pages/legislators-current.json"
PARTY = {"Democratic": "Democrat"}


def parse_legislators(csv_text: str) -> dict:
    """{"senate": {"1": [...]}, "house": {"1": [...]}} from the Open States CSV."""
    out: dict[str, dict] = {"senate": {}, "house": {}}
    for row in csv.DictReader(io.StringIO(csv_text)):
        m = re.match(r"^\s*0*(\d+)\s*$", row.get("current_district") or "")
        chamber = {"upper": "senate", "lower": "house"}.get((row.get("current_chamber") or "").strip())
        name = (row.get("name") or "").strip()
        if not m or not chamber or not name:
            continue
        out[chamber].setdefault(m.group(1), []).append({
            "name": name,
            "party": PARTY.get(row.get("current_party", ""), row.get("current_party", "")),
            "phone": (row.get("capitol_voice") or row.get("district_voice") or "").strip(),
            "email": (row.get("email") or "").strip(),
        })
    for seats in out.values():
        for people in seats.values():
            people.sort(key=lambda p: p["name"])
    return out


def parse_congress(rows: list, state: str = "OR") -> dict:
    out = {"senators": [], "house": {}}
    for person in rows:
        term = person["terms"][-1]
        if term.get("state") != state:
            continue
        entry = {
            "name": person["name"].get("official_full")
                    or f"{person['name'].get('first', '')} {person['name'].get('last', '')}".strip(),
            "party": term.get("party", ""),
            "phone": term.get("phone", ""),
            "url": term.get("url", ""),
        }
        if term["type"] == "sen":
            out["senators"].append(entry)
        else:
            out["house"][str(term.get("district"))] = entry
    out["senators"].sort(key=lambda m: m["name"])
    return out


def get(url, params=None):
    import requests
    from build import check_robots  # same robots.txt rule as the calendar
    check_robots(url)
    resp = requests.get(url, params=params, headers={"User-Agent": UA}, timeout=45)
    resp.raise_for_status()
    return resp


def main() -> int:
    now = datetime.now(ZoneInfo("America/Los_Angeles"))
    try:
        previous = json.loads(OUT.read_text())
    except Exception:
        previous = {}
    data = {"generated": now.isoformat(timespec="seconds"),
            "legislators": previous.get("legislators", {"senate": {}, "house": {}}),
            "congress": previous.get("congress", {"senators": [], "house": {}})}

    try:
        found = parse_legislators(get(LEGISLATORS).content.decode("utf-8-sig"))
        # A short file means the source is mid-update; keep the last good one.
        if len(found["senate"]) >= 25 and len(found["house"]) >= 50:
            data["legislators"] = found
        print(f"legislators: {sum(map(len, found['senate'].values()))} senators in {len(found['senate'])} districts, "
              f"{sum(map(len, found['house'].values()))} representatives in {len(found['house'])} districts")
    except Exception as exc:
        print(f"[warn] legislators: {type(exc).__name__}: {exc}"[:300], file=sys.stderr)

    try:
        congress = parse_congress(get(CONGRESS).json())
        if congress["senators"]:
            data["congress"] = congress
        print(f"congress: {len(congress['senators'])} senators, {len(congress['house'])} representatives")
    except Exception as exc:
        print(f"[warn] congress: {type(exc).__name__}: {exc}"[:300], file=sys.stderr)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
