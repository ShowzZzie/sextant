import datetime
import json
import pathlib

import pytest

from sextant.adapters.greenhouse import parse
from sextant.models import NormalizedRecord, WorkType

SEEN_AT = datetime.datetime(2026, 11, 1, 12, 0, tzinfo=datetime.UTC)

WORK_TYPE_DATA = [
    ("4461450008", WorkType.ONSITE),
    ("5452922008", WorkType.REMOTE),
    ("4423394008", WorkType.HYBRID),
    ("5079916008", None),
    ("5382033008", None),
]


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


@pytest.mark.parametrize("gh_id, expected_work_type", WORK_TYPE_DATA)
def test_work_type(
    load_greenhouse: list[NormalizedRecord],
    gh_id: str,
    expected_work_type: WorkType | None,
) -> None:
    recs = load_greenhouse
    rec = next(rec for rec in recs if rec.external_id == gh_id)
    assert rec.work_type == expected_work_type


def test_description(load_greenhouse: list[NormalizedRecord]) -> None:
    recs = load_greenhouse
    for rec in recs:
        assert "<" not in rec.description
        assert ">" not in rec.description
        assert "&lt;" not in rec.description
        assert "&amp;" not in rec.description
    assert "Response & Policy" in next(
        rec.description for rec in recs if rec.external_id == "5382033008"
    )
