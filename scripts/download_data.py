"""Download project datasets directly from the Paris open-data API."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Final

import requests

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_ROOT / "data" / "raw"

FONTAINS_URL: Final[str] = "https://opendata.paris.fr/api/records/1.0/download/?dataset=fontaines-a-boire&format=csv"
FONTAINS_PATH = RAW_DIR / "fontaines_a_boire.csv"

SENIORS_URL: Final[str] = (
    "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/"
    "nombre-de-beneficiaires-pass-paris-seniors-ou-access/records?limit=100"
)
SENIORS_PATH = RAW_DIR / "nombre_de_beneficiaires_pass_paris_seniors.json"


def download_file(url: str, destination: Path) -> None:
    """Fetch content from *url* and save it to *destination*."""
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(response.content)


def fetch_fontaines(force: bool = False) -> None:
    """Download the fountains dataset if missing or *force* requested."""
    if FONTAINS_PATH.exists() and not force:
        logging.info("Fountains CSV already present; skipping download.")
        return
    logging.info("Downloading fountains dataset from %s", FONTAINS_URL)
    download_file(FONTAINS_URL, FONTAINS_PATH)


def fetch_seniors(force: bool = False) -> None:
    """Download the seniors dataset if missing or *force* requested."""
    if SENIORS_PATH.exists() and not force:
        logging.info("Seniors JSON already present; skipping download.")
        return
    logging.info("Downloading seniors dataset from %s", SENIORS_URL)
    download_file(SENIORS_URL, SENIORS_PATH)


def ensure_datasets(force: bool = False) -> None:
    """Ensure both datasets required for the analysis are available locally."""
    fetch_fontaines(force=force)
    fetch_seniors(force=force)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    ensure_datasets(force=False)


if __name__ == "__main__":
    main()
