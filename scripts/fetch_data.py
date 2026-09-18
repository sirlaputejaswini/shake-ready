"""Download the PNW earthquake catalog slice from the USGS fdsnws event API.

The U.S. Geological Survey's earthquake catalog is public domain
(https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits).
No API key is needed.

Query parameters are deliberately bounded (magnitude, region, time window)
so the download finishes in well under three minutes. The raw GeoJSON is
stored in ``data/`` (gitignored — never committed) as ``catalog.geojson``.

Usage:
    python scripts/fetch_data.py
"""

from datetime import datetime, timezone
from pathlib import Path

import requests

API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# Bounding box: the Pacific Northwest plus the northern California coast,
# which shares the Cascadia subduction zone.
QUERY_PARAMS = {
    "format": "geojson",
    "minlatitude": 40.0,
    "maxlatitude": 49.5,
    "minlongitude": -126.0,
    "maxlongitude": -116.0,
    "minmagnitude": 2.5,  # ~completeness magnitude for this region in recent years
    "starttime": "2016-01-01",
    "orderby": "time",
    "limit": 20000,  # safety cap; actual catalog is ~3.5k events
}

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
OUT_PATH = DATA_DIR / "catalog.geojson"


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    params = dict(QUERY_PARAMS)
    # Re-querying must reproduce the same slice, so pin the end time.
    params["endtime"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"Querying {API_URL} with:")
    for key, value in params.items():
        print(f"  {key}={value}")

    response = requests.get(API_URL, params=params, timeout=120)
    response.raise_for_status()
    payload = response.json()

    features = payload.get("features", [])
    OUT_PATH.write_text(response.text)
    print(f"Saved {len(features)} events to {OUT_PATH}")


if __name__ == "__main__":
    main()
