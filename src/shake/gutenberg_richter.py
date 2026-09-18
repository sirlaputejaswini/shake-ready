"""Gutenberg–Richter magnitude–frequency analysis.

The Gutenberg–Richter relation says earthquake counts follow
``log10 N(M) = a - b*M``: for every magnitude unit you go down, events get
~10^b times more frequent. Globally b ≈ 1. The b-value is estimated two
ways here:

1. Maximum-likelihood (Aki, 1965): ``b = log10(e) / (mean(M) - Mc)``,
   computed only on events at or above the completeness magnitude Mc.
   This is the honest one — it does not depend on arbitrary binning.
2. Ordinary least squares on log10 cumulative counts (via scikit-learn),
   reported as a sanity check against the MLE value.

Mc itself is picked by the maximum-curvature heuristic (the most
populated magnitude bin) and then nudged up slightly, because incomplete
small events drag the MLE b-value down.

None of this forecasts anything. It only describes the catalog we have.
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

BIN_WIDTH = 0.1


@dataclass
class GutenbergRichterResult:
    mc: float  # completeness magnitude used
    b_mle: float
    b_ls: float
    a_value: float  # log10 N(M=0) intercept from the MLE fit
    n_used: int  # events at or above Mc
    annual_m7_equivalent: float  # expected M≥7 rate from the fit, per year


def estimate_completeness(magnitudes: np.ndarray, bin_width: float = BIN_WIDTH) -> float:
    """Pick a completeness magnitude from the histogram's peak bin.

    Maximum curvature is crude but transparent; we then round *up* to the
    next bin edge so small-event incompleteness can't silently bias b.
    """
    bins = np.arange(magnitudes.min(), magnitudes.max() + bin_width, bin_width)
    counts, edges = np.histogram(magnitudes, bins=bins)
    peak = edges[np.argmax(counts)]
    return float(np.ceil(peak / bin_width) * bin_width)


def fit(df: pd.DataFrame, mc: float | None = None) -> GutenbergRichterResult:
    """Fit the Gutenberg–Richter relation to events at/above completeness."""
    mags = df["magnitude"].to_numpy()
    if mc is None:
        mc = estimate_completeness(mags)
    usable = mags[mags >= mc - 1e-9]
    if len(usable) < 10:
        raise ValueError(f"Only {len(usable)} events at/above Mc={mc}; cannot fit.")

    # Aki (1965) maximum-likelihood estimator.
    b_mle = float(np.log10(np.e) / (usable.mean() - mc))

    # Least-squares check on cumulative counts: log10 N(M) vs M.
    centers = np.arange(mc, usable.max() + BIN_WIDTH, BIN_WIDTH)
    cumulative = np.array([(usable >= m).sum() for m in centers])
    positive = cumulative > 0
    reg = LinearRegression().fit(
        centers[positive].reshape(-1, 1), np.log10(cumulative[positive])
    )
    b_ls = float(-reg.coef_[0])
    a_value = float(reg.intercept_)

    # What the fit implies per year — descriptive, not a prediction.
    years = (
        df["time"].max() - df["time"].min()
    ).total_seconds() / (365.25 * 24 * 3600)
    annual_m7 = (10 ** (a_value - b_mle * 7.0)) / max(years, 1e-9)

    return GutenbergRichterResult(
        mc=mc,
        b_mle=b_mle,
        b_ls=b_ls,
        a_value=a_value,
        n_used=len(usable),
        annual_m7_equivalent=annual_m7,
    )


def frequency_table(df: pd.DataFrame, mc: float) -> pd.DataFrame:
    """Binned non-cumulative counts and cumulative log10 counts for plotting."""
    mags = df["magnitude"].to_numpy()
    edges = np.arange(np.floor(mags.min() * 10) / 10, mags.max() + BIN_WIDTH, BIN_WIDTH)
    counts, _ = np.histogram(mags, bins=edges)
    centers = edges[:-1] + BIN_WIDTH / 2
    cumulative = np.array([(mags >= e).sum() for e in edges[:-1]])
    return pd.DataFrame(
        {
            "magnitude": centers,
            "count": counts,
            "cumulative": cumulative,
            "log10_cumulative": np.where(
                cumulative > 0, np.log10(np.maximum(cumulative, 1)), np.nan
            ),
        }
    )
