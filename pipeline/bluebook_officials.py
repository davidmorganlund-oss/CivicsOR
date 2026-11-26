"""Build site/data/county_officials.json and site/data/mayors.json from the
Oregon Blue Book, for the "Who represents you" lookup.

Each county's Blue Book page has a "County Officials" paragraph that starts
with the governing body (a board of commissioners, or a county court of a
county judge and two commissioners), each name followed by the year the term
ends, then the other county officers. It also links every incorporated city,
and each city page names the mayor.

Never fails the nightly run: a county or city that can't be read keeps the
names from the last good run, and if too few come back the files are left
as they were.
"""
from __future__ import annotations

import html
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
LOCAL = ROOT / "site" / "data" / "local.json"
COUNTY_OUT = ROOT / "site" / "data" / "county_officials.json"
MAYOR_OUT = ROOT / "site" / "data" / "mayors.json"
UA = {"User-Agent": "Mozilla/5.0 (CivicsOR civic lookup; +https://civicsor.org)"}
SITE = "https://sos.oregon.gov"
PAGE = SITE + "/blue-book/government/Pages/{}.aspx"
HOME = SITE + "/blue-book/government/Pages/local-county.aspx"
MIN_COUNTIES, MIN_MAYORS = 30, 180

TAG = re.compile(r"<[^>]+>")
# Officers listed after the governing body. A segment that starts with one of
# these ends the list of commissioners.
OFFICER = re.compile(
    r"^(?:Dist\.? ?Atty|District Attorney|Sheriff|Assess|Clerk|Treas|Surv|Justice|J\.P\.|Co\.|County (?:Admin|Counsel|Manager|Clerk|Assessor|Surveyor|Treasurer)|"
    r"Admin|Auditor|Coroner|Recorder|Tax|Legal|Counsel|Manager|Public Works|Road|Dir|Health|Juvenile|Elections|Finance|Commission Admin)",
    re.I)
MEMBER = re.compile(
    r"(?:(?P<title>Chair|Vice[- ]Chair|Judge|Commissioner|President|Pres\.)\s+)?"
    r"(?:(?:Dist\.?|District|Pos\.?|Position)\s*(?P<d1>\d+)\s*[:,-]?\s+)?"
    r"(?P<name>[A-Z][^,;:()]*?)\s*"
    r"(?:\((?:Dist\.?|District|Pos\.?|Position)\s*(?P<d2>\d+)\)\s*)?"
    r"\((?P<year>\d{4})\)")


def text(fragment: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(TAG.sub(" ", fragment)).replace("​", "")).strip()


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower().replace(".", "")).strip("-")


def officials_paragraph(page: str) -> str:
    m = re.search(r"County Officials\s*</h2>(.*?)</p>", page, re.S | re.I)
    return text(m.group(1)) if m else ""


def parse_body(paragraph: str):
    """(body, members) from a County Officials paragraph."""
    body = "County Court" if re.match(r"\s*County Court", paragraph, re.I) or re.search(r"\bJudge\b", paragraph.split(";")[0]) else "Board of Commissioners"
    members = []
    for seg in paragraph.split(";"):
        seg = seg.strip()
        # Drop labels like "Commissioners:" or "County Court:" in front of names.
        bare = re.sub(r"^(?:[A-Za-z. ]+:\s*)+", "", seg) if re.match(r"^[A-Za-z. ]+:", seg) else seg
        if members and OFFICER.match(bare):
            break
        if not members and OFFICER.match(bare) and not re.match(r"(?i)co(?:unty|\.)? (?:court|comm)", seg):
            break
        for m in MEMBER.finditer(bare):
            title = (m.group("title") or "").replace("Pres.", "President").replace("Vice Chair", "Vice-Chair")
            members.append({
                "name": m.group("name").strip(),
                "title": title or None,
                "district": m.group("d1") or m.group("d2"),
                "term_ends": m.group("year"),
            })
    return body, members


def get(url):
    import requests
    try:
        r = requests.get(url, headers=UA, timeout=30)
        return r.text if r.status_code == 200 else None
    except Exception:
        return None


def county_page(name):
    for s in (slug(name), slug(name) + "-county"):
        url = PAGE.format(s)
        page = get(url)
        if page and re.search(re.escape(name) + r"\s+County", page) and "County Officials" in page:
            return name, url, page
    return name, None, None


def city_links(page: str):
    m = re.search(r"Incorporated Cities\s*</h2>(.*?)</h2>", page, re.S | re.I)
    block = m.group(1) if m else ""
    return [(text(t), SITE + h) for h, t in re.findall(r'href="(/blue-book/government/Pages/[a-z0-9-]+\.aspx)"[^>]*>(.*?)</a>', block, re.S)]


def mayor_of(item):
    city, url = item
    page = get(url)
    if not page:
        return city, url, None
    m = re.search(r"Mayor\s*(?::|&#58;)\s*(?:</?[^>]+>|\s)*([^<]+)", page)
    name = text(m.group(1)) if m else ""
    if not name or re.match(r"(?i)(vacant|none|tbd|n/?a)\b", name):
        return city, url, ""
    return city, url, name


def load(path, key):
    try:
        return json.loads(path.read_text())[key]
    except Exception:
        return {}


def main() -> int:
    names = sorted(json.loads(LOCAL.read_text())["counties"])
    old_counties, old_mayors = load(COUNTY_OUT, "counties"), load(MAYOR_OUT, "mayors")
    counties, mayors, cities, problems = {}, {}, [], []
    with ThreadPoolExecutor(6) as pool:
        for name, url, page in pool.map(county_page, names):
            if not page:
                problems.append(f"{name} County page not found")
                if name in old_counties:
                    counties[name] = old_counties[name]
                continue
            para = officials_paragraph(page)
            body, members = parse_body(para)
            if not members:
                problems.append(f"{name}: no commissioners parsed from: {para[:200]}")
            counties[name] = {"body": body, "members": members, "source_url": url, "text": para}
            cities += city_links(page)
        for city, url, name in pool.map(mayor_of, dict(cities).items()):
            if name is None:
                problems.append(f"{city}: city page not read")
                if city in old_mayors:
                    mayors[city] = old_mayors[city]
            elif name:
                mayors[city] = {"name": name, "source": url}
    for p in problems:
        print("  " + p)
    print(f"Blue Book: {len(counties)} counties, {sum(bool(c['members']) for c in counties.values())} with commissioners; "
          f"{len(mayors)} mayors from {len(dict(cities))} city pages")
    today = datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat()
    meta = {"source": "Oregon Blue Book", "source_url": HOME, "as_of": today}
    if len(counties) >= MIN_COUNTIES:
        COUNTY_OUT.write_text(json.dumps({**meta, "counties": counties}, indent=1, ensure_ascii=False) + "\n")
    else:
        print("Too few counties; keeping the last good county file.")
    if len(mayors) >= MIN_MAYORS:
        MAYOR_OUT.write_text(json.dumps({**meta, "source_url": SITE + "/blue-book/government/Pages/local-cities.aspx",
                                         "mayors": dict(sorted(mayors.items()))}, indent=1, ensure_ascii=False) + "\n")
    else:
        print("Too few mayors; keeping the last good mayors file.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
