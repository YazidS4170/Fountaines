"""Compute coverage metrics between Paris drinking fountains and senior beneficiaries."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from download_data import ensure_datasets


REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_ROOT / "data" / "raw"
PROCESSED_DIR = REPO_ROOT / "data" / "processed"

FONTAINS_PATH = RAW_DIR / "fontaines_a_boire.csv"
SENIORS_PATH = RAW_DIR / "nombre_de_beneficiaires_pass_paris_seniors.json"
OUTPUT_PATH = PROCESSED_DIR / "fountains_vs_seniors.csv"


def load_fountains(path: Path) -> pd.DataFrame:
    """Load fountains CSV and extract arrondissement numbers."""
    df = pd.read_csv(path, sep=";", dtype=str)
    df["commune"] = df["commune"].fillna("")
    df["arrondissement"] = (
        df["commune"].str.extract(r"PARIS\s+(\d{1,2})EME", expand=False).astype("float")
    )
    df = df.dropna(subset=["arrondissement"])
    df["arrondissement"] = df["arrondissement"].astype(int).apply(lambda x: 75000 + x)
    df = df[df["dispo"].str.upper() == "OUI"]
    fountains = (
        df.groupby("arrondissement", as_index=False)["gid"].count().rename(columns={"gid": "fountains_total"})
    )
    return fountains


def load_seniors(path: Path) -> pd.DataFrame:
    """Load senior beneficiaries JSON and retain the latest year per arrondissement."""
    data = json.loads(path.read_text(encoding="utf-8"))
    records = data.get("results", [])
    df = pd.DataFrame.from_records(records)
    keep_cols = ["arrondissement", "personnes_agees", "exercice"]
    missing_cols = set(keep_cols) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing expected columns in seniors dataset: {missing_cols}")
    df = df[keep_cols].copy()
    df["arrondissement"] = df["arrondissement"].astype(int)
    df["exercice"] = df["exercice"].astype(int)
    df["personnes_agees"] = df["personnes_agees"].astype(int)
    df = df.sort_values(["arrondissement", "exercice"], ascending=[True, False])
    latest = df.drop_duplicates(subset=["arrondissement"], keep="first")
    latest = latest.rename(columns={"personnes_agees": "seniors_beneficiaries", "exercice": "latest_exercice"})
    latest = latest[["arrondissement", "latest_exercice", "seniors_beneficiaries"]]
    return latest


def compute_metrics() -> pd.DataFrame:
    ensure_datasets(force=False)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    fountains = load_fountains(FONTAINS_PATH)
    seniors = load_seniors(SENIORS_PATH)
    merged = pd.merge(seniors, fountains, on="arrondissement", how="left")
    merged["fountains_total"] = merged["fountains_total"].fillna(0).astype(int)
    merged["fountains_per_1000_seniors"] = merged.apply(
        lambda row: (row["fountains_total"] / row["seniors_beneficiaries"] * 1000)
        if row["seniors_beneficiaries"] > 0
        else 0,
        axis=1,
    )
    merged = merged.sort_values("fountains_per_1000_seniors", ascending=False)
    output = merged[[
        "arrondissement",
        "latest_exercice",
        "seniors_beneficiaries",
        "fountains_total",
        "fountains_per_1000_seniors",
    ]]
    output.to_csv(OUTPUT_PATH, index=False)
    return output


def main() -> None:
    result = compute_metrics()
    top = result.head(5)[
        [
            "arrondissement",
            "latest_exercice",
            "seniors_beneficiaries",
            "fountains_total",
            "fountains_per_1000_seniors",
        ]
    ]
    pd.options.display.float_format = "{:.2f}".format
    print("Top arrondissements by fountains per 1000 seniors:\n")
    print(top.to_string(index=False))


if __name__ == "__main__":
    main()
