# Fountains vs Seniors

Mini-project comparing the availability of public drinking fountains in Paris with the number of seniors benefiting from the Pass Paris dispositif.

## Project Layout

- `scripts/compute_metrics.py` – downloads the datasets, computes fountain coverage ratios, and writes `data/processed/fountains_vs_seniors.csv`.
- `scripts/visualize_metrics.py` – renders `data/processed/fountains_per_1000_seniors.png` from the processed CSV.
- `scripts/load_to_sqlite.py` – stores raw, intermediate, and final tables in `data/processed/paris_fountains.sqlite`.
- `scripts/export_sqlserver.py` – replicates the SQLite tables into a SQL Server database (for SSMS demos).
- `scripts/download_data.py` – helper used by the other scripts to fetch the datasets from the Paris Open Data API.
- `data/raw/` – cached downloads from the API (CSV/JSON).
- `data/processed/` – analysis outputs (CSV, PNG, SQLite db).

## Quick Start

1. **Create/activate virtualenv**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
2. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```
   *(If you do not keep a requirements file, install manually: `pip install pandas matplotlib sqlalchemy pyodbc requests`.)*
3. **Run the main workflow**
   ```powershell
   python scripts\compute_metrics.py
   python scripts\visualize_metrics.py
   python scripts\load_to_sqlite.py
   ```
4. **Optional SQL Server export**
   ```powershell
   python scripts\export_sqlserver.py --server "LAPTOP-4G8QP3G4\SQLEXPRESS" --database "ParcFountains" --trusted --trust-server-certificate
   ```

## Outputs

- `data/processed/fountains_vs_seniors.csv` – fountain counts, senior counts, ratios by arrondissement.
- `data/processed/fountains_per_1000_seniors.png` – top coverage bar chart.
- `data/processed/paris_fountains.sqlite` – SQLite store with raw/intermediate/final tables.

## Notes


