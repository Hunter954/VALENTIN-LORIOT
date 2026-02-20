"""app/schema.py

A função ensure_schema existia para compatibilidade com SQLite (usando sqlite_master),
mas isso quebra em Postgres.

Esta implementação usa o inspector do SQLAlchemy (compatível com Postgres/SQLite) e é segura.
Se você precisar aplicar ALTER TABLE/novas colunas, coloque as regras em `SCHEMA_UPDATES`.
"""

from __future__ import annotations

from sqlalchemy import text, inspect
from . import db


# Exemplo de estrutura para evoluções manuais de schema (opcional):
# SCHEMA_UPDATES = [
#   {
#     "table": "site_setting",
#     "columns": [
#       ("new_col", "TEXT", "DEFAULT ''"),
#     ]
#   }
# ]
SCHEMA_UPDATES: list[dict] = []


def _has_table(table_name: str) -> bool:
    inspector = inspect(db.engine)
    return inspector.has_table(table_name)


def _has_column(table_name: str, column_name: str) -> bool:
    inspector = inspect(db.engine)
    cols = inspector.get_columns(table_name)
    return any(c.get("name") == column_name for c in cols)


def ensure_schema() -> None:
    """Aplica pequenas evoluções de schema de forma idempotente.

    Se você usa Alembic/Flask-Migrate, pode deixar SCHEMA_UPDATES vazio.
    """
    if not SCHEMA_UPDATES:
        return

    for upd in SCHEMA_UPDATES:
        table = upd.get("table")
        columns = upd.get("columns", [])
        if not table or not columns:
            continue

        if not _has_table(table):
            continue

        for col_name, col_type, *rest in columns:
            if _has_column(table, col_name):
                continue
            extra = rest[0] if rest else ""
            stmt = f'ALTER TABLE "{table}" ADD COLUMN "{col_name}" {col_type} {extra}'.strip()
            db.session.execute(text(stmt))
    db.session.commit()
