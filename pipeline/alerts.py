"""Open (or update, or close) one GitHub issue listing calendar sources that
have failed for three days or more, or have answered with no meetings for
seven days or more. GitHub emails the repository owner when the issue opens,
so a broken or silent city calendar doesn't go unnoticed.

Runs after build.py in the nightly workflow; needs the gh CLI and GH_TOKEN.
"""
import json
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

TITLE = "Calendar sources need attention"
UPKEEP_TITLE = "Hand-entered schedules need new dates"
ROOT = Path(__file__).resolve().parent.parent
STATUS = ROOT / "site" / "data" / "status.json"
SOURCES = ROOT / "pipeline" / "sources.yml"
DAYS = 3
QUIET_DAYS = 7  # a feed that answers but lists no meetings this long gets a look
AHEAD = 21  # warn this many days before a hand-entered date list runs out


def gh(*args):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def stuck_sources(status, today):
    cutoff = (today - timedelta(days=DAYS - 1)).isoformat()
    return [s for s in status["sources"]
            if s.get("state") == "failing" and s.get("failing_since") and s["failing_since"] <= cutoff]


def quiet_sources(status, today, cfg=None):
    """Feeds that answer but have listed no meetings for QUIET_DAYS or more.
    Hand-entered schedules are left out: when their dates run out, the
    upkeep issue already says so, and a board that skips a month is not news."""
    cutoff = (today - timedelta(days=QUIET_DAYS - 1)).isoformat()
    kinds = {s["id"]: s.get("type") for s in (cfg or {}).get("sources", [])}
    return [s for s in status["sources"]
            if s.get("state") == "quiet" and s.get("quiet_since") and s["quiet_since"] <= cutoff
            and kinds.get(s["id"]) != "schedule"]


def body(stuck, silent=()):
    lines = []
    if stuck:
        lines += ["These calendars have not answered for three days or more. CivicsOR keeps showing the "
                  "last meetings it read from them, so their listings are going stale.", ""]
        for s in stuck:
            lines.append(f"- **{s['name']}** ({s.get('county', '')} County), failing since {s['failing_since']}. "
                         f"Last good read: {s.get('last_success') or 'never'}. Error: `{s.get('error', '')[:200]}`")
        lines += ["", "If a site now refuses automated readers, remove it from `pipeline/sources.yml` "
                  "rather than working around the block."]
    if silent:
        if lines:
            lines.append("")
        lines += [f"These calendars answer but have listed no meetings for {QUIET_DAYS} days or more. Some are "
                  "seasonal (boards that post a week ahead, or skip summer or December); others may have "
                  "moved to a new page or platform.", ""]
        for s in silent:
            lines.append(f"- **{s['name']}** ({s.get('county', '')} County), quiet since {s['quiet_since']}. "
                         f"Check {s.get('homepage') or 'its website'}.")
        lines += ["", "For a board that publishes its year's dates, add them as a `regular_schedule` in "
                  "`pipeline/sources.yml`."]
    lines += ["", "This issue closes itself when every source answers and lists meetings again."]
    return "\n".join(lines)


def upkeep_items(cfg, today):
    """Hand-entered schedules whose list of dates runs out soon, and sources
    with a 'review_by' date (a planned change, like a portal move) that is due."""
    horizon = today + timedelta(days=AHEAD)
    items = []
    for src in cfg["sources"]:
        review = src.get("review_by")
        if review and date.fromisoformat(str(review)) <= horizon:
            items.append(f"- **{src['name']}** (`{src['id']}`): {src.get('review_note', 'planned change due')} (by {review}).")
        ruled = {m["title"] for m in src.get("meetings", []) if m.get("when")}
        for mtg in src.get("meetings", []):
            if mtg.get("one_off"):
                continue  # a single special meeting, not a series that needs more dates
            if mtg.get("dates") and mtg["title"] in ruled:
                continue  # the dates bridge a gap; a regular rule for the same meeting takes over
            last = max([date.fromisoformat(str(d)) for d in mtg.get("dates", [])], default=None)
            until = mtg.get("until") and date.fromisoformat(str(mtg["until"]))
            end = last if (last and not mtg.get("when")) else until
            if end and end <= horizon:
                when = "ran out" if end < today else "runs out"
                items.append(f"- **{src['name']}**, {mtg['title']} (`{src['id']}`): listed dates {when} {end}. "
                             f"Add the next dates from {mtg.get('url') or src.get('homepage', '')}.")
    return items


def quiet(text):
    """Meeting names come from outside sites; keep a stray "@name" in one
    from pinging a real GitHub user."""
    return re.sub(r"@(?=[A-Za-z0-9])", "@\u2060", text)


def sync_issue(title, lines, closing):
    lines = [quiet(line) for line in lines]
    found = json.loads(gh("issue", "list", "--state", "open", "--search", f'"{title}" in:title',
                          "--json", "number,title"))
    issue = next((i["number"] for i in found if i["title"] == title), None)
    if lines and issue is None:
        gh("issue", "create", "--title", title, "--body", "\n".join(lines))
        print(f"opened: {title}")
    elif lines:
        gh("issue", "edit", str(issue), "--body", "\n".join(lines))
        print(f"updated #{issue}: {title}")
    elif issue is not None:
        gh("issue", "close", str(issue), "--comment", closing)
        print(f"closed #{issue}")


def main():
    import yaml
    cfg = yaml.safe_load(SOURCES.read_text())
    items = upkeep_items(cfg, date.today())
    roster = ROOT / "site" / "data" / "county_officials.json"
    if roster.exists():
        meta = json.loads(roster.read_text())
        if meta.get("review_by") and date.fromisoformat(meta["review_by"]) <= date.today() + timedelta(days=AHEAD):
            items.append(f"- **County officials roster** (`site/data/county_officials.json`): {meta.get('review_note', '')} (by {meta['review_by']}).")
    sync_issue(UPKEEP_TITLE, (["These hand-entered schedules or planned changes need a human look in the next "
                               f"{AHEAD} days. Once their meetings pass, the calendar quietly goes empty for them.", ""]
                              + items) if items else [], "Every hand-entered schedule has dates for the next three weeks.")
    import checks
    found = checks.report()
    sync_issue("Data or link problems to look at", (["The nightly checks found these. Listings that look wrong may be a parsing or time zone "
                                                   "problem; broken links are pages that moved (checked Mondays).", ""] + found) if found else [],
               "Tonight's data and link checks came back clean.")
    status = json.loads(STATUS.read_text())
    stuck = stuck_sources(status, date.today())
    silent = quiet_sources(status, date.today(), cfg)
    print(f"{len(stuck)} source(s) failing {DAYS}+ days, {len(silent)} quiet {QUIET_DAYS}+ days")
    # One issue for both, opened, updated or closed to match tonight's run.
    sync_issue(TITLE, body(stuck, silent).split("\n") if (stuck or silent) else [],
               "Every calendar source is answering and listing meetings again.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
