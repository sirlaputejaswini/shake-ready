# Vision: what this data actually teaches us, and what it unlocks

## Non-obvious insights discovered in this catalog slice

These are not generic observations — they came out of the numbers above:

1. **Published b-values are not comparable unless you know the estimator.**
   The same 3,463 events give b = 1.03 by maximum likelihood and b = 0.83 by
   least squares. The least-squares fit is dragged down by the handful of
   largest events. Two papers quoting "the b-value of the Pacific Northwest"
   can disagree by 20% and both be arithmetically correct — the difference is
   methodology, not geology. Any public-facing seismic statistic should name
   its estimator the way a poll names its margin of error.

2. **This decade's biggest sequence decayed faster than textbook.**
   The M7.0 Cape Mendocino aftershocks fit Omori p = 1.18 (R² = 0.89),
   noticeably above the canonical p ≈ 1.0. In plain terms: the aftershock
   hazard fell off *faster* than a generic model would have predicted. A
   city running on generic parameters would have overestimated the danger
   window — which matters because over-warning erodes trust just as surely
   as under-warning.

3. **The hazard geography of this window is reassuring and misleading at
   once.** Only ~9% of events fell within 200 km of Seattle, and the largest
   event was 700+ km away off Cape Mendocino. A resident reading this decade
   of data would conclude the danger lives elsewhere — while the quiet
   Cascadia megathrust, invisible in a 10-year catalog, holds the region's
   largest long-term risk. *The most important hazard is the one this
   dataset cannot see.* That is itself the insight: short catalogs measure
   background seismicity, not the full hazard.

4. **The felt record is shallow.** Median depth 12.5 km — this is crustal
   seismicity, the kind people actually feel. Deep slab earthquakes (like
   the 2001 Nisqually M6.8 at ~52 km) are a different hazard class and are
   barely represented here. "Earthquake risk" is at least two different
   phenomena wearing one name.

## What becomes possible because of this

- **A seismic weather service.** Minutes after any M5+, an automated
   pipeline like this one fits the sequence and publishes a plain-language
   briefing: how many aftershocks so far, how fast they're decaying, what
   the next 72 hours most plausibly look like — with the uncertainty stated,
   not hidden. The public gets a calibrated decay curve instead of rumors.
- **Preparedness priced in reality, not vibes.** Combine local background
   rates with building-stock and soil data, and a city can rank
   neighborhoods for retrofit subsidies, drill planning, and supply
   pre-positioning — spending resilience money where the numbers point.
- **Aftershock-aware response logistics.** Emergency managers currently
   stage resources on judgment; a fitted Omori curve turns "it'll probably
   calm down" into a staffing schedule.

## Concrete use cases at scale

1. **City emergency operations centers** auto-generate the public briefing
   within 10 minutes of a mainshock, in multiple languages, from the live
   catalog — no seismologist required at 3 a.m.
2. **Schools and hospitals** set drill cadence and "drop, cover, hold on"
   refreshers from their *local* background rate rather than a national
   average nobody believes applies to them.
3. **Homeowners** get a one-page, address-level seismicity summary —
   "314 events within 200 km of Seattle in 10 years, median depth 12.5 km"
   — as a nudge toward securing water heaters and bookcases, the unglamorous
   interventions that actually prevent injuries.
4. **Journalists** get a same-day explainer template ("what an Omori p-value
   means") so the first 24 hours of coverage after a quake are informative
   instead of speculative.

## The honest boundary, restated

None of this predicts earthquakes. Everything above describes the past and
extrapolates *statistical tendencies* of sequences already underway. The
megathrust — the event that matters most — is out of sample. A future built
on this work is one where society responds to earthquakes with calibrated
numbers instead of fear or complacency, not one where we see them coming.
