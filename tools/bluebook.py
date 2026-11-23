"""Official city websites from the Oregon Blue Book (Secretary of State).

python tools/bluebook.py tools/or-cities.tsv  ->  BLUEBOOK lines: name, county, website
Run in CI, where sos.oregon.gov is reachable.
"""
import re, sys
from concurrent.futures import ThreadPoolExecutor
import requests

UA = {"User-Agent": "Mozilla/5.0 (CivicsOR meeting finder; +https://civicsor.org)"}
BASE = "https://sos.oregon.gov/blue-book/Pages/local/cities"


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower().replace(".", "")).strip("-")


def folder(name):
    c = name[0].lower()
    return "a-k" if c <= "k" else "l-r" if c <= "r" else "s-z"


def find(row):
    name, county = row[0], row[1]
    statuses = []
    cands = dict.fromkeys([slug(name), slug(name).replace("-", ""), slug(name.replace("St. ", "Saint ").replace("Mt. ", "Mount "))])
    for url in [f"https://sos.oregon.gov/blue-book/government/Pages/{s}.aspx" for s in cands] + [f"{BASE}/{folder(name)}/{s}.aspx" for s in cands]:
        try:
            r = requests.get(url, headers=UA, timeout=20)
        except Exception:
            continue
        statuses.append(r.status_code)
        if r.status_code == 200 and "Web:" in r.text:
            m = re.search(r"Web:\s*(?:</?[^>]+>\s*)*<a[^>]+href=\"([^\"]+)\"", r.text, re.I) or \
                re.search(r"Web:\s*(?:</?[^>]+>\s*)*((?:https?://)?www\.[a-z0-9.-]+\.[a-z]{2,}[^\s<\"]*)", r.text, re.I)
            if m:
                site = m.group(1)
                return name, county, site if site.startswith("http") else "https://" + site, url
            return name, county, "", url
    return name, county, "", "statuses " + ",".join(map(str, statuses))


if __name__ == "__main__":
    rows = [l.rstrip("\n").split("\t") for l in open(sys.argv[1]) if l.strip()]
    with ThreadPoolExecutor(8) as ex:
        for name, county, site, page in ex.map(find, rows):
            print("BLUEBOOK", f"{name}\t{county}\t{site}\t{page}")
