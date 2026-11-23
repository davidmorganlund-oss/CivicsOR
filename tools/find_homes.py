"""Find each Oregon city's official website by trying the usual address patterns.

Reads tools/or-cities.tsv (name, county, population) and writes a TSV of
name, county, homepage for probe.py. A guess counts only when the page answers
and names the city and Oregon. Run in CI, where the sites are reachable:
python tools/find_homes.py tools/or-cities.tsv tools/cities.tsv
"""
import re, sys
from concurrent.futures import ThreadPoolExecutor
import requests

UA = {"User-Agent": "Mozilla/5.0 (CivicsOR meeting finder; +https://civicsor.org)"}
PATTERNS = [
    "https://www.{s}oregon.gov/", "https://{s}oregon.gov/", "https://www.{s}or.gov/", "https://{s}or.gov/",
    "https://www.{h}-or.gov/", "https://www.{h}-oregon.gov/", "https://www.cityof{s}.org/",
    "https://www.ci.{s}.or.us/", "https://www.ci.{h}.or.us/", "https://www.{s}.or.us/", "https://www.cityof{s}.com/",
    "https://www.{s}.org/", "https://www.cityof{s}or.gov/", "https://www.cityof{s}oregon.gov/", "https://cityof{s}.org/",
    "https://www.{s}city.org/", "https://www.{s}.gov/", "https://www.cityof{s}.net/", "https://www.{s}.com/",
    "https://www.{s}.us/", "https://www.{s}oregon.org/", "https://www.{s}or.us/", "https://{s}.org/",
]


def slugs(name):
    base = name.lower().replace("st. ", "saint ").replace("mt. ", "mount ")
    s = re.sub(r"[^a-z]", "", base)
    h = re.sub(r"[^a-z]+", "-", base).strip("-")
    short = re.sub(r"[^a-z]", "", name.lower())  # sthelens, mtangel
    return {s, short}, {h}


def looks_right(name, text):
    t = text.lower()
    words = [w for w in re.findall(r"[a-z]+", name.lower()) if w not in ("st", "mt")]
    return all(w in t for w in words) and ("oregon" in t or " or " in t or ", or" in t)


def find(row):
    name, county = row[0], row[1]
    ss, hs = slugs(name)
    tried = []
    for p in PATTERNS:
        for s in ss:
            for h in hs:
                url = p.format(s=s, h=h)
                if url in tried:
                    continue
                tried.append(url)
                try:
                    r = requests.get(url, headers=UA, timeout=12, allow_redirects=True)
                except Exception:
                    continue
                if r.status_code < 400 and looks_right(name, r.text[:60000]):
                    return name, county, r.url
    return name, county, ""


if __name__ == "__main__":
    rows = [l.rstrip("\n").split("\t") for l in open(sys.argv[1]) if l.strip()]
    with ThreadPoolExecutor(24) as ex:
        out = list(ex.map(find, rows))
    with open(sys.argv[2], "w") as f:
        for name, county, home in out:
            if home:
                f.write(f"{name}\t{county}\t{home}\n")
    for name, county, home in out:
        print("HOME", name, "|", county, "|", home or "NOT FOUND")
    print(sum(1 for o in out if o[2]), "of", len(out), "found")
