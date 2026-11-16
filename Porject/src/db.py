from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from .config import DATA_DIR, get_database_url
from .data_generation import generate_demo_datasets


def get_engine():
    return create_engine(get_database_url(), future=True)


def ensure_demo_data() -> None:
    engine = get_engine()
    table_names = {"PRODUCTS", "CUSTOMERS", "TRANSACTIONS", "INVENTORY", "RECOMMENDATION"}
    with engine.connect() as conn:
        existing = set(conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'")) if "sqlite" in get_database_url() else conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")))
    if table_names.issubset(existing):
        return

    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not any(DATA_DIR.glob("*.csv")):
        generate_demo_datasets(DATA_DIR)

    for file_name, table_name in [
        ("PRODUCTS.csv", "PRODUCTS"),
        ("CUSTOMERS.csv", "CUSTOMERS"),
        ("TRANSACTIONS.csv", "TRANSACTIONS"),
        ("INVENTORY.csv", "INVENTORY"),
        ("RECOMMENDATION.csv", "RECOMMENDATION"),
    ]:
        df = pd.read_csv(DATA_DIR / file_name)
        df.to_sql(table_name, engine, if_exists="replace", index=False)


def get_all_tables() -> dict[str, pd.DataFrame]:
    ensure_demo_data()
    engine = get_engine()
    tables = {}
    for table_name in ["PRODUCTS", "CUSTOMERS", "TRANSACTIONS", "INVENTORY", "RECOMMENDATION"]:
        tables[table_name.lower()] = pd.read_sql_table(table_name, engine)
    return tables


def reset_demo_data() -> None:
    db_path = Path(get_database_url().replace("sqlite:///", "", 1))
    if db_path.exists():
        db_path.unlink()
    if DATA_DIR.exists():
        for file in DATA_DIR.glob("*.csv"):
            file.unlink()
    generate_demo_datasets(DATA_DIR)
    ensure_demo_data()
