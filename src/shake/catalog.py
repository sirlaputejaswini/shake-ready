"""Light loading and cleaning of the USGS GeoJSON catalog.

``scripts/fetch_data.py`` writes the raw catalog to ``data/catalog.geojson``.
This module flattens it into a tidy DataFrame of (time, magnitude, lat, lon,
depth_km, place) with no interpretation — all statistics live elsewhere.
"""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
GEOJSON_NAME = "catalog.geojson"


def raw_geojson_path() -> Path:
    """Path where scripts/fetch_data.py puts the catalog."""
    return DATA_DIR / GEOJSON_NAME


def load(ensure: bool = True) -> pd.DataFrame:
    """Load the catalog into a chronologically sorted DataFrame.

    Cleaning is intentionally minimal: flatten the GeoJSON features, parse
    timestamps as UTC, sort by time, and drop exact duplicate event IDs
    (the USGS sometimes revises events in place; duplicates would double
    count). Events without a magnitude are dropped — without one they are
    useless for any magnitude-based analysis.
    """
    path = raw_geojson_path()
    if ensure and not path.exists():
        raise FileNotFoundError(
            f"Catalog not found at {path}. Run `python scripts/fetch_data.py` first."
        )
    import json

    features = json.loads(path.read_text())["features"]
    rows = []
    for feature in features:
        props = feature["properties"]
        lon, lat, depth = feature["geometry"]["coordinates"]
        rows.append(
            {
                "event_id": feature["id"],
                "time": pd.to_datetime(props["time"], unit="ms", utc=True),
                "magnitude": props["mag"],
                "latitude": lat,
                "longitude": lon,
                "depth_km": depth,
                "place": props["place"],
                "url": props["url"],
            }
        )
    df = pd.DataFrame(rows)
    df = df.dropna(subset=["magnitude"])
    df = df.drop_duplicates(subset=["event_id"], keep="first")
    df = df.sort_values("time").reset_index(drop=True)
    return df
