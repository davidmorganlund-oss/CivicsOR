# CivicsOR

A civic calendar, Engage guides and a "who represents you" lookup for Oregon.
A project of BarNone, an independent nonprofit. Not affiliated with any
government agency. Sister site to CivicsWA (civicswa.org) and CivicsID (civicsid.org).

**Status: live at civicsor.org since November 2026.** See [OPERATIONS.md](OPERATIONS.md) for how it runs and how to add calendars.

Built from CivicsID's code: the same pipeline, connectors, page generator and
nightly publish, rewritten for Oregon.

## How it works

- `pipeline/sources.yml` lists the public calendars and published schedules the site reads.
- `pipeline/build.py` reads each one and writes `site/data/events.json`,
  `site/data/status.json`, the subscribable calendars in `site/data/ics/` and
  the what's-new feeds in `site/data/feeds/`.
- `pipeline/officials.py` writes `site/data/officials.json` (state senators,
  state representatives and members of Congress) for the lookup page.
- `.github/workflows/refresh.yml` runs both every night, saves the result and
  publishes the site with GitHub Pages.
- `.github/workflows/links.yml` checks every outside link weekly.
- `site/` is a plain static site that reads those files. No accounts, no tracking.
- `tools/pages/gen.py` writes the guide, Engage, calendar, Legislature, reps,
  About, Coverage and privacy pages from `tools/pages/guides_or.py` and
  `tools/pages/guides_or2.py` (27 guides). Run `python3 tools/pages/gen.py`.
- `tools/` also holds the calendar finder (`probe.py`, `find_homes.py`,
  `bluebook.py`, `ode.py`, `gen_candidates.py`, `trial.py`), run by the
  "Find calendars" and "Trial sources" workflows.

## Oregon specifics

- **Time zones.** Nearly all of Oregon is on Pacific time; most of Malheur County is
  on Mountain. Sources default to Pacific; a Malheur source sets `timezone: America/Boise`.
- **The Legislature** comes from its own public OData service (OLIS), via the
  `oregon_legislature` connector: meetings, hearing rooms, agenda links, each bill
  on the agenda with its OLIS description, and topic tags for the Legislature page.
- **Districts.** 30 Senate districts, 60 House districts; each Senate district is two
  House districts. The reps lookup reads both from the Census geocoder.
- **Regional bodies.** Metro serves three counties. A source can list
  `counties: [...]` and its meetings show in each county's view and calendar file.
- **Holidays.** Regular schedules skip Oregon legal holidays (ORS 187.010) and
  Thanksgiving unless a meeting sets `skip_holidays: false`.

## Sources (November 2026)

| Source | County | How | Notes |
|---|---|---|---|
| Oregon Legislature | Statewide | OLIS OData (`oregon_legislature`) | Interim committees now; standing committees in session |
| Metro | Multnomah, Washington, Clackamas | Legistar | Agenda highlights |
| City of Portland | Multnomah | Published schedule | 9:30 a.m. 1st, 2nd, 4th, 5th Wednesdays; 6 p.m. 3rd Wednesday |
| Multnomah County | Multnomah | Published schedule | Thursday meetings, Tuesday briefings |
| Multnomah County Library | Multnomah | BiblioCommons | Civic programs only |
| Washington County | Washington | Published schedule | Work sessions and business meetings |
| City of Hillsboro | Washington | Published schedule | 1st and 3rd Tuesdays |
| WCCLS libraries | Washington | BiblioCommons | Civic programs only |
| Clackamas County | Clackamas | Published schedule | Thursday business meetings |
| City of Oregon City | Clackamas | CivicClerk | |
| City of Salem | Marion | Published schedule | 2nd and 4th Mondays |

Every county has at least a link to its own website in `site/data/local.json`.
`inventory/sources.csv` lists what is next.

## Guides (first set)

Contact your representatives, voting in Oregon (including after a conviction),
local government and land use, speaking at a public meeting, the Public Meetings
Law, public records requests, the Legislature, weighing in on a state bill,
initiatives and referendums, a two-minute pitch, reading a bill or agenda,
problem to policy, and media literacy. Federal guides, courts, budgets, campaign
finance, boards and commissions, and running for office come next, then Spanish.

## Reading only what sites allow

Every request the pipeline makes checks the site's robots.txt first. A source whose
address is disallowed fails with a clear message, shows nothing, and is listed in
the upkeep issue.

## Security

Same as CivicsID: static site, everything from outside treated as untrusted and
inserted as text, links checked, a Content-Security-Policy on every page, pinned
Actions and packages. Tests in `tests/test_normalize.py`.

The representatives page's policy also allows `services.arcgis.com` and
`maps.oda.oregon.gov`, where the State Fire Marshal, the state's education
boundaries and the Department of Agriculture publish district maps.
`site/districts.js` sends them only the map point the Census Bureau returned,
never the address.

## Run it yourself

    pip install -r requirements.txt
    python -m pytest -q tests
    python pipeline/build.py
    python pipeline/officials.py
    python -m http.server --directory site 8000

## Look

Coast teal on driftwood: teal #0E5C63 for text, links and buttons; driftwood
#E6DED2 and sand #F8F5F0 for large areas; weathered stone #8A7B68 as a second
accent. Inter, Source Serif 4 and Barlow Condensed. Variables at the top of
`site/styles.css`; share card and icons from `tools/brand/render.js`.
