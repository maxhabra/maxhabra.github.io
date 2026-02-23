#!/usr/bin/env python3
"""Generate a compact GitHub activity summary for the website header."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

USERNAME = os.environ.get("GITHUB_USERNAME", "maxhabra")
TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
OUTPUT_PATH = Path("assets/data/github-activity.json")


@dataclass
class ActivitySummary:
    generated_at: str
    profile_url: str
    activity_url: str
    week_events: int
    day_events: int
    last_event_at: str | None
    last_event_date: str | None
    source: str
    summary: str


def fetch_events() -> tuple[list[dict[str, Any]], str]:
    if TOKEN:
        url = "https://api.github.com/user/events?per_page=100"
        source = "authenticated"
    else:
        url = f"https://api.github.com/users/{USERNAME}/events/public?per_page=100"
        source = "public"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USERNAME}-activity-updater",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))
        if not isinstance(payload, list):
            raise ValueError("Unexpected GitHub API response")
    return payload, source


def parse_timestamp(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def build_summary(events: list[dict[str, Any]], source: str) -> ActivitySummary:
    now = datetime.now(timezone.utc)
    week_cutoff = now - timedelta(days=7)
    day_cutoff = now - timedelta(days=1)

    week_events = 0
    day_events = 0
    last_event_at = None

    for event in events:
        created_at = event.get("created_at")
        if not isinstance(created_at, str):
            continue

        ts = parse_timestamp(created_at)
        if ts >= week_cutoff:
            week_events += 1
        if ts >= day_cutoff:
            day_events += 1

        if last_event_at is None:
            last_event_at = created_at

    last_event_date = None
    if last_event_at:
        last_event_date = last_event_at[:10]

    if last_event_date:
        summary = f"7d events: {week_events}. Last activity: {last_event_date}."
    else:
        summary = "No recent GitHub events found."

    return ActivitySummary(
        generated_at=now.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        profile_url=f"https://github.com/{USERNAME}",
        activity_url=f"https://github.com/{USERNAME}",
        week_events=week_events,
        day_events=day_events,
        last_event_at=last_event_at,
        last_event_date=last_event_date,
        source=source,
        summary=summary,
    )


def write_output(summary: ActivitySummary) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(summary.__dict__, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    try:
        events, source = fetch_events()
        summary = build_summary(events, source)
    except (urllib.error.URLError, ValueError, TimeoutError) as exc:
        fallback = ActivitySummary(
            generated_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            profile_url=f"https://github.com/{USERNAME}",
            activity_url=f"https://github.com/{USERNAME}",
            week_events=0,
            day_events=0,
            last_event_at=None,
            last_event_date=None,
            source="fallback",
            summary=f"Failed to refresh activity: {exc}",
        )
        write_output(fallback)
        return 0

    write_output(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
