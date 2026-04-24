"""
Main runner: orchestrates Wayback Machine data collection for all companies.

Phase 1 of the pipeline — this script ONLY downloads HTML.
Parsing happens in a separate step so we can iterate on parsers without
re-downloading anything.

Usage:
    python collect_wayback.py --from-date 20241001 --to-date 20260424
"""

import argparse
import csv
import json
from pathlib import Path
from datetime import datetime

from companies import COMPANIES
from wayback_cdx import query_snapshots, sample_weekly, build_snapshot_url
from wayback_fetcher import fetch_with_cache, looks_like_js_wall


DATA_DIR = Path("data/raw/wayback")
INDEX_PATH = DATA_DIR / "snapshot_index.csv"
LOG_PATH = DATA_DIR / "collection_log.jsonl"


def log(event: dict) -> None:
    """Append a structured event to the collection log."""
    event["ts"] = datetime.utcnow().isoformat()
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a") as f:
        f.write(json.dumps(event) + "\n")


def collect_company(company: dict, from_date: str, to_date: str) -> list[dict]:
    """
    For one company: query CDX, sample weekly, fetch each snapshot to cache.
    Returns list of records (one per successfully fetched snapshot) for the index.
    """
    name = company["name"]
    ats_url = company["ats_url"]
    print(f"\n=== {name} ({ats_url}) ===")

    try:
        snaps = query_snapshots(
            url=ats_url,
            from_date=from_date,
            to_date=to_date,
            match_type="prefix",
            collapse_by="digest",
        )
    except Exception as e:
        print(f"  CDX query failed: {e}")
        log({"event": "cdx_error", "company": name, "error": str(e)})
        return []

    print(f"  CDX returned {len(snaps)} snapshots")
    weekly = sample_weekly(snaps)
    print(f"  After weekly sampling: {len(weekly)}")

    records = []
    for snap in weekly:
        ts = snap["timestamp"]
        original = snap["original"]
        snap_url = build_snapshot_url(ts, original)

        html = fetch_with_cache(
            snapshot_url=snap_url,
            company=name,
            timestamp=ts,
            cache_dir=DATA_DIR / "html",
        )

        if html is None:
            log({"event": "fetch_failed", "company": name, "timestamp": ts})
            continue

        is_js_wall = looks_like_js_wall(html)
        records.append({
            "company": name,
            "ats_platform": company["ats_platform"],
            "timestamp": ts,
            "original_url": original,
            "snapshot_url": snap_url,
            "content_length": len(html),
            "is_js_wall": is_js_wall,
        })
        status = "⚠ JS wall" if is_js_wall else "✓"
        print(f"  {status} {ts}  ({len(html):,} chars)")

    log({"event": "company_done", "company": name, "records": len(records)})
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-date", default="20241001",
                        help="YYYYMMDD, default 20241001")
    parser.add_argument("--to-date", default=None,
                        help="YYYYMMDD, default today")
    parser.add_argument("--only", nargs="+", default=None,
                        help="Only run these company names (for testing)")
    args = parser.parse_args()

    to_date = args.to_date or datetime.utcnow().strftime("%Y%m%d")
    companies_to_run = COMPANIES
    if args.only:
        companies_to_run = [c for c in COMPANIES if c["name"] in args.only]
        if not companies_to_run:
            print(f"No matching companies found for: {args.only}")
            return

    print(f"Collecting snapshots from {args.from_date} to {to_date}")
    print(f"Companies: {len(companies_to_run)}")

    all_records = []
    for company in companies_to_run:
        records = collect_company(company, args.from_date, to_date)
        all_records.extend(records)

    # Write consolidated index
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    if all_records:
        with INDEX_PATH.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=all_records[0].keys())
            writer.writeheader()
            writer.writerows(all_records)

    # Summary
    total = len(all_records)
    js_walls = sum(1 for r in all_records if r["is_js_wall"])
    print(f"\n{'=' * 50}")
    print(f"Collected {total} snapshots total")
    print(f"  Usable: {total - js_walls}")
    print(f"  JS walls (need different approach): {js_walls}")
    print(f"Index written to: {INDEX_PATH}")
    print(f"Log written to: {LOG_PATH}")


if __name__ == "__main__":
    main()
