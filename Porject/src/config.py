from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "retail_bi.db"


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")
