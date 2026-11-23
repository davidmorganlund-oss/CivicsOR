"""List Oregon school districts and their websites from ODE's school directory.

Downloads the Oregon School Directory PDF and writes a TSV of district name,
county, website for probe.py. Run in CI: python tools/ode.py tools/schools.tsv
"""
import re, subprocess, sys
import requests

UA = {"User-Agent": "Mozilla/5.0 (CivicsOR meeting finder; +https://civicsor.org)"}
PAGE = "https://www.oregon.gov/ode/about-us/Pages/School-Directory.aspx"


def directory_text():
    page = requests.get(PAGE, headers=UA, timeout=30).text
    links = re.findall(r'href="([^"]*CombinedDirectory[^"]*\.pdf)"', page, re.I)
    url = links[0] if links else "https://www.oregon.gov/ode/about-us/Documents/CombinedDirectory_20261110_010505.pdf"
    if url.startswith("/"):
        url = "https://www.oregon.gov" + url
    print("DIRECTORY", url)
    open("dir.pdf", "wb").write(requests.get(url, headers=UA, timeout=120).content)
    return subprocess.run(["pdftotext", "-layout", "dir.pdf", "-"], capture_output=True, text=True).stdout


if __name__ == "__main__":
    text = directory_text()
    if len(sys.argv) > 2 and sys.argv[2] == "dump":
        i = text.find("School District")
        for line in text.splitlines()[:4000]:
            if re.search(r"SD|School District|www\.|http|County", line):
                print("DUMP", line.rstrip()[:160])
        sys.exit(0)
    rows, name = [], None
    for line in text.splitlines():
        m = re.match(r"\s*([A-Z][A-Za-z.'/ -]+?(?:SD|School District|Schools)\b[^\s]*(?: [0-9A-Z]{1,5})?)\s{2,}", line)
        if m:
            name = m.group(1).strip()
        w = re.search(r"((?:https?://)?(?:www\.)?[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:org|net|com|us|edu|k12\.or\.us)(?:/[^\s]*)?)", line, re.I)
        if name and w and "oregon.gov" not in w.group(1):
            url = w.group(1)
            rows.append((name, "", url if url.startswith("http") else "https://" + url))
            name = None
    seen = set()
    with open(sys.argv[1], "w") as f:
        for n, c, u in rows:
            if n not in seen:
                seen.add(n)
                f.write(f"{n}\t{c}\t{u}\n")
    print(len(seen), "districts with websites")
