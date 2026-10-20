"""Configuración central del proyecto: rutas relativas, semilla y fechas clave.

Todas las decisiones que deben ser comunes entre módulos (período útil, partición
de prueba, horizonte) viven aquí para que los notebooks no las escriban a mano.
"""

from pathlib import Path

# --- Rutas (relativas a la raíz del repositorio) ---------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "olist.duckdb"
SQL_DIR = PROJECT_ROOT / "sql"
FIG_DIR = PROJECT_ROOT / "reports" / "figures"
MODELS_DIR = PROJECT_ROOT / "models"

# --- Reproducibilidad ------------------------------------------------------------
RANDOM_STATE = 42

# --- Período útil (Módulo 0) -----------------------------------------------------
# Incluye los días desde el primer bloque sostenido de órdenes. Se excluye el tramo
# posterior al 2018-08-21: la cobertura cae desde el día 22 y es casi nula al final
# de agosto, señal de extracción incompleta y no de demanda representativa.
FECHA_INICIO_UTIL = "2017-01-05"
FECHA_FIN_UTIL = "2018-08-22"  # exclusiva: incluye compras hasta el 2018-08-21

# --- Series de tiempo (Módulo B) -------------------------------------------------
HORIZONTE = 28  # días a pronosticar (4 semanas)
SEMANAS_PRUEBA = 8  # la prueba son las últimas 8 semanas del período útil
ESTACIONALIDAD = 7  # estacionalidad semanal
