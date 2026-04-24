"""
Wayback Machine snapshot fetcher.

Fetches HTML for individual snapshots with polite rate limiting and retries.
"""

import requests
import time
import hashlib
from pathlib import Path
from typing import Optional


USER_AGENT = (
    "HiringMarketResearch/1.0 "
    "(personal research project; contact: alokdeep9925@gmail.com)"
)


def fetch_snapshot(
    snapshot_url: str,
    max_retries: int = 3,
    timeout: int = 30,
    sleep_seconds: float = 2.0,
) -> Optional[str]:
    """
    Fetch the HTML of a Wayback Machine snapshot.

    Handles rate limiting with exponential backoff on 429/503.
    Returns None if the snapshot is unrecoverable.
    """
    headers = {"User-Agent": USER_AGENT}
    backoff = 5.0

    for attempt in range(max_retries):
        try:
            response = requests.get(
                snapshot_url,
                headers=headers,
                timeout=timeout,
                allow_redirects=True,
            )

            if response.status_code == 200:
                time.sleep(sleep_seconds)
                return response.text

            if response.status_code in (429, 503):
                # Rate-limited; back off and retry
                wait = backoff * (2 ** attempt)
                print(f"  Rate-limited ({response.status_code}), waiting {wait}s")
                time.sleep(wait)
                continue

            # Other errors: don't retry
            print(f"  HTTP {response.status_code} for {snapshot_url}")
            return None

        except requests.exceptions.RequestException as e:
            wait = backoff * (2 ** attempt)
            print(f"  Error: {e}. Waiting {wait}s before retry")
            time.sleep(wait)

    return None


def cache_path(cache_dir: Path, company: str, timestamp: str) -> Path:
    """Deterministic path where a snapshot's HTML is cached on disk."""
    return cache_dir / company / f"{timestamp}.html"


def fetch_with_cache(
    snapshot_url: str,
    company: str,
    timestamp: str,
    cache_dir: Path,
    sleep_seconds: float = 2.0,
) -> Optional[str]:
    """
    Fetch a snapshot, using disk cache if available.

    Never re-fetches something already on disk. This is critical for
    iterative development — you'll run the pipeline many times.
    """
    path = cache_path(cache_dir, company, timestamp)
    if path.exists():
        return path.read_text(encoding="utf-8", errors="replace")

    html = fetch_snapshot(snapshot_url, sleep_seconds=sleep_seconds)
    if html is None:
        return None

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return html


def looks_like_js_wall(html: str) -> bool:
    """
    Heuristic: does this page look like a JS-rendered shell with no content?

    If the HTML is short and contains React/Vue/Angular root markers but
    no job listings, we're probably looking at an empty SPA shell.
    """
    if len(html) < 10_000:
        # Anything under 10KB is almost certainly not a populated jobs page
        markers = ['id="root"', 'id="app"', "ng-app", "__NEXT_DATA__"]
        if any(m in html for m in markers):
            return True
    return False


if __name__ == "__main__":
    # Smoke test
    test_url = "https://web.archive.org/web/20250315000000/https://jobs.lever.co/razorpay"
    html = fetch_snapshot(test_url)
    if html:
        print(f"Fetched {len(html):,} chars")
        print(f"Looks like JS wall: {looks_like_js_wall(html)}")
    else:
        print("Fetch failed")
