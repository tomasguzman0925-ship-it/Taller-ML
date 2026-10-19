"""Utilidades compartidas del taller Olist (Módulos 0, B y D)."""

from olist.config import (
    DB_PATH,
    FIG_DIR,
    MODELS_DIR,
    PROJECT_ROOT,
    RANDOM_STATE,
    SQL_DIR,
)
from olist.db import conectar, consulta, leer_sql

__all__ = [
    "DB_PATH",
    "FIG_DIR",
    "MODELS_DIR",
    "PROJECT_ROOT",
    "RANDOM_STATE",
    "SQL_DIR",
    "conectar",
    "consulta",
    "leer_sql",
]
