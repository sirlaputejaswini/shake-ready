"""Plain-language preparedness briefing, written from the computed numbers.

The briefing is deliberately two-layered:

1. What the *data* say — descriptive statistics of the catalog slice.
2. What preparedness *experts* recommend — generic, public guidance
   (emergency kit, securing heavy furniture, knowing Drop/Cover/Hold On).
   None of this comes from the data; it is standard public guidance and
   the text says so.

Every briefing carries the no-prediction disclaimer. If any number in it
looked like a forecast, that would be a bug — report it as one.
"""

from datetime import datetime

from .aftershocks import OmoriResult, SEATTLE_LAT, SEATTLE_LON
from .gutenberg_richter import GutenbergRichterResult

DISCLAIMER = (
    "IMPORTANT: Everything in this briefing describes PAST seismicity. "
    "It does not predict when, where, or how large the next earthquake "
    "will be. No statistical method applied here has forecasting power."
)


def write_briefing(
    n_events: int,
    start: str,
    end: str,
    gr: GutenbergRichterResult,
    omori: OmoriResult,
    n_within_200km_of_seattle: int,
    median_depth_km: float,
) -> str:
    """Render the briefing text from the real computed values."""
    generated = datetime.now().strftime("%Y-%m-%d")
    lines = [
        "SHAKE-READY: PACIFIC NORTHWEST SEISMICITY BRIEFING",
        f"Generated {generated} from the USGS Earthquake Catalog (public domain).",
        "",
        DISCLAIMER,
        "",
        "WHAT THE DATA SHOW (2016 to present, magnitude 2.5 and up):",
        f"- {n_events:,} earthquakes were recorded in the Pacific Northwest "
        f"bounding box between {start} and {end}.",
        f"- The catalog is reasonably complete down to magnitude {gr.mc:.1f}.",
        f"- Gutenberg-Richter b-value: {gr.b_mle:.2f} (least-squares check: "
        f"{gr.b_ls:.2f}). A b-value near 1 is typical worldwide: each step "
        "down in magnitude brings roughly ten times as many earthquakes.",
        f"- Largest event in the window: magnitude {omori.mainshock_magnitude:.1f}, "
        f"{omori.mainshock_place} on {omori.mainshock_time.strftime('%Y-%m-%d')}.",
        f"- After that mainshock, {omori.n_aftershocks} aftershocks were recorded "
        f"within {omori.radius_km:.0f} km over {omori.window_days} days. The "
        f"decay fits the Omori-Utsu law with p = {omori.p:.2f} "
        f"(c = {omori.c_days:.3f} days, R^2 = {omori.fit_r2:.2f}) — a textbook "
        "relaxing sequence, exactly what seismologists expect.",
        f"- {n_within_200km_of_seattle} of the events occurred within 200 km of "
        "downtown Seattle; the median event depth was "
        f"{median_depth_km:.1f} km.",
        "",
        "WHAT THIS MEANS FOR PREPAREDNESS:",
        "- The Pacific Northwest is seismically active on human timescales: "
        "hundreds of detectable earthquakes every year. Most are too small "
        "to feel, but the same faults produce the region's large ones.",
        "- Aftershock sequences last weeks to months after a large event — "
        "that is the one timing statement the data support, and it only "
        "applies *after* a mainshock has already happened.",
        "- Standard public guidance (not derived from this data): keep two "
        "weeks of food, medication, and emergency supplies; secure heavy "
        "furniture; know Drop, Cover, and Hold On; keep shoes and a "
        "flashlight by the bed. See ready.gov and the Washington Emergency "
        "Management Division for checklists.",
        "",
        "HONEST LIMITS OF THIS BRIEFING:",
        "- Magnitude 2.5 is a *recent-era* completeness level for this "
        "region. Earlier catalogs and smaller events are undercounted, so "
        "long-term rates inferred from short windows are approximate.",
        "- The aftershock box is a simple distance/time window, not a "
        "proper declustering — a few background events are mixed in.",
        f"- Seattle is at ({SEATTLE_LAT}, {SEATTLE_LON}); 'distance to "
        "Seattle' is epicentral distance, not shaking intensity, which "
        "depends on depth, geology, and building type.",
        "- Again: none of this predicts the next earthquake.",
    ]
    return "\n".join(lines)
