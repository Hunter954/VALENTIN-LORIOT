"""Pequeno "auto-migrate" para SQLite.

Objetivo: permitir atualizar o código sem perder uploads já existentes.
- db.create_all() cria tabelas novas.
- Para colunas novas em tabelas existentes, fazemos ALTER TABLE ADD COLUMN.

Isso é intencionalmente simples (sem Alembic) e cobre o que este projeto usa.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

from sqlalchemy import text

from . import db


def _get_columns(table_name: str) -> List[str]:
    rows = db.session.execute(text(f"PRAGMA table_info({table_name});")).fetchall()
    return [r[1] for r in rows]  # name


def _table_exists(table_name: str) -> bool:
    row = db.session.execute(
        text("SELECT name FROM sqlite_master WHERE type='table' AND name=:n"),
        {"n": table_name},
    ).fetchone()
    return row is not None


def _add_column(table: str, col_name: str, col_sql: str) -> None:
    db.session.execute(text(f"ALTER TABLE {table} ADD COLUMN {col_name} {col_sql};"))


def ensure_schema() -> None:
    """Garante que o schema tenha as colunas/tabelas novas."""

    # Tabelas novas (create_all já cria, mas deixamos aqui como documentação)
    # - showreel
    # - instagram_photos
    # - social_links

    # Colunas novas em tabelas existentes
    alterations: Dict[str, List[Tuple[str, str]]] = {
        "site_settings": [
            ("brand_logo_path", "VARCHAR(255) DEFAULT ''"),
            ("footer_about", "TEXT DEFAULT ''"),
            ("footer_phone", "VARCHAR(120) DEFAULT ''"),
            ("footer_email", "VARCHAR(120) DEFAULT ''"),
            ("footer_copyright", "VARCHAR(180) DEFAULT ''"),
        ],
        "hero_videos": [
            ("overlay_top", "VARCHAR(120) DEFAULT ''"),
            ("overlay_title", "VARCHAR(120) DEFAULT ''"),
        ],
    }

    for table, cols in alterations.items():
        if not _table_exists(table):
            continue
        existing = set(_get_columns(table))
        for col_name, col_sql in cols:
            if col_name not in existing:
                _add_column(table, col_name, col_sql)

    db.session.commit()
