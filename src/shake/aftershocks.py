"""Aftershock decay: fit the Omori–Utsu law to the largest recent sequence.

After a big earthquake, aftershock *rate* decays roughly as
``n(t) = K / (t + c)^p`` (Omori–Utsu), with p ≈ 1 in most sequences. We:

1. Take the largest-magnitude event in the catalog as the mainshock.
2. Keep later events within ``radius_km`` and ``window_days`` — a simple
   space–time box. This is a heuristic, not a declustering algorithm
   (proper declustering needs the full Gardner–Knopoff or Reasenberg
   machinery), and the results section says so.
3. Bin the sequence into daily rates and fit (K, c, p) with
   ``scipy.optimize.curve_fit`` on ``n(t) = K / (t + c)^p``.

A fitted p near 1 with decaying residuals is the normal, boring signature
of a relaxing aftershock sequence. It tells us nothing about the *next*
mainshock — this is characterization, not forecasting.
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# Seattle's coordinates, used for the depth/distance breakdown in run.py.
SEATTLE_LAT, SEATTLE_LON = 47.6062, -122.3321


@dataclass
class OmoriResult:
    mainshock_id: str
    mainshock_magnitude: float
    mainshock_time: pd.Timestamp
    mainshock_place: str
    n_aftershocks: int
    K: float
    c_days: float
    p: float
    fit_r2: float
    window_days: int
    radius_km: float


def haversine_km(lat1: np.ndarray, lon1: np.ndarray, lat2: float, lon2: float) -> np.ndarray:
    """Great-circle distance in km (spherical Earth is fine at these scales)."""
    lat1, lon1 = np.radians(lat1), np.radians(lon1)
    lat2, lon2 = np.radians(lat2), np.radians(lon2)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return 2 * 6371.0 * np.arcsin(np.sqrt(a))


def _omori(t: np.ndarray, K: float, c: float, p: float) -> np.ndarray:
    return K / (t + c) ** p


def select_aftershocks(
    df: pd.DataFrame, radius_km: float = 100.0, window_days: int = 30
) -> tuple[pd.Series, pd.DataFrame]:
    """Return (mainshock row, aftershock candidates in the space–time box)."""
    mainshock = df.loc[df["magnitude"].idxmax()]
    later = df[df["time"] > mainshock["time"]]
    elapsed_days = (later["time"] - mainshock["time"]).dt.total_seconds() / 86400.0
    distance = haversine_km(
        later["latitude"].to_numpy(),
        later["longitude"].to_numpy(),
        mainshock["latitude"],
        mainshock["longitude"],
    )
    mask = (elapsed_days <= window_days) & (distance <= radius_km)
    return mainshock, later[mask].copy()


def fit_omori(
    df: pd.DataFrame, radius_km: float = 100.0, window_days: int = 30
) -> OmoriResult:
    """Fit Omori–Utsu decay to daily aftershock rates after the largest event."""
    mainshock, aftershocks = select_aftershocks(df, radius_km, window_days)
    if len(aftershocks) < 20:
        raise ValueError(
            f"Only {len(aftershocks)} aftershock candidates — too few to fit."
        )

    elapsed = (
        (aftershocks["time"] - mainshock["time"]).dt.total_seconds() / 86400.0
    ).to_numpy()
    # Daily rate bins; drop the first day since catalogs are usually
    # incomplete in the chaotic hours right after a mainshock.
    bins = np.arange(1, window_days + 1)
    counts, _ = np.histogram(elapsed, bins=bins)
    t = bins[:-1] + 0.5  # bin centers, in days
    positive = counts > 0
    if positive.sum() < 5:
        raise ValueError("Too few non-empty daily bins to fit Omori–Utsu.")

    popt, _ = curve_fit(
        _omori,
        t[positive],
        counts[positive].astype(float),
        p0=[counts[positive].max(), 0.1, 1.0],
        bounds=([0, 1e-3, 0.3], [np.inf, 5.0, 3.0]),
        maxfev=10000,
    )
    K, c, p = (float(v) for v in popt)
    predicted = _omori(t[positive], K, c, p)
    observed = counts[positive].astype(float)
    ss_res = float(np.sum((observed - predicted) ** 2))
    ss_tot = float(np.sum((observed - observed.mean()) ** 2))
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")

    return OmoriResult(
        mainshock_id=str(mainshock["event_id"]),
        mainshock_magnitude=float(mainshock["magnitude"]),
        mainshock_time=mainshock["time"],
        mainshock_place=str(mainshock["place"]),
        n_aftershocks=len(aftershocks),
        K=K,
        c_days=c,
        p=p,
        fit_r2=r2,
        window_days=window_days,
        radius_km=radius_km,
    )
