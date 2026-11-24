# Running CivicsOR

CivicsOR is a static site on GitHub Pages (custom domain civicsor.org, registered at
Namecheap). A GitHub Actions workflow rebuilds the calendar every night. There is no
server, database or paid service.

## What runs, and when

- **Refresh and publish** (`.github/workflows/refresh.yml`) runs nightly at 11:17 UTC
  (3:17 a.m. Pacific in winter), on every push to `main` that changes the site or the
  pipeline, and on demand from the Actions tab. It runs the tests, reads every
  calendar in `pipeline/sources.yml` (`pipeline/build.py`), updates representatives
  (`pipeline/officials.py`), commits the data in `site/data/`, and deploys `site/` to
  GitHub Pages.
- **Link check** (`.github/workflows/links.yml`) runs weekly and opens an issue for
  outside links that stop working.
- **Alerts** (`pipeline/alerts.py`): when a calendar has failed three nights in a row,
  the run opens or updates the GitHub issue "Calendar sources need attention", and
  closes it when everything reads again. Watch the repository to get those emails.
- When a calendar can't be read, the site keeps showing what it listed the last time
  it worked, and the coverage page says so.
- GitHub Actions are pinned to full commit SHAs; the repository requires it.

## Adding or fixing a calendar

1. **Find the platform.** Run "Find calendars" (`.github/workflows/discover.yml`)
   from the Actions tab. Its `list` input takes:
   - `all`: guess every city's website (`tools/find_homes.py`), then scan cities and
     counties. Prefer the next option; the guesser gets about a third of cities wrong.
   - a TSV in `tools/` (name, county, homepage), like `tools/discover.tsv`, which
     holds every city's official website from the Oregon Blue Book. Pushing a change
     to `tools/discover.tsv` also starts a scan.
   - `schools`: school districts from the Oregon Department of Education directory
     (`tools/ode.py`); `tools/schools.tsv` is the cleaned list.
   - `bluebook`: re-read each city's official website from the Oregon Blue Book
     (`tools/bluebook.py`).

   Each scanned site prints a `PROBE` line saying which meeting software it links to.
2. **Make candidates.** `python3 tools/gen_candidates.py probe.jsonl tools/candidates.yml city`
   (or `school`) turns the PROBE lines into source entries.
3. **Try them.** Pushing `tools/candidates.yml` runs "Trial sources" (`tools/trial.py`),
   which prints a `TRIAL` line per source: how many upcoming meetings it found, a few
   titles, or the error.
4. **Check the city.** Before adding a source, confirm it's the Oregon city and not a
   same-named one elsewhere. (The first scan matched Jacksonville and Elgin to cities
   in Florida and Illinois.)
5. **Add it** to `pipeline/sources.yml`. The comment at the top of that file lists the
   fields. Push; the next run picks it up.

Supported platforms include Legistar, CivicClerk, CivicPlus, CivicWeb, PrimeGov,
Granicus agenda feeds, Apptegy school sites, iCalendar feeds (WordPress, Finalsite),
BiblioCommons library events, OLIS for the Legislature, and published standing
schedules (`type: schedule`, shown as "Usually meets").

**School boards on BoardBook** (`type: boardbook`, with the number from the board's
BoardBook address as `organization`) usually post a meeting about a week ahead. For
the largest districts the source also has a `regular_schedule`: the dates the board
publishes for the year. Those show as "Usually meets" until the board posts that
day's meeting, and then the posting, with its agenda, takes over. Update each
`regular_schedule` every summer, when boards adopt the next year's calendar.

**Rules we keep:** respect sites that ask automated readers to stay out. The reader
checks `robots.txt` and skips anything it disallows. That rules out, for now, Google
Calendar feeds, BoardDocs, many Finalsite school calendars and several CivicWeb and
Granicus portals; for those places the site links to the body's own meeting page.

## Large cities without a readable calendar

Councils that don't publish a feed are listed from their published regular schedule
(`type: schedule`). Schedules change, usually in January. Check them each winter
against each city's council page, which is the `homepage` of each source.

## Pages

- Most pages are written by `tools/pages/gen.py` from the guide text in
  `tools/pages/guides_or.py` and `tools/pages/guides_or2.py`. Edit those, then run
  `python3 tools/pages/gen.py`. It also writes `sitemap.xml` and `robots.txt`.
- `site/legislature.js` (the Legislature page), `site/coverage.js` and `site/app.js`
  read the data files in the browser.
- `site/data/local.json`: county sites, city sites (from the Oregon Blue Book) and
  school districts (from the ODE directory), used by the "Near you" boxes.
- The 2027 session starts in January. In `site/legislature.js`, update `SESSION_YEAR`
  before the 2028 short session.

## Accounts and renewals

- **GitHub:** `davidmorganlund-oss/CivicsOR`. The "Protect main" ruleset blocks
  deleting `main` and force-pushes. Give at least one other BarNone person admin access
  so the site doesn't depend on one account.
- **Domain:** civicsor.org at Namecheap, with auto-renew, domain lock, WHOIS privacy
  and DNSSEC on. DNS has GitHub Pages A and AAAA records, `www` as a CNAME, a CAA
  record limiting certificates to Let's Encrypt, and a DMARC record rejecting mail
  that claims to be from civicsor.org (the domain sends no mail).
- **Search engines:** Google Search Console (domain property, verified by DNS) and
  Bing Webmaster Tools (verified by a DNS CNAME). The sitemap is submitted to both.
- **Corrections and accessibility reports** go to admin@barnoneinc.org.
- **Security:** code scanning (CodeQL), Dependabot alerts, secret scanning and private
  vulnerability reporting are on.
