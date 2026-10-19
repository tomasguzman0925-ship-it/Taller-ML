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
# TODO (Módulo 0): justificar estas fechas con el análisis de cobertura temporal
# (sql/00_datos/cobertura_mensual.sql). Son valores provisionales:
# - antes del 2017-01-05 casi no hay órdenes (2016 es escaso y 2017-01-01..04 tienen 0);
# - desde el 2018-08-22 las órdenes caen en picada (de ~250 a 4 diarias) por el corte
#   de extracción del dataset, no por la demanda real.
FECHA_INICIO_UTIL = "2017-01-05"
FECHA_FIN_UTIL = "2018-08-20"  # exclusiva: se usan compras con fecha < FECHA_FIN_UTIL

# --- Series de tiempo (Módulo B) -------------------------------------------------
HORIZONTE = 28  # días a pronosticar (4 semanas)
SEMANAS_PRUEBA = 8  # la prueba son las últimas 8 semanas del período útil
ESTACIONALIDAD = 7  # estacionalidad semanal
