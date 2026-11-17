import datetime
import json
import pathlib

import pytest

from sextant.adapters.greenhouse import parse
from sextant.models import NormalizedRecord

SEEN_AT = datetime.datetime(2026, 11, 1, 12, 0, tzinfo=datetime.UTC)


@pytest.fixture
def load_greenhouse() -> list[NormalizedRecord]:
    tests_dir = pathlib.Path(__file__).resolve().parent

    with open(tests_dir / "fixtures" / "greenhouse_board.json", "r") as file:
        data = json.load(file)
        return parse(data, "test_Anthropic", SEEN_AT)


def test_parses_all_jobs(load_greenhouse: list[NormalizedRecord]) -> None:
    recs = load_greenhouse
    assert len(recs) == 5


def test_run_fields(load_greenhouse: list[NormalizedRecord]) -> None:
    recs = load_greenhouse
    assert all(isinstance(rec, NormalizedRecord) for rec in recs)
    assert all(rec.company == "test_Anthropic" for rec in recs)
    assert all(rec.first_seen == SEEN_AT for rec in recs)
    assert all(rec.last_seen == SEEN_AT for rec in recs)
    assert all(isinstance(rec.external_id, str) for rec in recs)


def test_published_at_is_utc(load_greenhouse: list[NormalizedRecord]) -> None:
    recs = load_greenhouse
    test_listing = next(rec for rec in recs if rec.external_id == "4461450008")
    assert test_listing.published_at == datetime.datetime(
        2024, 12, 20, 18, 53, 38, tzinfo=datetime.UTC
    )
