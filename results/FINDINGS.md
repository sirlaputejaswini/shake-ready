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

## Artifacts

- `metrics.txt` — every computed number.
- `magnitude_frequency.png` — histogram with the MLE fit line.
- `depth_distance.png` — depth distribution and distance-to-Seattle histogram.
- `briefing.txt` — the plain-language briefing generated from these numbers.

Re-run any time (`python scripts/fetch_data.py && PYTHONPATH=src python -m shake.run`)
to refresh these findings as the catalog grows.
