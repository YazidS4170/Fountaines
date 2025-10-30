"""Generate visualisations for the fountains vs seniors project."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = REPO_ROOT / "data" / "processed"
DATA_PATH = PROCESSED_DIR / "fountains_vs_seniors.csv"
OUTPUT_PNG = PROCESSED_DIR / "fountains_per_1000_seniors.png"


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.sort_values("fountains_per_1000_seniors", ascending=False)
    return df


def plot_top_bottom(df: pd.DataFrame, top_n: int = 10) -> None:
    top = df.head(top_n)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top["arrondissement"].astype(str), top["fountains_per_1000_seniors"], color="#1f77b4")
    ax.invert_yaxis()
    ax.set_xlabel("Fontaines disponibles pour 1000 bénéficiaires seniors")
    ax.set_ylabel("Arrondissement")
    ax.set_title(f"Top {top_n} arrondissements par densité de fontaines (2017)")
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(OUTPUT_PNG, dpi=150)
    plt.close(fig)


def main() -> None:
    data = load_data(DATA_PATH)
    plot_top_bottom(data, top_n=10)


if __name__ == "__main__":
    main()
