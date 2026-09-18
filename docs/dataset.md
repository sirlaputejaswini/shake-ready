# Dataset provenance

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

- **Storage:** the raw catalog is downloaded to `data/` (gitignored, never
  committed). Only derived artifacts (`results/`) are committed.
- **Reproducibility:** the fetch script pins `endtime` at download time;
  re-running the fetch on a later date extends the window, so reference
  numbers drift slowly as the catalog grows.
