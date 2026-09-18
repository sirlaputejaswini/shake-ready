# Findings — reference run, 2026-09-18 (real USGS data)

Window: 2016-01-01 → 2026-09-16. Bounding box 40.0–49.5°N, 126–116°W.
3,463 events at M≥2.5.

## What the numbers say

- **The Pacific Northwest is steadily, ordinarily seismic.** 3,463 events
  M≥2.5 in ~10.7 years — roughly one every 27 hours. Nothing in this window
  looks anomalous against the region's known background rate.
- **The magnitude-frequency distribution is textbook.** The Gutenberg–Richter
  b-value by maximum likelihood is **1.03**, essentially the global average
  (~1.0): for every ten M3s, expect about one M4. The least-squares check
  gives 0.83 — pulled down by the largest events, which is exactly why the
  briefing quotes the MLE.
- **The largest event behaved like a textbook mainshock.** The M7.0 offshore
  Cape Mendocino earthquake (2024-12-05) was followed by **322** aftershocks
  within 100 km over 30 days, decaying with Omori p = **1.18** (R² = 0.89) —
  a clean, relaxing sequence, no secondary large shock in the window.
- **Seattle's backyard is active but shallow and moderate.** 314 events fell
  within 200 km of Seattle; median depth 12.5 km. These are epicentral
  distances, not shaking intensities — most were small and unfelt.

## What the numbers do NOT say

- Nothing here constrains *when* the next large Cascadia event occurs.
  A ~10-year catalog slice is blind to a ~500-year megathrust cycle.
- The aftershock fit describes one sequence with a simple box selection;
  it is not a calibrated forecasting model.

## Non-obvious insights from this data

1. **Estimator choice moves the headline number by 20%.** MLE b = 1.03 vs
   least-squares b = 0.83 on identical data — methodology, not geology.
   Public seismic statistics should name their estimator like polls name
   their margin of error.
2. **The decade's biggest sequence decayed faster than textbook**
   (Omori p = 1.18 vs canonical ~1.0, R² = 0.89) — a generic model would
   have overestimated the danger window, and over-warning erodes trust.
3. **Only ~9% of events fell within 200 km of Seattle** while the largest
   was 700+ km away — reassuring, but misleading, because the quiet
   Cascadia megathrust holding the region's largest risk is invisible in a
   10-year catalog. The most important hazard is the one this dataset
   cannot see.
4. **Median depth 12.5 km: the felt record is shallow crustal seismicity.**
   Deep slab events are a different hazard class barely represented here —
   "earthquake risk" is at least two phenomena wearing one name.

See [docs/vision.md](../docs/vision.md) for the full write-up: what becomes
possible in the future because of this work, and concrete use cases at scale.

## Artifacts

- `metrics.txt` — every computed number.
- `magnitude_frequency.png` — histogram with the MLE fit line.
- `depth_distance.png` — depth distribution and distance-to-Seattle histogram.
- `briefing.txt` — the plain-language briefing generated from these numbers.

Re-run any time (`python scripts/fetch_data.py && PYTHONPATH=src python -m shake.run`)
to refresh these findings as the catalog grows.
