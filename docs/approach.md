# Approach

The pipeline is five stages, each a small module in `src/shake/`:

1. **Catalog load** (`catalog.py`) — download the USGS GeoJSON catalog slice
   and flatten it to a tidy DataFrame: time, latitude, longitude, depth,
   magnitude. Drop duplicates, sort chronologically.
2. **Gutenberg–Richter fit** (`gutenberg_richter.py`) — estimate the
   completeness magnitude by maximum curvature, then fit the b-value by
   maximum likelihood (Aki, 1965). A least-squares fit via scikit-learn is
   computed as a cross-check and reported honestly when it disagrees.
3. **Aftershock decay** (`aftershocks.py`) — take the largest event in the
   window as the mainshock, select later events within 100 km and 30 days
   (a simple distance/time box, not full declustering), and fit the
   Omori–Utsu law `n(t) = K / (t + c)^p` to daily rates with
   `scipy.optimize.curve_fit`.
4. **Geography** — depth histogram and epicentral distance of each event to
   Seattle (47.6062, −122.3321).
5. **Briefing** (`briefing.py`) — render a plain-language text summary from
   the computed numbers, with the no-prediction disclaimer baked into the
   template itself so it cannot be accidentally dropped.

Why this shape: every stage is independently re-runnable and inspectable,
the statistics are textbook seismology (no exotic models to hide behind),
and the final artifact is a *briefing a person can read*, not a dashboard
nobody opens.
