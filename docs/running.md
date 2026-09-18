# How to run

```bash
# 1. Create and activate a virtual environment
python -m venv .venv && source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Fetch the catalog slice (public USGS API, no key; takes ~seconds)
python scripts/fetch_data.py

# 4. Run the full pipeline
PYTHONPATH=src python -m shake.run
```

The full pipeline runs in under a minute on a laptop (fetch ~5 s,
analysis ~3 s).

## Outputs

| Path | Contents |
|---|---|
| `results/metrics.txt` | All computed numbers (see below) |
| `results/magnitude_frequency.png` | Magnitude-frequency histogram + Gutenberg–Richter fit |
| `results/depth_distance.png` | Depth histogram + epicentral distance to Seattle |
| `results/briefing.txt` | Plain-language preparedness briefing (also printed to stdout) |

Reference run (2026-09-18, real data, 3,463 events 2016-01-01 → 2026-09-16):

```
events: 3463
completeness_mc: 2.5
b_value_mle: 1.027
b_value_least_squares: 0.835
largest_event_magnitude: 7.0
largest_event_time: 2024-12-05
largest_event_place: 2024 Offshore Cape Mendocino, California Earthquake
aftershocks_in_window: 322
omori_p: 1.178
omori_c_days: 0.7846
omori_K: 89.31
omori_r2: 0.885
events_within_200km_of_seattle: 314
median_depth_km: 12.48
```

Numbers shift slightly as the catalog grows — the window end is the fetch
date. Re-run any time to refresh.
