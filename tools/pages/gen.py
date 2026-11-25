"""Generator for CivicsOR's static pages (guides, Engage, reps, calendar shell).
Run: python3 tools/pages/gen.py  -- writes plain HTML into site/.
English only for now; Spanish pages come in a later pass (CivicsID's
tools/pages/gen.py has the Spanish set-up to copy)."""
import html, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import guides_or
import guides_or2  # noqa: E402

SITE = Path(__file__).resolve().parents[2] / "site"
# The reps page also loads three state district maps (JSONP).
REPS_SCRIPTS = " https://services.arcgis.com https://maps.oda.oregon.gov"
FONTS = ('<link rel="preload" href="{up}fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>\n'
         '<link rel="preload" href="{up}fonts/source-serif-4-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>')
SITE_URL = "https://civicsor.org/"
REPORT = "admin@barnoneinc.org"
NOTICE = '<aside class="notice" aria-label="About CivicsOR">A project of BarNone, a nonprofit. Not affiliated with any government agency.</aside>'
BY = ('<p class="by-barnone"><a href="https://barnoneinc.org"><img src="{up}barnone-phoenix.png" alt="" width="28" height="28">'
      '<span>A service of <strong>BarNone, Inc.</strong></span></a> An independent nonprofit. CivicsOR is not a government website, '
      'is not affiliated with any government agency, and does not speak for any public office.</p>')


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
<meta property="og:image" content="{SITE_URL}{"share-es.png" if lang == "es" else "share.png"}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="CivicsOR: Get Engaged, Oregon.">
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
       "es": ("Calendario comunitario", "Calendario", "Participa", "Mis representantes", "Mis reps", "Principal", "Legislatura")}


def top(up, current, lang="en", alt=None, reps_up=None):
    """alt: link to this page in the other language. Spanish pages link to the
    English representatives lookup (reps_up), which isn't translated yet."""
    cal, cal_s, eng, reps, reps_s, main, leg = NAV[lang]
    notice = NOTICE if lang == "en" else '<aside class="notice" aria-label="Acerca de CivicsOR">Un proyecto de BarNone, una organización sin fines de lucro. No está afiliado a ninguna agencia de gobierno.</aside>'
    switch = (f'\n  <a class="lang-switch" href="{alt}" lang="{"es" if lang == "en" else "en"}" hreflang="{"es" if lang == "en" else "en"}">{"Español" if lang == "en" else "English"}</a>' if alt else "")
    def a(href, label, key, short=None):
        cur = ' aria-current="page"' if key == current else ""
        if short:  # a shorter label on phones; the full name stays for screen readers
            return f'    <a href="{up}{href}"{cur} aria-label="{label}"><span class="full">{label}</span><span class="short">{short}</span></a>'
        return f'    <a href="{up}{href}"{cur}>{label}</a>'
    reps_href = (reps_up or up) + "reps.html"
    reps_link = a("reps.html", reps, "reps", reps_s).replace(f'href="{up}reps.html"', f'href="{reps_href}"')
    return f'''{notice}

<header class="top"><div class="wrap">
  <a class="brand" href="{up}index.html">Civics<span>OR</span></a>{switch}
  <nav aria-label="{main}">
{a("index.html", cal, "calendar", cal_s)}
{a("legislature.html", leg, "legislature")}
{a("engage.html", eng, "engage")}
{reps_link}
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
{top("../", "engage")}

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
{top("", "engage")}

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
{top("", "calendar")}

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
{top("", "reps")}

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
  <p class="small">Your address is sent from your browser to the U.S. Census Bureau's address lookup to find your districts. Only the map point it returns, not your address, goes to public state maps to find your fire, education and conservation districts. CivicsOR never receives or stores either. Your browser remembers only your county and city, so the Engage guides can show local links.</p>
</div></section>

<main class="wrap narrow" style="padding-block: 40px 64px">
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
{top("", "")}

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
<p>Some public bodies only post PDFs, or don't post a calendar online at all. Some websites block automated readers, and we respect that, including systems such as BoardDocs that ask automated readers to stay out. For those places, the site links to their own meeting pages instead. The <a href="coverage.html">coverage page</a> lists what's included county by county. Spanish pages are planned.</p>

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
    <li><strong>Address lookups.</strong> When you look up your representatives, your browser sends the address straight to the U.S. Census Bureau's public geocoder to find your districts. Your browser then sends only the map point the Census Bureau returns, not the address, to public map services run by the Oregon State Fire Marshal, the state's education agencies and the Oregon Department of Agriculture to find fire, education and conservation districts. Neither passes through us, and we never see or store them.</li>
    <li><strong>Hosting.</strong> The site is hosted on GitHub Pages. Like any web host, GitHub keeps standard server logs, such as IP addresses, for security. We don't get or use those logs.</li>
    <li><strong>Links you follow.</strong> Meeting details, agendas and guide sources open on government and other websites, which have their own privacy policies.</li>
    <li><strong>Problem reports.</strong> If you email us a correction, it goes to BarNone's inbox ({REPORT}). We use it only to fix the site.</li>
  </ul>
  <p class="muted">Updated November 2026. Questions: {REPORT}.</p>
"""
(SITE / "privacy.html").write_text(f'''{head("Privacy | CivicsOR", "", "CivicsOR has no accounts, no ads, no cookies and no tracking.")}
<a class="skip" href="#privacy">Skip to content</a>
{top("", "")}
<main class="wrap narrow guide" id="privacy">
  <h1>Privacy</h1>
{PRIV_EN.format(REPORT=REPORT)}
</main>
{footer("", "CivicsOR is free to use and asks nothing of you.")}
</body>
</html>
''')
print("privacy pages written")


# The page GitHub Pages shows for an address that doesn't exist. It can be
# served from any path, so its links are absolute, and search engines skip it.
(SITE / "404.html").write_text(f'''{head("Page not found | CivicsOR", "/", "That page isn't here. Find your meetings, guides and representatives from the CivicsOR home page.").replace("<title>", '<meta name="robots" content="noindex">\n<title>', 1)}
<a class="skip" href="#notfound">Skip to content</a>
{top("/", "")}
<main class="wrap narrow guide" id="notfound">
  <h1>We can't find that page.</h1>
  <p class="lede">The address may be mistyped, or the page may have moved.</p>
  <ul>
    <li><a href="/index.html">Community Calendar</a>: what your city, county and the Legislature are deciding.</li>
    <li><a href="/legislature.html">The Legislature, day by day</a></li>
    <li><a href="/engage.html">Engage guides</a>: how to take part.</li>
    <li><a href="/reps.html">Find who represents you</a></li>
  </ul>
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
         "inLanguage": ["en"], "publisher": {"@id": "https://barnoneinc.org/#org"},
         "description": "A free calendar of what Oregon's city councils, county boards, Metro and the Legislature are deciding, with plain-language guides to taking part."},
        {"@type": "NGO", "@id": "https://barnoneinc.org/#org", "name": "BarNone", "url": "https://barnoneinc.org",
         "logo": SITE_URL + "barnone-phoenix.png"},
    ],
}

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
        tags.append('<script type="application/ld+json">' + json.dumps(ORG).replace("</", "<\\/") + "</script>")
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
