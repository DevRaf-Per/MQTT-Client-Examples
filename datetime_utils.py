from __future__ import annotations

from datetime import UTC, datetime


def now_local() -> datetime:
    """Return the current local time as a naive datetime object."""
    return datetime.now(UTC).astimezone().replace(tzinfo=None)


def now_local_tz() -> datetime:
    """Return the current local time as a timezone-aware datetime object."""
    return datetime.now(UTC).astimezone()


def now_utc() -> datetime:
    """Return the current UTC time as an aware datetime object."""
    return datetime.now(UTC)


# Use this helper anywhere you need timestamps:

# from datetime_utils import now_local

# ts = now_local().strftime("%Y%m%d_%H%M%S")
# or
# text = now_local().isoformat()
