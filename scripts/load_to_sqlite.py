"""Load project datasets and metrics into a SQLite database."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pandas as pd

from compute_metrics import (
    FONTAINS_PATH,
    PROCESSED_DIR,
    SENIORS_PATH,
    compute_metrics,
    load_fountains,
    load_seniors,
)
from download_data import ensure_datasets

DB_PATH = PROCESSED_DIR / "paris_fountains.sqlite"


def load_raw_fountains(path: Path) -> pd.DataFrame:
    """Return the raw fountains dataset with all columns."""
    return pd.read_csv(path, sep=";")


def load_raw_seniors(path: Path) -> pd.DataFrame:
    """Return the raw seniors dataset as downloaded from the API."""
    data = json.loads(path.read_text(encoding="utf-8"))
    records = data.get("results", [])
    df = pd.DataFrame.from_records(records)
    if not df.empty:
        df = df.apply(
            lambda column: column.map(
                lambda value: json.dumps(value)
                if isinstance(value, (dict, list))
                else value
            )
        )
    return df


def main() -> None:
    ensure_datasets(force=False)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    raw_fountains = load_raw_fountains(FONTAINS_PATH)
    raw_seniors = load_raw_seniors(SENIORS_PATH)
    fountains_available = load_fountains(FONTAINS_PATH)
    seniors_latest = load_seniors(SENIORS_PATH)
    metrics = compute_metrics()

    with sqlite3.connect(DB_PATH) as connection:
        raw_fountains.to_sql("fountains_raw", connection, if_exists="replace", index=False)
        raw_seniors.to_sql("seniors_raw", connection, if_exists="replace", index=False)
        fountains_available.to_sql("fountains_available", connection, if_exists="replace", index=False)
        seniors_latest.to_sql("seniors_latest", connection, if_exists="replace", index=False)
        metrics.to_sql("fountains_vs_seniors", connection, if_exists="replace", index=False)

    print(f"SQLite database created at: {DB_PATH}")


if __name__ == "__main__":
    main()
