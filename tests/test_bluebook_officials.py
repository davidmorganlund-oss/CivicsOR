import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pipeline"))
from bluebook_officials import parse_body  # noqa: E402


def names(paragraph):
    body, members = parse_body(paragraph)
    return body, [(m["title"], m["name"], m["term_ends"]) for m in members]


def test_board_with_chair_stops_at_officers():
    assert names("Commissioners: Chair Jennifer Euwer (2029); Arthur Babitz (2029), Ed Weathers (2027); "
                 "Dist. Atty. Matthew Ellis (2029); Sheriff Matt English (2029); Assess./Clerk Brian Beebe") == (
        "Board of Commissioners",
        [("Chair", "Jennifer Euwer", "2029"), (None, "Arthur Babitz", "2029"), (None, "Ed Weathers", "2027")])


def test_county_court():
    assert names("County Court: Judge Jim Hamsher (2029); John A Rowell (2027), Mitchel Wilson (2029); Assess. X (2027)") == (
        "County Court",
        [("Judge", "Jim Hamsher", "2029"), (None, "John A Rowell", "2027"), (None, "Mitchel Wilson", "2029")])


def test_odd_punctuation_and_nicknames():
    _, m = names("Commissioners: Chair Anthony DeBone (2027); Patti Adair, (2027); Phil Chang (2029); Dist. Atty. Steve Gunnels (2027)")
    assert [x[1] for x in m] == ["Anthony DeBone", "Patti Adair", "Phil Chang"]
    _, m = names("Commissioners: Kit Johnston (2027), David (Bubba) King (2029), Mary Starrett (2027); Dist. Atty. Kate Lynch (2029)")
    assert [x[1] for x in m] == ["Kit Johnston", "David (Bubba) King", "Mary Starrett"]


def test_officer_in_same_segment_is_not_a_commissioner():
    _, m = names("Commissioners: Ron Smith (2029), Dist. Atty. Joshua J. Eastman (2029); Assess. Chris Parton (2029)")
    assert [x[1] for x in m] == ["Ron Smith"]
