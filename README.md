# Shake-Ready

A data-grounded earthquake resilience briefing for the Pacific Northwest,
built from the public USGS earthquake catalog.

**Full documentation:** [docs/problem.md](docs/problem.md) ·
[docs/approach.md](docs/approach.md) · [docs/running.md](docs/running.md) ·
[docs/dataset.md](docs/dataset.md) · [docs/limitations.md](docs/limitations.md)
· [results/FINDINGS.md](results/FINDINGS.md)

## The problem

The Cascadia region faces a major earthquake in the coming decades — the
Cascadia subduction zone has produced magnitude 9-class events on a
roughly 500-year rhythm, and the last one was in 1700. Households and
cities in Seattle, Portland, and the surrounding region need *honest,
data-grounded* preparedness: what the recent seismic record actually
shows, communicated without hype and without pretending we can forecast
what comes next.

**What this project does not do:** predict earthquakes. Every number and
sentence here describes *past* seismicity. No statistical method in this
pipeline has forecasting power, and the output says so repeatedly.

## Dataset

- **Source:** USGS Earthquake Catalog, fdsnws event web service
  (`https://earthquake.usgs.gov/fdsnws/event/1/`), GeoJSON output.
- **Terms of use:** USGS data are **public domain**
  ([USGS copyrights and credits policy](https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits)).
  No API key required.
- **Exact query** (see `scripts/fetch_data.py` for the pinned version):

  | Parameter | Value |
  |---|---|
  | `format` | `geojson` |
  | `minlatitude` / `maxlatitude` | 40.0 / 49.5 |
  | `minlongitude` / `maxlongitude` | −126.0 / −116.0 |
  | `minmagnitude` | 2.5 |
  | `starttime` | 2016-01-01 |
  | `endtime` | run date (pinned at fetch time for reproducibility) |
  | `orderby` | `time` |
  | `limit` | 20000 (safety cap; actual slice is ~3.5k events) |

  Full URL (with a pinned end date, e.g.):

  ```
  https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minlatitude=40.0&maxlatitude=49.5&minlongitude=-126.0&maxlongitude=-116.0&minmagnitude=2.5&starttime=2016-01-01&endtime=2026-09-18&orderby=time&limit=20000
  ```

  The raw catalog is downloaded to `data/` (gitignored, never committed).

## What the pipeline computes

1. **Catalog load** (`src/shake/catalog.py`) — flatten GeoJSON to a tidy
   DataFrame, drop duplicates, sort chronologically.
2. **Gutenberg–Richter fit** (`src/shake/gutenberg_richter.py`) —
   completeness magnitude via maximum curvature; b-value by maximum
   likelihood (Aki, 1965), with a least-squares check via scikit-learn.
3. **Aftershock decay** (`src/shake/aftershocks.py`) — takes the largest
   event in the window as the mainshock, selects later events within
   100 km / 30 days, and fits the Omori–Utsu law
   `n(t) = K / (t + c)^p` to daily rates with `scipy.optimize.curve_fit`.
4. **Geography** — depth histogram and epicentral distance to Seattle
   (47.6062, −122.3321).
5. **Briefing** (`src/shake/briefing.py`) — a plain-language text summary
   written from the computed numbers, with the no-prediction disclaimer
   baked in.

## How to run

```bash
cd shake-ready
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/fetch_data.py   # downloads the catalog slice (~seconds)
PYTHONPATH=src python -m shake.run
```

Full pipeline runs in under a minute on a laptop (fetch ~5 s, analysis
~3 s).

## Expected output

`results/metrics.txt`:

```
events: 3463
window_start: 2016-01-01
window_end: 2026-09-16
completeness_mc: 2.5
b_value_mle: 1.027
b_value_least_squares: 0.835
events_at_or_above_mc: 3463
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

(Numbers shift slightly as the catalog grows — the window end is the
fetch date.)

`results/magnitude_frequency.png` — magnitude-frequency histogram plus
the Gutenberg–Richter fit.

`results/depth_distance.png` — depth histogram and epicentral distance
to Seattle.

`results/briefing.txt` — the plain-language preparedness briefing,
printed to stdout as well.

Headline results from the reference run (2026-09-18, real data):
**3,463** events M≥2.5 since 2016; b-value **1.03**; largest event the
**M7.0 offshore Cape Mendocino** earthquake of 2024-12-05, followed by
**322** aftershocks within 100 km over 30 days decaying with Omori
**p = 1.18** (R² = 0.89) — a textbook relaxing sequence. **314** events
fell within 200 km of Seattle; median depth **12.5 km**.

## Honest limitations

- **This is descriptive statistics of past seismicity, not prediction.**
  Nothing here forecasts the timing, location, or size of the next
  earthquake. Any reading of these numbers as a forecast is a misuse.
- **Catalog completeness varies by magnitude and era.** M2.5 is a
  reasonable completeness level for this region in recent years, but
  smaller events are undercounted, and older or more remote parts of the
  region are less complete. Rates inferred from a ~10-year window are
  approximate and dominated by the biggest sequences.
- The aftershock selection is a **simple distance/time box**, not a
  proper declustering algorithm — some background events are mixed in,
  and c/p values would shift with a stricter declustering.
- "Distance to Seattle" is **epicentral distance**, not shaking
  intensity, which also depends on depth, local geology, and building
  type.
- The least-squares b-value (0.83) differs from the MLE (1.03) because
  least squares on cumulative counts is pulled by the largest events;
  the MLE is the trustworthy estimate and the one quoted in the
  briefing.
