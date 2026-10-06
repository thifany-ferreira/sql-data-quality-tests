"""Monta o banco SQLite em memória a partir dos arquivos .sql."""

import sqlite3
from pathlib import Path

SQL_DIR = Path(__file__).resolve().parent.parent / "sql"

DATASETS = {
    "limpos": SQL_DIR / "dados_limpos.sql",
    "defeitos": SQL_DIR / "dados_com_defeitos.sql",
}


def connect(dataset: str = "limpos") -> sqlite3.Connection:
    """Cria um banco novo com a estrutura e os dados escolhidos."""
    if dataset not in DATASETS:
        raise ValueError(f"Conjunto de dados desconhecido: {dataset}. Opções: {', '.join(DATASETS)}")
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript((SQL_DIR / "schema.sql").read_text(encoding="utf-8"))
    conn.executescript(DATASETS[dataset].read_text(encoding="utf-8"))
    return conn
