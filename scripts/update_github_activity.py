#!/usr/bin/env python3
"""Generate GitHub contribution summary and compact graph data for the website."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

USERNAME = os.environ.get("GITHUB_USERNAME", "maxhabra")
TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
OUTPUT_PATH = Path("assets/data/github-activity.json")
RECENT_DAY_COUNT = 84

GRAPHQL_QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            contributionLevel
            date
          }
        }
      }
    }
  }
}
"""


def fallback_payload(message: str) -> dict[str, Any]:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return {
        "generated_at": now,
        "profile_url": f"https://github.com/{USERNAME}",
        "activity_url": f"https://github.com/{USERNAME}",
        "yearly_contributions": 0,
        "last_contribution_date": None,
        "recent_days": [],
        "source": "fallback",
        "summary": message,
    }


def graphql_request() -> dict[str, Any]:
    if not TOKEN:
        raise ValueError("Missing GITHUB_TOKEN secret")

    payload = json.dumps({"query": GRAPHQL_QUERY, "variables": {"login": USERNAME}}).encode("utf-8")
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github+json",
            "User-Agent": f"{USERNAME}-activity-updater",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))

    if result.get("errors"):
        raise ValueError(f"GraphQL error: {result['errors'][0].get('message', 'unknown')}" )

    data = result.get("data", {})
    user = data.get("user", {})
    collection = user.get("contributionsCollection", {})
    calendar = collection.get("contributionCalendar")
    if not isinstance(calendar, dict):
        raise ValueError("Missing contribution calendar data")
    return calendar


def build_payload(calendar: dict[str, Any]) -> dict[str, Any]:
    total = int(calendar.get("totalContributions", 0))

    days: list[dict[str, Any]] = []
    for week in calendar.get("weeks", []):
        for day in week.get("contributionDays", []):
            days.append(
                {
                    "date": day.get("date"),
                    "count": int(day.get("contributionCount", 0)),
                    "level": day.get("contributionLevel", "NONE"),
                }
            )

    recent_days = days[-RECENT_DAY_COUNT:]

    last_contribution_date = None
    for day in reversed(days):
        if day.get("count", 0) > 0:
            last_contribution_date = day.get("date")
            break

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    summary = f"{total} contributions in the last year"
    if last_contribution_date:
        summary = f"{summary}. Last contribution: {last_contribution_date}."

    return {
        "generated_at": now,
        "profile_url": f"https://github.com/{USERNAME}",
        "activity_url": f"https://github.com/{USERNAME}",
        "yearly_contributions": total,
        "last_contribution_date": last_contribution_date,
        "recent_days": recent_days,
        "source": "graphql",
        "summary": summary,
    }


def write_output(payload: dict[str, Any]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    try:
        calendar = graphql_request()
        payload = build_payload(calendar)
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        payload = fallback_payload(f"Failed to refresh contribution data: {exc}")

    write_output(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
