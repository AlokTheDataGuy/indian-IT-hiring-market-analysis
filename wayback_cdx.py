"""
Wayback Machine CDX API client.

The CDX Server API lets you list all available snapshots for a URL.
Docs: https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server
"""

import requests
import time
from datetime import datetime
from typing import Optional


CDX_ENDPOINT = "https://web.archive.org/cdx/search/cdx"


def query_snapshots(
    url: str,
    from_date: str = "20240101",
    to_date: Optional[str] = None,
    match_type: str = "prefix",
    collapse_by: str = "digest",
    limit: Optional[int] = None,
    sleep_seconds: float = 2.0,
) -> list[dict]:
    """
    Query the Wayback Machine CDX API for snapshots of a URL.

    Args:
        url: The URL to look up. e.g. 'jobs.lever.co/razorpay'
        from_date: Start date in YYYYMMDD format. Default: 20240101.
        to_date: End date in YYYYMMDD format. Defaults to today.
        match_type: 'exact', 'prefix', 'host', or 'domain'.
                    'prefix' is usually what you want for career pages.
        collapse_by: 'digest' dedupes consecutive snapshots with the same content.
                     Pass None to disable.
        limit: Max results to return. None = no limit.
        sleep_seconds: Polite delay after the request.

    Returns:
        List of dicts, each representing a snapshot with keys:
        timestamp, original_url, mimetype, statuscode, digest, length
    """
    if to_date is None:
        to_date = datetime.utcnow().strftime("%Y%m%d")

    params = {
        "url": url,
        "from": from_date,
        "to": to_date,
        "output": "json",
        "matchType": match_type,
        "filter": "statuscode:200",  # only successful captures
        "fl": "timestamp,original,mimetype,statuscode,digest,length",
    }
    if collapse_by:
        params["collapse"] = collapse_by
    if limit:
        params["limit"] = str(limit)

    response = requests.get(CDX_ENDPOINT, params=params, timeout=30)
    response.raise_for_status()
    time.sleep(sleep_seconds)

    data = response.json()
    if not data:
        return []

    # First row is the header; the rest are records
    header = data[0]
    rows = data[1:]
    return [dict(zip(header, row)) for row in rows]


def sample_weekly(snapshots: list[dict]) -> list[dict]:
    """
    From a list of snapshots, keep at most one per ISO week.
    Reduces fetch volume dramatically without losing temporal resolution.
    """
    seen_weeks = set()
    sampled = []
    for snap in snapshots:
        ts = snap["timestamp"]
        # timestamp format: YYYYMMDDhhmmss
        dt = datetime.strptime(ts[:8], "%Y%m%d")
        week_key = f"{dt.isocalendar().year}-W{dt.isocalendar().week:02d}"
        if week_key not in seen_weeks:
            seen_weeks.add(week_key)
            sampled.append(snap)
    return sampled


def build_snapshot_url(timestamp: str, original_url: str) -> str:
    """Construct the direct URL to fetch a specific snapshot's HTML."""
    return f"https://web.archive.org/web/{timestamp}/{original_url}"


if __name__ == "__main__":
    # Quick smoke test
    snaps = query_snapshots(
        url="jobs.lever.co/razorpay",
        from_date="20241001",
        to_date="20260101",
        limit=50,
    )
    print(f"Found {len(snaps)} snapshots")
    weekly = sample_weekly(snaps)
    print(f"After weekly sampling: {len(weekly)}")
    for s in weekly[:5]:
        print(f"  {s['timestamp']}  {s['original']}")
