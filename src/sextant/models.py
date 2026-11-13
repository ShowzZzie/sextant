import datetime
from enum import StrEnum

import sqlmodel


class SourceAPI(StrEnum):
    ASHBY = "ashby"
    GREENHOUSE = "greenhouse"
    LEVER = "lever"


class SalarySource(StrEnum):
    API = "api"
    EXTRACTED = "extracted"
    NONE = "none"


class WorkType(StrEnum):
    ONSITE = "onsite"
    REMOTE = "remote"
    HYBRID = "hybrid"


class EmploymentType(StrEnum):
    FULLTIME = "fulltime"
    PARTTIME = "parttime"
    INTERNSHIP = "internship"
    OTHER = "other"


class SalaryPeriod(StrEnum):
    HOURLY = "hourly"
    DAILY = "daily"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    OTHER = "other"


# All datetimes are timezone-aware UTC; adapters convert before building a record.
class NormalizedRecord(sqlmodel.SQLModel):
    source: SourceAPI
    external_id: str
    company: str
    job_title: str
    job_url: str
    department: str | None = sqlmodel.Field(
        default=None
    )  # keeping it in case API doesn't have this, or employer doesn't list it
    location: list[str] = sqlmodel.Field(default_factory=list)
    work_type: WorkType | None = sqlmodel.Field(
        default=None
    )  # Greenhouse doesn't provide this, needs to be optional
    employment_type: EmploymentType | None = sqlmodel.Field(default=None)
    published_at: datetime.datetime
    description: str
    salary_min: float | None = sqlmodel.Field(default=None)
    salary_max: float | None = sqlmodel.Field(default=None)
    salary_currency: str | None = sqlmodel.Field(default=None)
    salary_period: SalaryPeriod | None = sqlmodel.Field(default=None)
    salary_source: SalarySource = sqlmodel.Field(default=SalarySource.NONE)
    first_seen: datetime.datetime
    last_seen: datetime.datetime
    closed_at: datetime.datetime | None = sqlmodel.Field(default=None)
