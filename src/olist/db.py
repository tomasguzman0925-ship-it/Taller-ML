"""Acceso a la base olist.duckdb siguiendo las reglas del taller.

Reglas (sección 2.1 del enunciado):
- Toda la lectura de datos se hace con SQL sobre olist.duckdb (nunca CSV crudos).
- La conexión se abre en modo solo lectura.
- Las fechas de corte se pasan como parámetros ``?``, no con f-strings.
- Las consultas principales viven en archivos .sql dentro de ``sql/``.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import duckdb
import pandas as pd

from olist.config import DB_PATH, SQL_DIR


def conectar(ruta: Path | str = DB_PATH) -> duckdb.DuckDBPyConnection:
    """Abre la base en modo solo lectura.

    Si necesita tablas intermedias, cree vistas temporales sobre esta conexión
    (``CREATE TEMP VIEW ...``) o use una base aparte; la base cruda no se modifica.
    """
    ruta = Path(ruta)
    if not ruta.exists():
        raise FileNotFoundError(
            f"No existe {ruta}. Constrúyala primero con:\n"
            "  uv run python scripts/build_olist_duckdb.py --out data/olist.duckdb"
        )
    return duckdb.connect(str(ruta), read_only=True)


def leer_sql(nombre: str) -> str:
    """Lee un archivo de ``sql/``. Ejemplo: ``leer_sql("B_series/serie_diaria.sql")``."""
    ruta = SQL_DIR / nombre
    if ruta.suffix != ".sql":
        ruta = ruta.with_suffix(".sql")
    return ruta.read_text(encoding="utf-8")


def consulta(
    con: duckdb.DuckDBPyConnection,
    sql_o_archivo: str,
    params: Sequence | None = None,
) -> pd.DataFrame:
    """Ejecuta una consulta y devuelve un DataFrame.

    ``sql_o_archivo`` puede ser texto SQL o el nombre de un archivo en ``sql/``
    (si termina en ``.sql``). Los parámetros se pasan en ``params`` y se enlazan
    a los ``?`` de la consulta en orden.
    """
    texto = leer_sql(sql_o_archivo) if sql_o_archivo.endswith(".sql") else sql_o_archivo
    return con.execute(texto, list(params) if params else None).df()
