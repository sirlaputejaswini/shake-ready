"""Entry point: run the full Shake-Ready pipeline.

    python -m shake.run

Reads data/catalog.geojson (via scripts/fetch_data.py), computes the
Gutenberg–Richter fit, the Omori–Utsu aftershock fit after the largest
event, depth and distance-to-Seattle distributions, and writes:

- results/metrics.txt — the actual computed numbers
- results/magnitude_frequency.png — magnitude-frequency + GR fit
- results/depth_distance.png — depth and distance-to-Seattle histograms
- results/briefing.txt — the plain-language preparedness briefing
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless: figures are files, never windows
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from . import aftershocks, briefing, catalog, gutenberg_richter

RESULTS_DIR = Path(__file__).resolve().parents[2] / "results"


def _write_metrics(path: Path, **values: object) -> None:
    with open(path, "w") as f:
        for key, value in values.items():
            f.write(f"{key}: {value}\n")


def _plot_magnitude_frequency(df: pd.DataFrame, gr, path: Path) -> None:
    table = gutenberg_richter.frequency_table(df, gr.mc)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    # Left: non-cumulative counts per 0.1-magnitude bin (log scale).
    axes[0].bar(table["magnitude"], table["count"], width=0.09, color="#2a6f9e")
    axes[0].set_yscale("log")
    axes[0].axvline(gr.mc, color="#c0392b", linestyle="--",
                    label=f"completeness Mc={gr.mc:.1f}")
    axes[0].set_xlabel("Magnitude")
    axes[0].set_ylabel("Event count (log scale)")
    axes[0].set_title("Magnitude-frequency distribution")
    axes[0].legend()

    # Right: cumulative Gutenberg–Richter fit.
    valid = table["log10_cumulative"].notna()
    axes[1].scatter(table.loc[valid, "magnitude"], table.loc[valid, "log10_cumulative"],
                    s=14, color="#2a6f9e", label="catalog")
    m = table.loc[valid, "magnitude"].to_numpy()
    # MLE fit: N(M) = N_used * 10^(-b (M - Mc)), self-consistent with b_mle.
    mle_line = np.log10(gr.n_used) - gr.b_mle * (m - gr.mc)
    axes[1].plot(m, mle_line, color="#c0392b",
                 label=f"GR fit (MLE b={gr.b_mle:.2f})")
    axes[1].axvline(gr.mc, color="#c0392b", linestyle="--")
    axes[1].set_xlabel("Magnitude")
    axes[1].set_ylabel("log10 N(≥M)")
    axes[1].set_title("Gutenberg–Richter fit")
    axes[1].legend()

    fig.suptitle("Pacific Northwest seismicity, M≥2.5 (USGS catalog) — "
                 "descriptive statistics, not a forecast")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def _plot_depth_distance(df: pd.DataFrame, path: Path) -> None:
    dist = aftershocks.haversine_km(
        df["latitude"].to_numpy(), df["longitude"].to_numpy(),
        aftershocks.SEATTLE_LAT, aftershocks.SEATTLE_LON,
    )
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    axes[0].hist(df["depth_km"].clip(upper=150), bins=50, color="#2a6f9e")
    axes[0].set_xlabel("Depth (km)")
    axes[0].set_ylabel("Event count")
    axes[0].set_title("Event depth distribution")

    axes[1].hist(dist, bins=50, color="#2a6f9e")
    axes[1].axvline(200, color="#c0392b", linestyle="--",
                    label="200 km from Seattle")
    axes[1].set_xlabel("Epicentral distance to Seattle (km)")
    axes[1].set_ylabel("Event count")
    axes[1].set_title("How far from Seattle?")
    axes[1].legend()

    fig.suptitle("Depth and distance to Seattle — descriptive only")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    df = catalog.load()
    start = df["time"].min().strftime("%Y-%m-%d")
    end = df["time"].max().strftime("%Y-%m-%d")

    gr = gutenberg_richter.fit(df)
    omori = aftershocks.fit_omori(df)

    dist_to_seattle = aftershocks.haversine_km(
        df["latitude"].to_numpy(), df["longitude"].to_numpy(),
        aftershocks.SEATTLE_LAT, aftershocks.SEATTLE_LON,
    )
    n_near_seattle = int((dist_to_seattle <= 200).sum())
    median_depth = float(df["depth_km"].median())

    _plot_magnitude_frequency(df, gr, RESULTS_DIR / "magnitude_frequency.png")
    _plot_depth_distance(df, RESULTS_DIR / "depth_distance.png")

    _write_metrics(
        RESULTS_DIR / "metrics.txt",
        events=len(df),
        window_start=start,
        window_end=end,
        completeness_mc=round(gr.mc, 2),
        b_value_mle=round(gr.b_mle, 3),
        b_value_least_squares=round(gr.b_ls, 3),
        events_at_or_above_mc=gr.n_used,
        largest_event_magnitude=omori.mainshock_magnitude,
        largest_event_time=omori.mainshock_time.strftime("%Y-%m-%d"),
        largest_event_place=omori.mainshock_place,
        aftershocks_in_window=omori.n_aftershocks,
        omori_p=round(omori.p, 3),
        omori_c_days=round(omori.c_days, 4),
        omori_K=round(omori.K, 3),
        omori_r2=round(omori.fit_r2, 3),
        events_within_200km_of_seattle=n_near_seattle,
        median_depth_km=round(median_depth, 2),
    )

    text = briefing.write_briefing(
        n_events=len(df), start=start, end=end, gr=gr, omori=omori,
        n_within_200km_of_seattle=n_near_seattle, median_depth_km=median_depth,
    )
    (RESULTS_DIR / "briefing.txt").write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
