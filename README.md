# Taller ML 2026-2: Olist (Módulos 0, B y D)

Aprendizaje Automático, MCDA 2026-2 (Prof. Andrés Vásquez Restrepo).
Taller grupal sobre el *Brazilian E-Commerce Public Dataset by Olist*, con todos los datos leídos vía **SQL sobre DuckDB**.

| Módulo | Pregunta | Notebook | SQL |
|---|---|---|---|
| **0**: Datos, calidad y EDA | ¿Qué datos tenemos y qué período sirve? | `notebooks/00_datos.ipynb` | `sql/00_datos/` |
| **B**: Series de tiempo | ¿Cuántas órdenes recibiremos cada día en las próximas 4 semanas? | `notebooks/B_series.ipynb` | `sql/B_series/` |
| **D**: Interpretabilidad e integración | ¿Por qué pronostica eso el modelo y cómo se usaría? | `notebooks/D_integracion.ipynb` | `sql/D_integracion/` |

> **Alcance del Módulo D.** El enunciado plantea SHAP sobre el Módulo A (clasificación). Como el
> equipo no desarrolla A, el Módulo D se adapta al **modelo de ML del Módulo B** (LightGBM con
> rezagos, medias móviles y calendario). Ver la sección [Módulo D adaptado](#módulo-d-adaptado-a-series-de-tiempo).

---

## 1. Puesta en marcha (una sola vez por integrante)

### 1.1 Instalar uv

uv gestiona Python y las dependencias; no hace falta instalar Python aparte.

- **Windows (PowerShell):** `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **macOS / Linux:** `curl -LsSf https://astral.sh/uv/install.sh | sh`

Cierre y vuelva a abrir la terminal.

### 1.2 Clonar e instalar el entorno

```bash
git clone <URL-DEL-REPOSITORIO>
cd olist-taller-ml
uv sync                       # crea .venv con Python 3.12 y todas las librerías (uv.lock)
uv run nbstripout --install   # limpia las salidas de los notebooks al hacer commit
```

Alternativa sin uv: `python -m venv .venv`, activarlo, y `pip install -r requirements.txt && pip install -e .`

> **Windows:** clonen el repositorio en una ruta corta (p. ej. `Documents\olist-taller-ml`).
> Con rutas muy largas Windows trunca archivos al instalar paquetes.
> `lightgbm` está fijado en `<4.7` porque la versión 4.7.0 falla con *access violation* en Windows al entrenar.

### 1.5 Orden de ejecución

`00_datos` → `B_series` → `D_integracion`. B guarda el modelo en `models/lightgbm_series.joblib`, que
D carga. Si no existe, D lo entrena con la misma función. Las fechas del período útil viven en
`src/olist/config.py` (valores provisionales: 2017-01-05 a 2018-08-19). El Módulo 0 debe justificarlas.

### 1.3 Construir la base de datos

La base **no** está en el repositorio (no se entrega; el calificador la reconstruye).

```bash
uv run python scripts/build_olist_duckdb.py --out data/olist.duckdb
```

- `scripts/build_olist_duckdb.py` es una **copia exacta** del script oficial del curso
  (`homeworks/taller/build_olist_duckdb.py`), el mismo con el que el calificador reconstruye la base. No lo modifiquen.
- Descarga el dataset con `kagglehub`. Si Kaggle pide autenticación, cree un token en
  *kaggle.com → Settings → API → Create New Token* y guarde `kaggle.json` en `~/.kaggle/`
  (nunca en el repositorio).

Tablas resultantes: `orders`, `order_items`, `order_payments`, `order_reviews`, `customers`,
`sellers`, `products`, `geolocation`, `category_translation`.

### 1.4 Abrir los notebooks

```bash
uv run jupyter lab
```

En VS Code: abrir el notebook y elegir el kernel `.venv` del proyecto.

---

## 2. Estructura del repositorio

```
├── data/                      # olist.duckdb (ignorado por git)
├── notebooks/
│   ├── 00_datos.ipynb         # Módulo 0
│   ├── B_series.ipynb         # Módulo B
│   └── D_integracion.ipynb    # Módulo D
├── sql/
│   ├── 00_datos/              # llaves, cardinalidad, calidad, cobertura, EDA
│   ├── B_series/              # serie diaria (con días sin órdenes)
│   └── D_integracion/         # demanda por estado / categoría, carga logística
├── src/olist/                 # código reutilizable (importable desde los notebooks)
│   ├── config.py              # rutas, semilla, período útil, horizonte
│   ├── db.py                  # conexión solo lectura + lectura de .sql con parámetros
│   ├── series.py              # walk-forward, baselines, rezagos, métricas, cobertura
│   └── graficos.py            # estilo y guardado de figuras
├── scripts/build_olist_duckdb.py
├── reports/
│   ├── figures/               # figuras exportadas para el informe
│   └── informe/               # informe PDF (máx. 20 páginas)
├── models/                    # modelos entrenados (ignorados por git)
├── tests/                     # pruebas rápidas de las utilidades
├── pyproject.toml / uv.lock   # versiones declaradas
└── requirements.txt           # exportado de uv.lock para quien no use uv
```

## 3. Reglas del taller que el entorno ya aplica

| Regla del enunciado | Cómo se cumple aquí |
|---|---|
| Toda la lectura es SQL sobre `olist.duckdb` | `olist.conectar()` + `olist.consulta(con, "carpeta/archivo.sql", params)`. **Prohibido** `pd.read_csv` en notebooks. |
| Conexión en solo lectura | `conectar()` usa `read_only=True`. Tablas intermedias: `CREATE TEMP VIEW`. |
| Cruces, filtros y agregados en SQL | Pandas solo a partir del resultado de la consulta. |
| Fechas de corte como parámetro `?` | Los `.sql` usan `?`; las fechas vienen de `olist.config`. |
| Consultas principales en `sql/` y leídas desde los notebooks | `consulta()` acepta el nombre del archivo `.sql`. |
| Reproducibilidad | `RANDOM_STATE = 42`, `uv.lock` + `requirements.txt`, rutas relativas (`config.py`). |
| Celdas en orden y sin errores | Antes de entregar: `uv run jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb` |
| Código comentado en español | Convención del equipo. |

Ejemplo:

```python
from olist import conectar, consulta
from olist.config import FECHA_INICIO_UTIL, FECHA_FIN_UTIL

con = conectar()
serie = consulta(con, "B_series/serie_diaria.sql", [FECHA_INICIO_UTIL, FECHA_FIN_UTIL])
```

## 4. Qué pide cada módulo (checklist)

### Módulo 0: Datos, calidad y EDA (15 %)
- [ ] Unicidad de llaves y cardinalidad de relaciones (1:1, 1:N); qué uniones multiplican filas y cómo evitarlo.
- [ ] Calidad: faltantes, fechas inconsistentes, órdenes sin ítems, pagos ≠ precio + flete, prefijos sin geolocalización, categorías sin traducción.
- [ ] `customer_id` vs `customer_unique_id` y sus consecuencias.
- [ ] Cobertura temporal: definir y justificar el **período útil** → actualizar `src/olist/config.py`.
- [ ] EDA: tiempos de entrega y retraso, órdenes por día/semana, geografía de clientes y vendedores, compras por cliente.

### Módulo B: Series de tiempo (15 %)
- [ ] Serie diaria en SQL **incluyendo días sin órdenes** (`sql/B_series/serie_diaria.sql`).
- [ ] Prueba = últimas 8 semanas del período útil; validación walk-forward (horizonte 28 días).
- [ ] Análisis: tendencia, estacionalidad semanal, ACF/PACF, ADF/KPSS, descomposición, atípicos (Black Friday 2017, festivos, paros): modelar, marcar o excluir.
- [ ] Baselines: ingenuo e ingenuo estacional.
- [ ] Modelos: ≥1 estadístico (ETS / SARIMA / SARIMAX) y ≥1 ML (LightGBM con rezagos, medias móviles, calendario). Explicar estrategia multi-paso.
- [ ] Métricas MAE, RMSE, sMAPE **por horizonte** vs baselines.
- [ ] Intervalos de predicción y cobertura empírica.
- [ ] *(Opcional)* top-5 categorías o estado de São Paulo.

### Módulo D adaptado a series de tiempo
- [ ] **SHAP sobre el LightGBM del Módulo B:** importancia global (beeswarm), dependencia de las 3 variables más relevantes, explicación local de **un día bien pronosticado** y de **un día con gran error** (el análogo del falso negativo, p. ej. Black Friday o un festivo). Contraste con importancia por permutación.
- [ ] **Integración** con el Módulo 0 / B (al menos una):
  - (i) Plan de capacidad: convertir el pronóstico diario en carga semanal por estado de origen de los vendedores (participaciones históricas en SQL).
  - (ii) Demanda por estado o categoría: ¿el modelo global sirve para SP o para las top-5 categorías?
  - (iii) ¿Mejora el pronóstico al agregar variables de los datos (precio medio, flete, mezcla de categorías rezagados)?
- [ ] **Caso de uso:** cómo se operaría (plan semanal de capacidad, alertas de picos) y limitaciones: deriva temporal, censura al cierre del dataset, sesgos de cobertura geográfica.

> Confirmen con el profesor que esta adaptación del Módulo D es válida.

## 5. Flujo de trabajo en equipo (git)

1. `git pull` antes de empezar.
2. Una rama por tarea: `git checkout -b modulo-b/sarima`.
3. Commits pequeños y en español: `git commit -m "B: walk-forward con SARIMA"`.
4. `git push -u origin modulo-b/sarima` y abrir un Pull Request hacia `main`; otro integrante revisa.
5. **Evitar conflictos en notebooks:** cada notebook tiene un responsable; el código común va en
   `src/olist/` (archivos .py que git sí combina bien). `nbstripout` evita que las salidas generen conflictos.

## 6. Entregables

- Informe PDF (≤ 20 páginas): resumen ejecutivo, datos y calidad, capítulo por módulo, interpretabilidad/integración/caso de uso, limitaciones.
- Notebooks (`.ipynb`) + consultas `.sql`.
- **No** entregar `olist.duckdb`.
- Fecha: sábado 17 de octubre de 2026, 11:59 p. m., vía Interactiva.
