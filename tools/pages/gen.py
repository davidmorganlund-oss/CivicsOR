"""Generator for CivicsOR's static pages (guides, Engage, reps, calendar shell).
Run: python3 tools/pages/gen.py  -- writes plain HTML into site/.
Spanish pages (site/es/) come from the same file: the calendar, the address
lookup, About, Privacy, a short Spanish Engage page, and the guides in
tools/pages/guides_or_es.py. A guide with a Spanish twin gets an Español link
and hreflang tags automatically."""
import html, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import guides_or
import guides_or2  # noqa: E402
import guides_or_es  # noqa: E402

SITE = Path(__file__).resolve().parents[2] / "site"
# The reps page also loads three state district maps and, for Portland and
# Multnomah County addresses, the City's and County's district maps (JSONP).
REPS_SCRIPTS = " https://services.arcgis.com https://maps.oda.oregon.gov https://www.portlandmaps.com https://www3.multco.us"
FONTS = ('<link rel="preload" href="{up}fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>\n'
         '<link rel="preload" href="{up}fonts/source-serif-4-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>')
SITE_URL = "https://civicsor.org/"
REPORT = "admin@barnoneinc.org"
NOTICE = '<aside class="notice" aria-label="About CivicsOR">A project of BarNone, a nonprofit. Not affiliated with any government agency.</aside>'
BY = ('<p class="by-barnone"><a href="https://barnoneinc.org"><img src="{up}barnone-phoenix.png" alt="" width="28" height="28">'
      '<span>A service of <strong>BarNone, Inc.</strong></span></a> An independent nonprofit. CivicsOR is not a government website, '
      'is not affiliated with any government agency, and does not speak for any public office.</p>')


# The Spanish share card. tools/brand/render.js draws it (it needs Playwright's
# browser); until site/share-es.png exists, Spanish pages share the English card.
ES_SHARE = (SITE / "share-es.png").exists()


def head(title, up, desc, share=None, lang="en", scripts=""):
    """scripts: extra hosts this page may load scripts from, for its CSP."""
    share = share or title.split(" | ")[0]
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' https://geocoding.geo.census.gov{scripts}; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; manifest-src 'self'; worker-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; upgrade-insecure-requests">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
<meta property="og:site_name" content="CivicsOR">
<meta property="og:title" content="{html.escape(share, quote=True)}">
<meta property="og:description" content="{html.escape(desc, quote=True)}">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE_URL}{"share-es.png" if lang == "es" and ES_SHARE else "share.png"}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{"CivicsOR: Participe, Oregon." if lang == "es" and ES_SHARE else "CivicsOR: Get Engaged, Oregon."}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0E5C63">
<link rel="manifest" href="{up}manifest.webmanifest">
<link rel="icon" href="{up}favicon.ico" sizes="32x32">
<link rel="icon" href="{up}icon-192.png" type="image/png">
<link rel="apple-touch-icon" href="{up}apple-touch-icon.png">
{FONTS.format(up=up)}
<link rel="stylesheet" href="{up}styles.css">
<script src="{up}app-install.js" defer></script>
</head>
<body>'''


NAV = {"en": ("Community Calendar", "Calendar", "Engage", "My representatives", "My reps", "Main", "Legislature"),
       "es": ("Calendario comunitario", "Calendario", "Participe", "Mis representantes", "Mis reps", "Principal", "Legislatura (en inglés)")}


def top(up, current, lang="en", alt=None):
    """alt: link to this page in the other language. The Legislature page is
    English only, so Spanish pages link to it from /es/ marked "(en inglés)"."""
    cal, cal_s, eng, reps, reps_s, main, leg = NAV[lang]
    notice = NOTICE if lang == "en" else '<aside class="notice" aria-label="Acerca de CivicsOR">Un proyecto de BarNone, una organización sin fines de lucro. No está afiliado a ninguna agencia de gobierno.</aside>'
    switch = (f'\n  <a class="lang-switch" href="{alt}" lang="{"es" if lang == "en" else "en"}" hreflang="{"es" if lang == "en" else "en"}">{"Español" if lang == "en" else "English"}</a>' if alt else "")
    def a(href, label, key, short=None):
        cur = ' aria-current="page"' if key == current else ""
        if short:  # a shorter label on phones; the full name stays for screen readers
            return f'    <a href="{up}{href}"{cur} aria-label="{label}"><span class="full">{label}</span><span class="short">{short}</span></a>'
        return f'    <a href="{up}{href}"{cur}>{label}</a>'
    leg_link = a("legislature.html", leg, "legislature")
    if lang == "es":
        leg_link = a("legislature.html", leg, "legislature", "Legislatura").replace(
            f'href="{up}legislature.html"', f'href="{up}../legislature.html" hreflang="en"')
    return f'''{notice}

<header class="top"><div class="wrap">
  <a class="brand" href="{up}index.html">Civics<span>OR</span></a>{switch}
  <nav aria-label="{main}">
{a("index.html", cal, "calendar", cal_s)}
{leg_link}
{a("engage.html", eng, "engage")}
{a("reps.html", reps, "reps", reps_s)}
  </nav>
</div></header>'''


def footer(up, first):
    return f'''<footer><div class="wrap">
  <p>{first}</p>
  {BY.format(up=up)}
  <p class="footer-links"><a href="{up}about.html">About</a> · <a href="{up}coverage.html">Coverage</a> · <a href="{up}privacy.html">Privacy</a> · <a href="{up}about.html#accessibility">Accessibility</a> · <a href="mailto:{REPORT}?subject=CivicsOR%3A%20report%20a%20problem">Report a problem or a missing meeting</a></p>
</div></footer>'''


# ---------- guides ----------
ALL = {**guides_or.G, **guides_or2.G}
for slug, g in ALL.items():
    sources = "\n".join(f'    <li><a href="{html.escape(u, quote=True)}" rel="noopener">{html.escape(t)}</a></li>' for u, t in g["sources"])
    script = '\n<script src="../local.js"></script>' if 'class="near-you"' in g["body"] else ""
    # "short" and "desc" are optional: a shorter <title> and meta description
    # for guides whose heading or lede runs past what search results show.
    page = f'''{head(g.get("short", g["title"]) + " | CivicsOR", "../", g.get("desc", g["lede"]))}
<a class="skip" href="#guide">Skip to guide</a>
{top("../", "engage", alt=("../es/guides/" + slug + ".html") if slug in guides_or_es.G else None)}

<main class="wrap narrow guide" id="guide">
  <p class="eyebrow"><a href="../engage.html">Engage</a> · {g["cat"]}</p>
  <h1>{html.escape(g["title"])}</h1>
  <p class="lede">{html.escape(g["lede"])}</p>
{g["body"].strip(chr(10))}

  <h2>Sources</h2>
  <ul class="sources-list">
{sources}
  </ul>
  <p class="muted">Last reviewed November 2026. This guide is general information, not legal advice. Rules change, so check the linked sources before you rely on a deadline.</p>
</main>

{footer("../", "Every guide lists its sources so you can check them yourself.")}{script}
</body>
</html>
'''
    (SITE / "guides" / f"{slug}.html").write_text(page)

# ---------- engage ----------
SECTIONS = [
    ("Start here", [
        ("reps.html", "Who represents you", "Enter your address to see your state legislators, members of Congress, and your city and county."),
        ("guides/contact-your-representatives.html", None, "Picking the right office and writing a message that gets read."),
        ("guides/voting-in-oregon.html", None, "Registering, returning your ballot on time, and voting after a conviction."),
    ]),
    ("Your city and county", [
        ("guides/local-government.html", None, "Counties, cities, Metro, special districts, and Oregon's land use system."),
        ("guides/speak-at-a-public-meeting.html", None, "What Oregon's Public Meetings Law gives you, what it doesn't, and how to use two minutes well."),
        ("guides/public-meetings-law.html", None, "Notice, executive sessions, minutes, and what to do when a board breaks the rules."),
        ("guides/public-records-requests.html", None, "How to ask for emails, contracts and reports, what it costs, the deadlines, and what to do if they say no."),
        ("guides/your-neighborhood.html", None, "Neighborhood associations, county engagement programs, and getting notice of land use decisions near you."),
        ("guides/your-school-board.html", None, "What school boards decide, May elections, and how to speak up or run."),
        ("guides/local-ballot-measures.html", None, "Bonds, levies, the double majority, and reading your voters' pamphlet."),
    ]),
    ("The State of Oregon", [
        ("guides/legislature.html", None, "Who's in it, long and short sessions, how a bill moves, and where your voice counts."),
        ("guides/weigh-in-on-a-state-bill.html", None, "Testifying in person or remotely, written testimony, and the timing that catches people."),
        ("guides/state-budgets.html", None, "The two-year state budget, the kicker, and the local budget committees residents sit on."),
        ("guides/state-agencies.html", None, "The Oregon Bulletin, commenting on proposed rules, and getting help with an agency."),
        ("guides/state-initiatives.html", None, "Initiatives, referendums and referrals, the signature rules, and the Citizens' Initiative Review."),
        ("guides/constitution.html", None, "What Oregon's constitution does and how voters change it."),
        ("guides/courts.html", None, "How the courts fit together, elected judges, jury service and watching a case."),
        ("guides/boards-and-commissions.html", None, "Applying to state and local boards, and what serving involves."),
    ]),
    ("Elections and campaigns", [
        ("guides/running-for-office.html", None, "Which offices are up when, how to file, and the deadlines."),
        ("guides/campaign-finance.html", None, "Looking up campaign money in ORESTAR, and Oregon's new contribution limits."),
        ("guides/federal-offices.html", None, "Congress and the President: who can run and how Oregon runs those elections."),
    ]),
    ("Federal", [
        ("guides/federal-agencies.html", None, "Casework help, public lands decisions, commenting on rules and FOIA requests."),
        ("guides/federal-budget.html", None, "How Congress writes the budget and where you can weigh in."),
    ]),
    ("Skills", [
        ("guides/two-minute-pitch.html", None, "A simple shape for making your case in the time you get."),
        ("guides/read-a-bill-or-agenda.html", None, "Bill numbers, bold type and brackets, consent agendas and packets."),
        ("guides/problem-to-policy.html", None, "Finding the right level of government and shaping a specific ask."),
        ("guides/media-literacy.html", "Media literacy", "Quick habits for sorting good information from bad."),
        ("guides/volunteer-and-public-service.html", None, "Volunteering, giving wisely, and public service jobs."),
    ]),
]
blocks, listed = [], set()
for i, (heading, items) in enumerate(SECTIONS):
    style = ' style="margin-top: 20px"' if i else ""
    rows = []
    for href, label, blurb in items:
        if href.startswith("guides/"):
            slug = href[7:-5]
            listed.add(slug)
            label = label or ALL[slug]["title"]
        rows.append(f'    <li><a href="{href}">{html.escape(label)}<span>{html.escape(blurb)}</span></a></li>')
    blocks.append(f'  <h2{style}>{heading}</h2>\n  <ul class="guide-links">\n' + "\n".join(rows) + "\n  </ul>")
assert listed == set(ALL), (listed ^ set(ALL))
(SITE / "engage.html").write_text(f'''{head("Engage | CivicsOR", "", "Plain-language guides to how government works in Oregon and where you can step in.")}
<a class="skip" href="#guides">Skip to guides</a>
{top("", "engage", alt="es/engage.html")}

<section class="hero plain"><div class="wrap">
  <h1>Engage: how to take part, from your block to Congress.</h1>
  <p class="lede">Plain-language guides to how government works in Oregon and where you can step in. Every guide lists its sources so you can check them yourself. More guides are on the way.</p>
</div></section>

<main class="wrap" id="guides" style="padding-block: 32px 64px; display: flex; flex-direction: column; gap: 20px">
{chr(10).join(chr(10) + b if i else b for i, b in enumerate(blocks))}
</main>

{footer("", "Guides are written in plain language, list their sources, and are built to work with screen readers.")}
</body>
</html>
''')

# ---------- calendar ----------
(SITE / "index.html").write_text(f'''{head("Get Engaged, Oregon | CivicsOR", "", "See what your city council, county commissioners, Metro and the Oregon Legislature are deciding this week, and how to make your voice heard.", "Get Engaged, Oregon: what your community is deciding this week")}
<a class="skip" href="#events">Skip to events</a>
{top("", "calendar", alt="es/index.html")}

<section class="hero"><div class="wrap">
  <p class="eyebrow light">Community Calendar</p>
  <h1>Find out what your community is deciding this week.</h1>
  <p class="lede">City councils, county commissioners, public hearings and the Legislature, from across Oregon, in one calendar. Pick where you live and we'll show you what's near you.</p>
  <form class="search" id="search">
    <div class="field">
      <label for="county">County</label>
      <select id="county"><option value="">All of Oregon</option></select>
    </div>
    <div class="field">
      <label for="city">City</label>
      <select id="city" disabled><option value="">Pick a county</option></select>
    </div>
  </form>
  <p class="small"><span id="coverage">Meetings from across Oregon, with links to each county's own page where we can't read its calendar yet.</span> No account needed, and your choice stays in your browser.</p>
</div></section>

<div class="wrap layout">
  <main class="main" id="events">
    <div class="heading">
      <h2 id="heading">Coming up across Oregon</h2>
      <span id="range"></span>
    </div>
    <p class="muted" id="place-msg" role="status" hidden></p>
    <div class="find">
      <label for="q">Search meetings and agendas</label>
      <input id="q" type="search" placeholder="Try zoning, library, budget, schools" autocomplete="off">
    </div>
    <div class="chips" role="group" aria-label="Filter by type" id="chips"></div>
    <div class="list" id="list" aria-live="polite"><p class="empty">Loading events…</p></div>
    <button class="more" id="more" type="button" hidden>Show two more weeks</button>
  </main>

  <aside class="side">
    <div class="card">
      <h2>Get it on your phone</h2>
      <p id="subscribe-text">Subscribe once and these meetings show up in the calendar app you already use.</p>
      <a class="link" id="subscribe" href="data/ics/statewide.ics">Subscribe to Oregon Legislature committee meetings</a>
      <p style="margin-top: 14px">Want to hear when something changes? The <a id="feed" href="data/feeds/statewide.xml">what's-new feed</a> lists new meetings, newly posted agendas and cancellations. Add it to a feed reader, or to a free feed-to-email service to get it by email.</p>
    </div>
    <div class="card">
      <h2>Use it like an app</h2>
      <p>Add CivicsOR to your home screen and it opens like an app, even without a signal. On iPhone, tap Share, then <strong>Add to Home Screen</strong>. On Android, tap the menu, then <strong>Install app</strong> or <strong>Add to Home screen</strong>.</p>
    </div>
    <div class="card">
      <h2>Two time zones</h2>
      <p>Each meeting is listed in its own local time: Pacific for nearly all of Oregon, Mountain for most of Malheur County.</p>
    </div>
    <div class="card">
      <h2>The Legislature, day by day</h2>
      <p>Committee hearings with their agendas, and how to sign up to testify in person or remotely. The 2027 long session starts in January.</p>
      <a class="link" href="legislature.html">See what's coming up at the Capitol</a>
    </div>
    <div class="card warm">
      <span class="eyebrow">Engage</span>
      <h2>First time at a public meeting?</h2>
      <p>What Oregon law lets you do, what to say in two minutes, and what happens after you speak.</p>
      <a class="link" href="guides/speak-at-a-public-meeting.html">Read the guide</a>
    </div>
  </aside>
</div>

{footer("", 'Listings come straight from public agency calendars and are refreshed every night. <span id="updated"></span> Schedules change, so confirm with the host before you go.')}

<script src="app.js"></script>
</body>
</html>
''')

# ---------- representatives ----------
(SITE / "reps.html").write_text(f'''{head("Who represents you | CivicsOR", "", "Enter an Oregon street address to see every district you live in, your state legislators and members of Congress, and where to find city and county officials.", scripts=REPS_SCRIPTS)}
<a class="skip" href="#results">Skip to results</a>
{top("", "reps", alt="es/reps.html")}

<section class="hero"><div class="wrap">
  <h1>Find who represents you.</h1>
  <p class="lede">Enter an Oregon street address to see every district you live in, from Congress down to your fire district, plus your state senator, state representative and members of Congress and how to reach them.</p>
  <form class="search" id="lookup">
    <div class="field wide">
      <label for="address">Street address</label>
      <input id="address" name="address" type="text" autocomplete="street-address" placeholder="900 Court St NE, Salem">
    </div>
    <button class="btn" type="submit">Look up</button>
  </form>
  <p class="small">Your address is sent from your browser to the U.S. Census Bureau's address lookup to find your districts. Only the map point it returns, not your address, goes to public state maps to find your fire, education and conservation districts, and, for Portland and Multnomah County addresses, to the City's and County's district maps. CivicsOR never receives or stores either. Your browser remembers only your county and city, so the Engage guides can show local links.</p>
</div></section>

<main class="wrap narrow" style="padding-block: 40px 64px">
  <p class="term-note" id="term-note" hidden></p>
  <div class="list" id="results" aria-live="polite">
    <p class="empty">Your representatives will show up here.</p>
  </div>
  <p class="muted" style="margin-top: 24px">Not sure what to say once you have a name? Read <a href="guides/contact-your-representatives.html">how to contact the people who represent you</a>.</p>
</main>

{footer("", "State legislators come from Open States, a public roster built from the Oregon Legislature's member pages, and members of Congress from a public roster. Both are refreshed nightly. County links cover all 36 counties, and city links cover the official websites of 226 cities, from the Oregon Blue Book.")}

<script src="local.js"></script>
<script src="districts.js"></script>
<script src="reps.js"></script>
</body>
</html>
''')
print(len(ALL), "guides written")

(SITE / "legislature.html").write_text(f'''{head("The Oregon Legislature, day by day | CivicsOR", "", "Every Oregon Legislature committee meeting coming up, with the bills on each agenda, topic filters, and how to testify in person or remotely.", "The Oregon Legislature, day by day")}
<a class="skip" href="#hearings">Skip to the meetings</a>
{top("", "legislature")}

<section class="hero"><div class="wrap">
  <p class="eyebrow light">Oregon Legislature</p>
  <h1>What the Legislature is hearing, day by day.</h1>
  <p class="lede">Every committee meeting at the Capitol, day by day. See which bills are up, which meetings take public testimony, and how to register before it closes.</p>
  <p class="small" id="session-note">The 2027 long session starts in January. Until then, these are interim committees, which meet during Legislative Days to study issues between sessions.</p>
</div></section>

<div class="wrap layout">
  <main class="main" id="hearings">
    <div class="heading">
      <h2 id="day-heading">Committee meetings</h2>
      <span id="day-count"></span>
    </div>
    <div class="chips days scroll" role="group" aria-label="Pick a day" id="days"></div>
    <div class="find">
      <label for="bill">Find a bill or a word</label>
      <input id="bill" type="search" placeholder="A bill number or a word: HB 2001, sentencing, rent" autocomplete="off">
    </div>
    <div class="topics-wrap" id="topics-wrap" hidden>
      <p class="topics-label" id="topics-label">Follow a topic</p>
      <div class="chips scroll" role="group" aria-labelledby="topics-label" id="topics"></div>
    </div>
    <div class="list" id="list" aria-live="polite"><p class="empty">Loading committee meetings…</p></div>
  </main>

  <aside class="side">
    <div class="card">
      <h2>What the agenda words mean</h2>
      <p><strong>Public hearing.</strong> The committee takes public testimony on the bill. This is your chance to speak, in person or remotely, or to send written testimony.</p>
      <p><strong>Work session.</strong> The committee discusses the bill and may vote on amendments and on sending it to the floor. There's usually no public testimony, but you can watch.</p>
      <p><strong>Informational meeting.</strong> A briefing for the committee from agencies, experts or invited guests. No votes.</p>
    </div>
    <div class="card">
      <h2>How to testify</h2>
      <ol class="tight">
        <li>Find the bill on a committee's agenda. Registration opens once a public hearing is scheduled.</li>
        <li>On the bill's OLIS page, choose <strong>Register to Testify</strong>, in person or remotely by video or phone. Registration closes 30 minutes before the meeting starts.</li>
        <li>Or choose <strong>Submit Testimony</strong> to send it in writing, up to 48 hours after the meeting's scheduled start.</li>
        <li>Keep it short: who you are, where you live, and how the bill would affect you.</li>
      </ol>
      <a class="link" href="https://www.oregonlegislature.gov/citizen_engagement/Pages/How-to-Testify.aspx" rel="noopener">How to testify, from the Legislature</a>
      <a class="link" href="guides/weigh-in-on-a-state-bill.html">How to weigh in on a bill</a>
      <a class="link" href="reps.html">Find your legislators</a>
    </div>
    <div class="card">
      <h2>Watch it live</h2>
      <p>Committee meetings and floor sessions stream live on OLIS, the Legislature's information system, and the recordings are kept. Open a committee's page and pick the meeting date.</p>
      <a class="link" href="https://olis.oregonlegislature.gov/liz/" rel="noopener">Open OLIS</a>
    </div>
    <div class="card">
      <h2>Get it on your phone</h2>
      <p>Subscribe once and every committee meeting shows up in the calendar app you already use.</p>
      <a class="link" href="data/ics/statewide.ics">Subscribe to Legislature committee meetings</a>
    </div>
  </aside>
</div>

{footer("", "Committee meetings, agendas and bill descriptions come from the Oregon Legislature's own public data service and are refreshed every night. <span id=\"updated\"></span> Topics are matched by keyword from the committee's name and each bill's description, so they're a guide, not an official category. Agendas change, so check the committee's page before you go.")}

<script src="legislature.js"></script>
</body>
</html>
''')


# ---------- About and Coverage ----------
(SITE / "about.html").write_text(f'''{head("About | CivicsOR", "", "Who runs CivicsOR, where its meeting listings come from, how current they are, and how to report a mistake.")}
<a class="skip" href="#about">Skip to the page</a>
{top("", "", alt="es/about.html")}

<section class="hero"><div class="wrap">
  <p class="eyebrow light">About</p>
  <h1>About CivicsOR</h1>
  <p class="lede">One place to see what Oregon's public bodies are deciding, and how to take part.</p>
</div></section>

<main class="wrap guide-body" id="about" style="padding-block: 32px 64px; display: flex; flex-direction: column; gap: 16px; max-width: 760px">
<h2>Who runs it</h2>
<p>CivicsOR is a service of BarNone, Inc., an independent nonprofit. It is not a government website. It is not affiliated with any government agency, and it does not speak for any public office. It doesn't take sides on candidates, parties, bills or ballot measures.</p>

<h2>Where the meetings come from</h2>
<p>Every listing comes from a public body's own published calendar: city and county meeting portals, school district calendars, library schedules, regional governments like Metro, and the Oregon Legislature's committee schedule. Each night, CivicsOR reads those calendars and updates the site. Every meeting links back to the host's own page.</p>
<p>A few public bodies publish a standing schedule ("the second and fourth Tuesday at 10 a.m.") instead of a calendar. Those meetings are marked <strong>Regular schedule: confirm first</strong>, because they can be cancelled or moved without the change reaching us. When a standing schedule lands on a state holiday, we leave that date off.</p>

<h2>How current it is</h2>
<p>Listings refresh every night. If a calendar can't be reached, we keep showing what it listed last time and keep trying. The <a href="coverage.html">coverage page</a> shows every calendar we read and when each was last read successfully.</p>
<p><strong>Always confirm with the host before you go.</strong> Agendas, times and rooms change, sometimes the same day.</p>

<h2>What's not here yet</h2>
<p>Some public bodies only post PDFs, or don't post a calendar online at all. CivicsOR reads public meeting notices once a night with a reader that identifies itself, and keeps its requests light. Where a calendar can't be read, the site links to the body's own meeting page instead. The <a href="coverage.html">coverage page</a> lists what's included county by county. The calendar, the address lookup and five of the guides are also <a href="es/index.html" hreflang="es" lang="es">en español</a>; more Spanish pages are planned.</p>

<h2>Found a mistake or a missing meeting?</h2>
<p><a class="link" href="mailto:{REPORT}?subject=CivicsOR%20correction">Report a correction</a></p>
<p class="muted">Email <a href="mailto:{REPORT}">{REPORT}</a>. Tell us what's wrong and where, and include a link to the right information if you have one.</p>

<h2 id="privacy">Privacy</h2>
<p>CivicsOR has no accounts, no ads and no cookies, and it doesn't sell or share information about visitors. The county you pick is saved only in your own browser. <a href="privacy.html">Read the privacy page</a>.</p>

<h2 id="accessibility">Accessibility</h2>
<p>We aim to meet the Web Content Accessibility Guidelines (WCAG) 2.1, level AA. Pages work with a keyboard and screen readers, text meets contrast standards, and the site works on phones. If something gets in your way, please <a href="mailto:{REPORT}?subject=CivicsOR%20accessibility">tell us</a> and we'll fix it.</p>
</main>

{footer("", "CivicsOR reads public calendars every night and links every meeting back to its host.")}
</body>
</html>
''')

(SITE / "coverage.html").write_text(f'''{head("Coverage | CivicsOR", "", "Every public calendar CivicsOR reads each night, county by county, and when each was last read.")}
<a class="skip" href="#coverage">Skip to the list</a>
{top("", "")}

<section class="hero"><div class="wrap">
  <p class="eyebrow light">Coverage</p>
  <h1>What the calendar covers</h1>
  <p class="lede" id="cov-summary">Loading…</p>
</div></section>

<main class="wrap" id="coverage" style="padding-block: 32px 64px; display: flex; flex-direction: column; gap: 12px; max-width: 860px">
  <p>Open a county to see the calendars we read there and when each one was last read. Where we can't read a county's calendars yet, we link to its own meetings page. Know a calendar we're missing? <a href="mailto:{REPORT}?subject=CivicsOR%20missing%20calendar">Tell us</a>.</p>
  <div id="cov-list" style="display: flex; flex-direction: column; gap: 12px"></div>
</main>

{footer("", "Calendars are read every night. When one can't be reached, the site keeps showing what it listed before.")}
<script src="coverage.js"></script>
</body>
</html>
''')


# ---------- Privacy ----------
PRIV_EN = """
  <h2>The short version</h2>
  <p>CivicsOR has no accounts, no ads, no cookies and no tracking or analytics. We don't collect your name, email or address.</p>
  <h2>What stays on your device</h2>
  <ul>
    <li><strong>Your county and city.</strong> When you pick them, your browser remembers them so the calendar opens there next time. That choice is stored only in your browser. Clearing your browser data removes it.</li>
    <li><strong>The app.</strong> If you add CivicsOR to your home screen, your device keeps a copy of the pages and the latest calendar so it works without a signal.</li>
  </ul>
  <h2>What leaves your device</h2>
  <ul>
    <li><strong>Address lookups.</strong> When you look up your representatives, your browser sends the address straight to the U.S. Census Bureau's public geocoder to find your districts. Your browser then sends only the map point the Census Bureau returns, not the address, to public map services run by the Oregon State Fire Marshal, the state's education agencies and the Oregon Department of Agriculture to find fire, education and conservation districts. For an address in Portland or Multnomah County, it also goes to the City of Portland's and Multnomah County's public maps to find your city council and county commissioner districts. Neither passes through us, and we never see or store them.</li>
    <li><strong>Hosting.</strong> The site is hosted on GitHub Pages. Like any web host, GitHub keeps standard server logs, such as IP addresses, for security. We don't get or use those logs.</li>
    <li><strong>Links you follow.</strong> Meeting details, agendas and guide sources open on government and other websites, which have their own privacy policies.</li>
    <li><strong>Problem reports.</strong> If you email us a correction, it goes to BarNone's inbox ({REPORT}). We use it only to fix the site.</li>
  </ul>
  <p class="muted">Updated November 2026. Questions: {REPORT}.</p>
"""
(SITE / "privacy.html").write_text(f'''{head("Privacy | CivicsOR", "", "CivicsOR has no accounts, no ads, no cookies and no tracking.")}
<a class="skip" href="#privacy">Skip to content</a>
{top("", "", alt="es/privacy.html")}
<main class="wrap narrow guide" id="privacy">
  <h1>Privacy</h1>
{PRIV_EN.format(REPORT=REPORT)}
</main>
{footer("", "CivicsOR is free to use and asks nothing of you.")}
</body>
</html>
''')
print("privacy pages written")


# ---------- Spanish (site/es/) ----------
# Same structure as the English pages. Pages in site/es/ use up="" for links
# inside /es/ and "../" (or "../../" for guides) for styles, scripts and data.
ES = SITE / "es"
(ES / "guides").mkdir(parents=True, exist_ok=True)
FOOT_ES = ('<p class="by-barnone"><a href="https://barnoneinc.org"><img src="{up}barnone-phoenix.png" alt="" width="28" height="28">'
           '<span>Un servicio de <strong>BarNone, Inc.</strong></span></a> Una organización independiente sin fines de lucro. CivicsOR no es un sitio '
           'de gobierno, no está afiliado a ninguna agencia de gobierno y no habla en nombre de ningún cargo público.</p>')


def footer_es(up, first):
    """up: the path from this page to the site root."""
    return f'''<footer><div class="wrap">
  <p>{first}</p>
  {FOOT_ES.format(up=up)}
  <p class="footer-links"><a href="{up}es/about.html">Acerca de CivicsOR</a> · <a href="{up}coverage.html" hreflang="en">Cobertura (en inglés)</a> · <a href="{up}es/privacy.html">Privacidad</a> · <a href="{up}es/about.html#accesibilidad">Accesibilidad</a> · <a href="mailto:{REPORT}?subject=CivicsOR%3A%20reportar%20un%20problema">Reportar un problema o una reunión que falta</a></p>
</div></footer>'''


for slug, g in guides_or_es.G.items():
    assert slug in ALL, slug  # every Spanish guide has an English twin
    sources = "\n".join(f'    <li><a href="{html.escape(u, quote=True)}" rel="noopener" hreflang="en">{html.escape(t)}</a></li>' for u, t in g["sources"])
    script = '\n<script src="../../local.js"></script>' if 'class="near-you"' in g["body"] else ""
    (ES / "guides" / f"{slug}.html").write_text(f'''{head(g.get("short", g["title"]) + " | CivicsOR", "../../", g.get("desc", g["lede"]), lang="es")}
<a class="skip" href="#guide">Ir a la guía</a>
{top("../", "engage", lang="es", alt="../../guides/" + slug + ".html")}

<main class="wrap narrow guide" id="guide">
  <p class="eyebrow"><a href="../engage.html">Participe</a> · {g["cat"]}</p>
  <h1>{html.escape(g["title"])}</h1>
  <p class="lede">{html.escape(g["lede"])}</p>
{g["body"].strip(chr(10))}

  <h2>Fuentes</h2>
  <ul class="sources-list">
{sources}
  </ul>
  <p class="muted">Revisado en noviembre de 2026. Esta guía es información general, no asesoría legal. Las reglas cambian, así que revise las fuentes antes de depender de un plazo. La mayoría de las fuentes oficiales están solo en inglés.</p>
</main>

{footer_es("../../", "Cada guía cita sus fuentes para que usted pueda verificarlas.")}{script}
</body>
</html>
''')

ES_SECTIONS = [
    ("Empiece aquí", [
        ("reps.html", "Quién le representa", "Escriba su dirección para ver a sus legisladores estatales, sus miembros del Congreso, y su ciudad y su condado."),
        ("guides/contact-your-representatives.html", None, "Cómo escoger la oficina correcta y escribir un mensaje que sí se lea."),
        ("guides/voting-in-oregon.html", None, "Quién puede votar, cómo registrarse, cómo devolver su boleta a tiempo y cómo votar después de una condena."),
    ]),
    ("Su ciudad y su condado", [
        ("guides/speak-at-a-public-meeting.html", None, "Lo que la Ley de Reuniones Públicas de Oregon le garantiza, lo que no, y cómo aprovechar dos minutos."),
        ("guides/public-records-requests.html", None, "Cómo pedir correos, contratos e informes, cuánto cuesta, los plazos y qué hacer si le dicen que no."),
        ("guides/your-school-board.html", None, "Qué deciden las juntas escolares, las elecciones de mayo y cómo hacerse escuchar o postularse."),
    ]),
]
es_blocks, es_listed = [], set()
for i, (heading, items) in enumerate(ES_SECTIONS):
    style = ' style="margin-top: 20px"' if i else ""
    rows = []
    for href, label, blurb in items:
        if href.startswith("guides/"):
            slug = href[7:-5]
            es_listed.add(slug)
            label = label or guides_or_es.G[slug]["title"]
        rows.append(f'    <li><a href="{href}">{html.escape(label)}<span>{html.escape(blurb)}</span></a></li>')
    es_blocks.append(f'  <h2{style}>{heading}</h2>\n  <ul class="guide-links">\n' + "\n".join(rows) + "\n  </ul>")
assert es_listed == set(guides_or_es.G), (es_listed ^ set(guides_or_es.G))
(ES / "engage.html").write_text(f'''{head("Participe | CivicsOR", "../", "Guías en lenguaje sencillo sobre cómo funciona el gobierno en Oregon y dónde puede participar usted.", lang="es")}
<a class="skip" href="#guides">Ir a las guías</a>
{top("", "engage", lang="es", alt="../engage.html")}

<section class="hero plain"><div class="wrap">
  <h1>Participe: cómo tomar parte, desde su cuadra hasta el Congreso.</h1>
  <p class="lede">Guías en lenguaje sencillo sobre cómo funciona el gobierno en Oregon y dónde puede participar usted. Cada guía cita sus fuentes para que usted pueda verificarlas. Muchas de las páginas oficiales que citamos están solo en inglés.</p>
</div></section>

<main class="wrap" id="guides" style="padding-block: 32px 64px; display: flex; flex-direction: column; gap: 20px">
{chr(10).join(chr(10) + b if i else b for i, b in enumerate(es_blocks))}
  <p class="muted">Estas son las primeras guías en español. Las demás, sobre la Legislatura, el gobierno local, las iniciativas, las cortes y más, todavía están en inglés: <a href="../engage.html" hreflang="en">todas las guías (en inglés)</a>.</p>
</main>

{footer_es("../", "Las guías están escritas en lenguaje sencillo, citan sus fuentes y funcionan con lectores de pantalla.")}
</body>
</html>
''')

(ES / "index.html").write_text(f'''{head("Participe en Oregon | CivicsOR", "../", "Vea lo que deciden esta semana su concejo municipal, los comisionados del condado, Metro y la Legislatura de Oregon, y cómo hacerse escuchar.", "Participe en Oregon: lo que su comunidad decide esta semana", lang="es")}
<a class="skip" href="#events">Ir a las reuniones</a>
{top("", "calendar", lang="es", alt="../index.html")}

<section class="hero"><div class="wrap">
  <p class="eyebrow light">Calendario comunitario</p>
  <h1>Entérese de lo que su comunidad decide esta semana.</h1>
  <p class="lede">Concejos municipales, comisionados del condado, audiencias públicas y la Legislatura, de todo Oregon, en un solo calendario. Elija dónde vive y le mostraremos lo que hay cerca.</p>
  <form class="search" id="search">
    <div class="field">
      <label for="county">Condado</label>
      <select id="county"><option value="">Todo Oregon</option></select>
    </div>
    <div class="field">
      <label for="city">Ciudad</label>
      <select id="city" disabled><option value="">Primero elija un condado</option></select>
    </div>
  </form>
  <p class="small"><span id="coverage">Reuniones de todo Oregon, con enlaces a la página de cada condado cuando todavía no podemos leer su calendario.</span> No necesita cuenta, y su elección se guarda solo en su navegador.</p>
</div></section>

<div class="wrap layout">
  <main class="main" id="events">
    <div class="heading">
      <h2 id="heading">Próximas reuniones en todo Oregon</h2>
      <span id="range"></span>
    </div>
    <p class="muted" id="place-msg" role="status" hidden></p>
    <p class="muted">Los nombres de las reuniones y las agendas vienen de cada entidad y están en inglés.</p>
    <div class="find">
      <label for="q">Buscar reuniones y agendas (escriba en inglés)</label>
      <input id="q" type="search" placeholder="Pruebe zoning, library, budget, schools" autocomplete="off">
    </div>
    <div class="chips" role="group" aria-label="Filtrar por tipo" id="chips"></div>
    <div class="list" id="list" aria-live="polite"><p class="empty">Cargando reuniones…</p></div>
    <button class="more" id="more" type="button" hidden>Mostrar dos semanas más</button>
  </main>

  <aside class="side">
    <div class="card">
      <h2>En su teléfono</h2>
      <p id="subscribe-text">Suscríbase una vez y estas reuniones aparecerán en la aplicación de calendario que ya usa.</p>
      <a class="link" id="subscribe" href="../data/ics/statewide.ics">Suscribirse a las reuniones de comités de la Legislatura de Oregon</a>
      <p style="margin-top: 14px">¿Quiere saber cuándo cambia algo? El <a id="feed" href="../data/feeds/statewide.xml">canal de novedades</a> muestra reuniones nuevas, agendas recién publicadas y cancelaciones. Agréguelo a un lector de noticias (feed reader), o a un servicio gratuito que lo envíe por correo electrónico.</p>
    </div>
    <div class="card">
      <h2>Úselo como aplicación</h2>
      <p>Agregue CivicsOR a su pantalla de inicio y se abrirá como una aplicación, incluso sin señal. En iPhone, toque Compartir y luego <strong>Agregar a pantalla de inicio</strong>. En Android, toque el menú y luego <strong>Instalar aplicación</strong> o <strong>Agregar a la pantalla principal</strong>.</p>
    </div>
    <div class="card">
      <h2>Dos zonas horarias</h2>
      <p>Cada reunión aparece en su hora local: hora del Pacífico para casi todo Oregon, hora de la Montaña para la mayor parte del condado de Malheur.</p>
    </div>
    <div class="card">
      <h2>La Legislatura, día a día</h2>
      <p>Las audiencias de los comités, con sus agendas, y cómo inscribirse para testificar en persona o a distancia. La sesión larga de 2027 empieza en enero.</p>
      <a class="link" href="../legislature.html" hreflang="en">Vea lo que viene en el Capitolio (en inglés)</a>
    </div>
    <div class="card warm">
      <span class="eyebrow">Participe</span>
      <h2>¿Primera vez en una reunión pública?</h2>
      <p>Lo que la ley de Oregon le permite, qué decir en dos minutos y qué pasa después de hablar.</p>
      <a class="link" href="guides/speak-at-a-public-meeting.html">Leer la guía</a>
    </div>
  </aside>
</div>

{footer_es("../", 'Las reuniones vienen directamente de los calendarios públicos de cada agencia y se actualizan cada noche. <span id="updated"></span> Los horarios cambian, así que confirme con la entidad antes de ir.')}

<script src="../app.js"></script>
</body>
</html>
''')

(ES / "reps.html").write_text(f'''{head("Quién le representa | CivicsOR", "../", "Escriba una dirección de Oregon para ver todos sus distritos, sus legisladores estatales y miembros del Congreso, y dónde encontrar a su ciudad y su condado.", lang="es", scripts=REPS_SCRIPTS)}
<a class="skip" href="#results">Ir a los resultados</a>
{top("", "reps", lang="es", alt="../reps.html")}

<section class="hero"><div class="wrap">
  <h1>Encuentre quién le representa.</h1>
  <p class="lede">Escriba una dirección de Oregon para ver todos los distritos donde vive, desde el Congreso hasta su distrito de bomberos, además de su senador o senadora estatal, su representante estatal y sus miembros del Congreso, y cómo comunicarse con ellos.</p>
  <form class="search" id="lookup">
    <div class="field wide">
      <label for="address">Dirección</label>
      <input id="address" name="address" type="text" autocomplete="street-address" placeholder="900 Court St NE, Salem">
    </div>
    <button class="btn" type="submit">Buscar</button>
  </form>
  <p class="small">Su navegador envía la dirección al servicio de búsqueda de direcciones de la Oficina del Censo de EE. UU. para encontrar sus distritos. Solo el punto en el mapa que devuelve, no su dirección, va a los mapas públicos del estado para encontrar sus distritos de bomberos, de educación y de conservación, y, para las direcciones de Portland y del condado de Multnomah, a los mapas de distritos de la Ciudad y del Condado. CivicsOR nunca recibe ni guarda ninguno de los dos. Su navegador recuerda solo su condado y su ciudad, para que las guías puedan mostrar enlaces locales.</p>
</div></section>

<main class="wrap narrow" style="padding-block: 40px 64px">
  <p class="term-note" id="term-note" hidden></p>
  <div class="list" id="results" aria-live="polite">
    <p class="empty">Sus representantes aparecerán aquí.</p>
  </div>
  <p class="muted" style="margin-top: 24px">¿No sabe qué decir cuando ya tiene un nombre? Lea <a href="guides/contact-your-representatives.html">cómo comunicarse con quienes le representan</a>.</p>
</main>

{footer_es("../", "Los legisladores estatales vienen de Open States, una lista pública basada en las páginas de miembros de la Legislatura de Oregon, y los miembros del Congreso de una lista pública. Ambas se actualizan cada noche. Los enlaces de condados cubren los 36 condados, y los de ciudades cubren los sitios web oficiales de 226 ciudades, según el Oregon Blue Book. Los sitios enlazados están en inglés.")}

<script src="../local.js"></script>
<script src="../districts.js"></script>
<script src="../reps.js"></script>
</body>
</html>
''')

ABOUT_ES = """
<h2>Quién lo administra</h2>
<p>CivicsOR es un servicio de BarNone, Inc., una organización independiente sin fines de lucro. No es un sitio de gobierno. No está afiliado a ninguna agencia de gobierno y no habla en nombre de ningún cargo público. No toma partido sobre candidatos, partidos, proyectos de ley ni medidas en la boleta.</p>

<h2>De dónde vienen las reuniones</h2>
<p>Cada reunión viene del calendario que publica la propia entidad pública: los portales de reuniones de ciudades y condados, los calendarios de los distritos escolares, los programas de las bibliotecas, gobiernos regionales como Metro y el calendario de comités de la Legislatura de Oregon. Cada noche, CivicsOR lee esos calendarios y actualiza el sitio. Cada reunión tiene un enlace a la página de la entidad.</p>
<p>Algunas entidades publican un calendario fijo ("el segundo y el cuarto martes a las 10 a. m.") en lugar de un calendario de reuniones. Esas reuniones se marcan como <strong>Reunión habitual</strong>, porque se pueden cancelar o mover sin que nos llegue el cambio, así que confirme antes de ir. Cuando un calendario fijo cae en un día feriado del estado, no mostramos esa fecha.</p>

<h2>Qué tan actualizado está</h2>
<p>Las reuniones se actualizan cada noche. Si no podemos abrir un calendario, seguimos mostrando lo que tenía la última vez y lo seguimos intentando. La <a href="../coverage.html" hreflang="en">página de cobertura (en inglés)</a> muestra cada calendario que leemos y cuándo lo leímos bien por última vez.</p>
<p><strong>Siempre confirme con la entidad antes de ir.</strong> Las agendas, los horarios y las salas cambian, a veces el mismo día. Los nombres de las reuniones y las agendas vienen de cada entidad y están en inglés.</p>

<h2>Lo que todavía no está aquí</h2>
<p>Algunas entidades públicas solo publican archivos PDF, o no publican ningún calendario en línea. CivicsOR lee los avisos de reuniones públicas una vez por noche con un lector que se identifica, y hace pocas solicitudes. Donde no se puede leer un calendario, el sitio tiene un enlace a la página de reuniones de esa entidad. La <a href="../coverage.html" hreflang="en">página de cobertura (en inglés)</a> muestra lo que se incluye, condado por condado.</p>

<h2>Sobre esta traducción</h2>
<p>En español están el calendario, la búsqueda de representantes, esta página, la página de privacidad y cinco guías: <a href="guides/contact-your-representatives.html">cómo comunicarse con quienes le representan</a>, <a href="guides/voting-in-oregon.html">votar en Oregon</a>, <a href="guides/speak-at-a-public-meeting.html">cómo hablar en una reunión pública</a>, <a href="guides/public-records-requests.html">cómo pedir registros públicos</a> y <a href="guides/your-school-board.html">su junta escolar</a>. Las demás guías y las páginas de la Legislatura y de cobertura todavía están en inglés.</p>

<h2>¿Encontró un error o falta una reunión?</h2>
<p><a class="link" href="mailto:{REPORT}?subject=CivicsOR%3A%20correcci%C3%B3n">Reportar una corrección</a></p>
<p class="muted">Escriba a <a href="mailto:{REPORT}">{REPORT}</a>. Díganos qué está mal y dónde, e incluya un enlace a la información correcta si lo tiene. Puede escribir en español.</p>

<h2 id="privacidad">Privacidad</h2>
<p>CivicsOR no tiene cuentas, anuncios ni cookies, y no vende ni comparte información sobre quienes lo visitan. El condado que usted elige se guarda solo en su propio navegador. <a href="privacy.html">Lea la página de privacidad</a>.</p>

<h2 id="accesibilidad">Accesibilidad</h2>
<p>Buscamos cumplir con las Pautas de Accesibilidad para el Contenido Web (WCAG) 2.1, nivel AA. Las páginas funcionan con teclado y con lectores de pantalla, el texto cumple con los estándares de contraste y el sitio funciona en teléfonos. Si algo le impide usar el sitio, por favor <a href="mailto:{REPORT}?subject=CivicsOR%3A%20accesibilidad">díganoslo</a> y lo corregiremos.</p>
"""
(ES / "about.html").write_text(f'''{head("Acerca de CivicsOR | CivicsOR", "../", "Quién administra CivicsOR, de dónde vienen las reuniones, qué tan actualizadas están y cómo reportar un error.", lang="es")}
<a class="skip" href="#about">Ir al contenido</a>
{top("", "", lang="es", alt="../about.html")}

<section class="hero"><div class="wrap">
  <p class="eyebrow light">Acerca de</p>
  <h1>Acerca de CivicsOR</h1>
  <p class="lede">Un solo lugar para ver lo que deciden las entidades públicas de Oregon y cómo participar.</p>
</div></section>

<main class="wrap guide-body" id="about" style="padding-block: 32px 64px; display: flex; flex-direction: column; gap: 16px; max-width: 760px">
{ABOUT_ES.strip(chr(10)).format(REPORT=REPORT)}
</main>

{footer_es("../", "CivicsOR lee calendarios públicos cada noche y enlaza cada reunión con la página de su entidad.")}
</body>
</html>
''')

PRIV_ES = """
  <h2>En resumen</h2>
  <p>CivicsOR no tiene cuentas, anuncios, cookies, rastreo ni analítica. No recopilamos su nombre, su correo electrónico ni su dirección.</p>
  <h2>Lo que se queda en su dispositivo</h2>
  <ul>
    <li><strong>Su condado y su ciudad.</strong> Cuando los elige, su navegador los recuerda para que el calendario abra allí la próxima vez. Esa elección se guarda solo en su navegador. Si borra los datos de su navegador, se borra.</li>
    <li><strong>La aplicación.</strong> Si agrega CivicsOR a su pantalla de inicio, su dispositivo guarda una copia de las páginas y del calendario más reciente para que funcione sin señal.</li>
  </ul>
  <h2>Lo que sale de su dispositivo</h2>
  <ul>
    <li><strong>Búsqueda por dirección.</strong> Cuando busca a sus representantes, su navegador envía la dirección directamente al servicio público de búsqueda de direcciones (geocoder) de la Oficina del Censo de EE. UU. para encontrar sus distritos. Después, su navegador envía solo el punto en el mapa que devuelve la Oficina del Censo, no la dirección, a los servicios públicos de mapas de la Oficina del Jefe de Bomberos del Estado de Oregon (Oregon State Fire Marshal), de las agencias de educación del estado y del Departamento de Agricultura de Oregon, para encontrar los distritos de bomberos, de educación y de conservación. Si la dirección está en Portland o en el condado de Multnomah, el punto también va a los mapas públicos de la Ciudad de Portland y del Condado de Multnomah, para encontrar sus distritos del concejo municipal y de comisionados del condado. Ni la dirección ni el punto pasan por nosotros, y nunca los vemos ni los guardamos.</li>
    <li><strong>Alojamiento.</strong> El sitio está alojado en GitHub Pages. Como cualquier servidor web, GitHub guarda registros estándar del servidor, como las direcciones IP, por seguridad. Nosotros no recibimos ni usamos esos registros.</li>
    <li><strong>Enlaces que usted abre.</strong> Los detalles de las reuniones, las agendas y las fuentes de las guías se abren en sitios de gobierno y otros sitios, que tienen sus propias políticas de privacidad.</li>
    <li><strong>Reportes de problemas.</strong> Si nos envía una corrección por correo electrónico, llega a la bandeja de entrada de BarNone ({REPORT}). Solo la usamos para corregir el sitio.</li>
  </ul>
  <p class="muted">Actualizado en noviembre de 2026. Preguntas: {REPORT}. Puede escribir en español.</p>
"""
(ES / "privacy.html").write_text(f'''{head("Privacidad | CivicsOR", "../", "CivicsOR no tiene cuentas, anuncios, cookies ni rastreo. Lo que se queda en su dispositivo y lo que sale de él.", lang="es")}
<a class="skip" href="#privacy">Ir al contenido</a>
{top("", "", lang="es", alt="../privacy.html")}
<main class="wrap narrow guide" id="privacy">
  <h1>Privacidad</h1>
{PRIV_ES.format(REPORT=REPORT)}
</main>
{footer_es("../", "CivicsOR es gratis y no le pide nada.")}
</body>
</html>
''')
print("Spanish pages written:", len(guides_or_es.G) + 5)


# The page GitHub Pages shows for an address that doesn't exist. It can be
# served from any path, so its links are absolute, and search engines skip it.
(SITE / "404.html").write_text(f'''{head("Page not found | CivicsOR", "/", "That page isn't here. Find your meetings, guides and representatives from the CivicsOR home page.").replace("<title>", '<meta name="robots" content="noindex">\n<title>', 1)}
<a class="skip" href="#notfound">Skip to content</a>
{top("/", "", alt="/es/index.html")}
<main class="wrap narrow guide" id="notfound">
  <h1>We can't find that page.</h1>
  <p class="lede">The address may be mistyped, or the page may have moved.</p>
  <ul>
    <li><a href="/index.html">Community Calendar</a>: what your city, county and the Legislature are deciding.</li>
    <li><a href="/legislature.html">The Legislature, day by day</a></li>
    <li><a href="/engage.html">Engage guides</a>: how to take part.</li>
    <li><a href="/reps.html">Find who represents you</a></li>
  </ul>
  <p lang="es">¿Busca la versión en español? Vaya al <a href="/es/index.html" hreflang="es">calendario en español</a>.</p>
  <p>Followed a link from this site to get here? <a href="mailto:{REPORT}?subject=CivicsOR%3A%20broken%20link">Tell us</a> and we'll fix it.</p>
</main>
{footer("/", "CivicsOR is free to use and asks nothing of you.")}
</body>
</html>
''')
print("404 page written")


# Every page's intro band is a named region, so screen reader users can jump
# to it and nothing on the page sits outside a landmark.
for page in SITE.rglob("*.html"):
    text = page.read_text()
    label = "Introducción" if '<html lang="es">' in text else "Introduction"
    fixed = re.sub(r'<section class="hero', f'<section aria-label="{label}" class="hero', text)
    if fixed != text:
        page.write_text(fixed)


# Search engines: each page names its one true address (canonical), points to
# its translation (hreflang), and the home pages say who runs the site. Then a
# sitemap lists every page, and robots.txt points to it.
def page_url(rel):
    rel = rel.replace("\\", "/")
    if rel == "index.html":
        return SITE_URL
    if rel.endswith("/index.html"):
        return SITE_URL + rel[: -len("index.html")]
    return SITE_URL + rel


def twin(rel):
    """The same page in the other language, or None if it isn't translated."""
    other = rel[3:] if rel.startswith("es/") else "es/" + rel
    return other if (SITE / other).exists() else None


ORG = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "WebSite", "@id": SITE_URL + "#site", "name": "CivicsOR", "url": SITE_URL,
         "inLanguage": ["en", "es"], "publisher": {"@id": "https://barnoneinc.org/#org"},
         "description": "A free calendar of what Oregon's city councils, county boards, Metro and the Legislature are deciding, with plain-language guides to taking part."},
        {"@type": "NGO", "@id": "https://barnoneinc.org/#org", "name": "BarNone", "url": "https://barnoneinc.org",
         "logo": SITE_URL + "barnone-phoenix.png"},
    ],
}

ORG_DESC_ES = ("Un calendario gratuito de lo que deciden los concejos municipales, las juntas de condado, Metro y la Legislatura "
               "de Oregon, con guías en lenguaje sencillo para participar.")

pages = sorted(p.relative_to(SITE).as_posix() for p in SITE.rglob("*.html") if p.name != "404.html")
MARK = "<!-- seo -->"
for rel in pages:
    page = SITE / rel
    text = re.sub(re.escape(MARK) + r".*?" + re.escape(MARK) + "\n", "", page.read_text(), flags=re.S)
    tags = [f'<link rel="canonical" href="{page_url(rel)}">',
            f'<meta property="og:url" content="{page_url(rel)}">']
    other = twin(rel)
    if other:
        en, es = (other, rel) if rel.startswith("es/") else (rel, other)
        tags += [f'<link rel="alternate" hreflang="en" href="{page_url(en)}">',
                 f'<link rel="alternate" hreflang="es" href="{page_url(es)}">',
                 f'<link rel="alternate" hreflang="x-default" href="{page_url(en)}">']
    if rel in ("index.html", "es/index.html"):
        org = ORG if rel == "index.html" else {**ORG, "@graph": [{**ORG["@graph"][0], "description": ORG_DESC_ES}, ORG["@graph"][1]]}
        tags.append('<script type="application/ld+json">' + json.dumps(org, ensure_ascii=False).replace("</", "<\\/") + "</script>")
    block = MARK + "\n" + "\n".join(tags) + "\n" + MARK + "\n"
    page.write_text(text.replace("</head>", block + "</head>", 1))

entries = []
for rel in pages:
    links = ""
    other = twin(rel)
    if other:
        en, es = (other, rel) if rel.startswith("es/") else (rel, other)
        links = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{page_url(r)}"/>'
                        for l, r in (("en", en), ("es", es), ("x-default", en)))
    entries.append(f"  <url>\n    <loc>{page_url(rel)}</loc>{links}\n  </url>")
(SITE / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    + "\n".join(entries) + "\n</urlset>\n")
(SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n")
print(f"search pieces written: {len(pages)} pages in the sitemap")
