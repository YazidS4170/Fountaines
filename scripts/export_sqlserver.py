"""Export project tables from the SQLite store to a SQL Server database."""
from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path
from typing import Iterable

import pandas as pd
import pyodbc
from sqlalchemy import create_engine

PROCESSED_DB = Path(__file__).resolve().parents[1] / "data" / "processed" / "paris_fountains.sqlite"


def list_sqlite_tables(connection: sqlite3.Connection) -> Iterable[str]:
    """Return the list of table names in the SQLite database."""
    rows = connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    return [row[0] for row in rows]


def build_odbc_connection_string(
    server: str,
    database: str,
    driver: str,
    username: str | None,
    password: str | None,
    trusted: bool,
    trust_certificate: bool,
) -> str:
    """Construct an ODBC connection string for SQL Server."""
    driver_section = f"DRIVER={{{driver}}}"
    base_parts = [driver_section, f"SERVER={server}", f"DATABASE={database}"]
    if trusted:
        base_parts.append("Trusted_Connection=Yes")
    else:
        if not username or not password:
            raise ValueError("Username and password must be provided when not using trusted authentication.")
        base_parts.append(f"UID={username}")
        base_parts.append(f"PWD={password}")
    if trust_certificate:
        base_parts.append("TrustServerCertificate=Yes")
    return ";".join(base_parts)


def export_to_sql_server(
    sqlite_path: Path,
    server: str,
    database: str,
    driver: str,
    username: str | None,
    password: str | None,
    trusted: bool,
    trust_certificate: bool,
) -> None:
    """Copy all tables from the SQLite file to the target SQL Server database."""
    if not sqlite_path.exists():
        raise FileNotFoundError(f"SQLite file not found: {sqlite_path}")

    server = server.replace("\\\\", "\\")

    odbc_connection_string = build_odbc_connection_string(
        server=server,
        database=database,
        driver=driver,
        username=username,
        password=password,
        trusted=trusted,
        trust_certificate=trust_certificate,
    )
    engine = create_engine(
        "mssql+pyodbc://",
        creator=lambda: pyodbc.connect(odbc_connection_string),
        fast_executemany=True,
    )

    with sqlite3.connect(sqlite_path) as sqlite_conn:
        tables = list_sqlite_tables(sqlite_conn)
        if not tables:
            raise RuntimeError("No tables found in the SQLite database.")
        for table in tables:
            df = pd.read_sql_query(f"SELECT * FROM {table}", sqlite_conn)
            df.to_sql(table, engine, if_exists="replace", index=False)
            print(f"Exported table: {table} ({len(df)} rows)")

    print("Export completed successfully.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Copy project tables from SQLite to SQL Server.")
    parser.add_argument("--sqlite", type=Path, default=PROCESSED_DB, help="Path to the SQLite database file.")
    parser.add_argument("--server", required=True, help="SQL Server instance, e.g. localhost\\SQLEXPRESS.")
    parser.add_argument("--database", required=True, help="Target SQL Server database name (must already exist).")
    parser.add_argument("--driver", default="ODBC Driver 17 for SQL Server", help="ODBC driver name installed on the machine.")
    parser.add_argument("--username", help="SQL Server login name (omit when using trusted auth).")
    parser.add_argument("--password", help="SQL Server password (omit when using trusted auth).")
    parser.add_argument("--trusted", action="store_true", help="Use Windows authentication (Trusted_Connection=Yes).")
    parser.add_argument(
        "--trust-server-certificate",
        action="store_true",
        help="Set TrustServerCertificate=Yes in the connection string.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    export_to_sql_server(
        sqlite_path=args.sqlite,
        server=args.server,
        database=args.database,
        driver=args.driver,
        username=args.username,
        password=args.password,
        trusted=args.trusted,
        trust_certificate=args.trust_server_certificate,
    )


if __name__ == "__main__":
    main()
