import datetime
import html
from typing import Any

from bs4 import BeautifulSoup

from sextant.models import NormalizedRecord, SalarySource, SourceAPI, WorkType

WORK_TYPE_MAP: dict[str, WorkType] = {
    "On-Site": WorkType.ONSITE,
    "Remote": WorkType.REMOTE,
    "Hybrid (Travel-Required)": WorkType.HYBRID,
}


def fetch(token: str) -> dict[str, Any]:
    """Retrieve the JSON file from the internet"""
    raise NotImplementedError


def parse(
    raw_json: dict[str, Any], company_name: str, seen_at: datetime.datetime
) -> list[NormalizedRecord]:
    """Take a raw JSON and convert to a list of NormalizedRecords"""

    jobs: list[dict[str, Any]] = raw_json["jobs"]
    final_list: list[NormalizedRecord] = []

    for job in jobs:
        plain_worktype_key: str | None = None
        for entry in job.get("metadata") or []:
            if entry["name"] == "Location Type":
                plain_worktype_key = entry["value"]

        soup = BeautifulSoup(html.unescape(job["content"]), "html.parser")

        record = NormalizedRecord(
            source=SourceAPI.GREENHOUSE,
            external_id=str(job["id"]),
            company=company_name,
            job_title=job["title"],
            job_url=job["absolute_url"],
            departments=[dep["name"] for dep in job["departments"]],
            locations=[off["name"] for off in job["offices"]],
            work_type=WORK_TYPE_MAP.get(plain_worktype_key)
            if plain_worktype_key is not None
            else None,
            published_at=datetime.datetime.fromisoformat(
                job["first_published"]
            ).astimezone(datetime.UTC),
            description=soup.get_text("\n", strip=True),
            salary_source=SalarySource.NONE,
            first_seen=seen_at,  # will need logic, checking against existing logic. Right now we just make new records every time
            last_seen=seen_at,
        )
        final_list.append(record)

    return final_list
