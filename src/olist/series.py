"""Herramientas reutilizables para el Módulo B (series de tiempo) y el Módulo D.

Incluye: partición prueba / walk-forward, baselines, variables de calendario y
rezagos sin fuga, pronóstico recursivo multi-paso y métricas por horizonte.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass

import holidays
import numpy as np
import pandas as pd

from olist.config import ESTACIONALIDAD, HORIZONTE, SEMANAS_PRUEBA

# ---------------------------------------------------------------------------------
# Partición
# ---------------------------------------------------------------------------------


def separar_prueba(y: pd.Series, semanas: int = SEMANAS_PRUEBA) -> tuple[pd.Series, pd.Series]:
    """Separa las últimas ``semanas`` como prueba (se usa una sola vez al final)."""
    corte = len(y) - semanas * 7
    return y.iloc[:corte], y.iloc[corte:]


@dataclass
class Pliegue:
    """Un pliegue de walk-forward: entrenar con ``entrenamiento`` y evaluar en ``validacion``."""

    numero: int
    origen: pd.Timestamp  # último día observado
    entrenamiento: pd.Series
    validacion: pd.Series


def walk_forward(
    y: pd.Series,
    n_pliegues: int = 6,
    horizonte: int = HORIZONTE,
    paso: int = 7,
    min_entrenamiento: int = 180,
) -> Iterator[Pliegue]:
    """Validación con origen móvil (ventana expansiva) sobre ``y`` (sin la prueba).

    Los orígenes se ubican hacia el final de la serie, separados ``paso`` días, y cada
    pliegue evalúa los ``horizonte`` días siguientes al origen.
    """
    n = len(y)
    ultimo_inicio_val = n - horizonte
    inicios = [ultimo_inicio_val - paso * k for k in range(n_pliegues)][::-1]
    for i, inicio in enumerate(inicios):
        if inicio < min_entrenamiento:
            continue
        yield Pliegue(
            numero=i,
            origen=y.index[inicio - 1],
            entrenamiento=y.iloc[:inicio],
            validacion=y.iloc[inicio : inicio + horizonte],
        )


# ---------------------------------------------------------------------------------
# Baselines
# ---------------------------------------------------------------------------------


def pronostico_ingenuo(historia: pd.Series, horizonte: int = HORIZONTE) -> pd.Series:
    """Repite el último valor observado."""
    fechas = _fechas_futuras(historia, horizonte)
    return pd.Series(historia.iloc[-1], index=fechas, name="ingenuo")


def pronostico_ingenuo_estacional(
    historia: pd.Series, horizonte: int = HORIZONTE, m: int = ESTACIONALIDAD
) -> pd.Series:
    """Mismo día de la semana anterior: repite el último ciclo de ``m`` días."""
    fechas = _fechas_futuras(historia, horizonte)
    ultimo_ciclo = historia.iloc[-m:].to_numpy()
    valores = np.resize(ultimo_ciclo, horizonte)
    return pd.Series(valores, index=fechas, name="ingenuo_estacional")


def _fechas_futuras(historia: pd.Series, horizonte: int) -> pd.DatetimeIndex:
    return pd.date_range(historia.index[-1] + pd.Timedelta(days=1), periods=horizonte, freq="D")


# ---------------------------------------------------------------------------------
# Variables (sin mirar al futuro)
# ---------------------------------------------------------------------------------


def black_friday(anio: int) -> pd.Timestamp:
    """Cuarto viernes de noviembre (también aplica a Brasil)."""
    noviembre = pd.date_range(f"{anio}-11-01", f"{anio}-11-30", freq="D")
    return noviembre[noviembre.dayofweek == 4][3]


def variables_calendario(fechas: pd.DatetimeIndex) -> pd.DataFrame:
    """Variables conocidas de antemano para cualquier fecha (no generan fuga)."""
    festivos = holidays.country_holidays("BR", years=sorted(set(fechas.year)))
    bf = {a: black_friday(a) for a in set(fechas.year)}
    df = pd.DataFrame(index=fechas)
    df["dia_semana"] = fechas.dayofweek
    df["dia_mes"] = fechas.day
    df["mes"] = fechas.month
    df["semana_anio"] = fechas.isocalendar().week.astype(int).to_numpy()
    df["fin_de_semana"] = (fechas.dayofweek >= 5).astype(int)
    df["festivo"] = [int(f in festivos) for f in fechas]
    df["dias_a_black_friday"] = [(bf[f.year] - f).days for f in fechas]
    df["semana_black_friday"] = df["dias_a_black_friday"].between(-3, 3).astype(int)
    return df


def variables_rezagos(
    y: pd.Series,
    rezagos: tuple[int, ...] = (1, 2, 3, 7, 14, 21, 28),
    ventanas: tuple[int, ...] = (7, 14, 28),
) -> pd.DataFrame:
    """Rezagos y medias móviles calculados solo con valores anteriores a cada fecha.

    Las medias móviles usan ``shift(1)`` para que el valor del día t nunca entre en
    sus propias variables.
    """
    df = pd.DataFrame(index=y.index)
    for k in rezagos:
        df[f"lag_{k}"] = y.shift(k)
    pasado = y.shift(1)
    for w in ventanas:
        df[f"media_{w}"] = pasado.rolling(w).mean()
        df[f"desv_{w}"] = pasado.rolling(w).std()
    return df


def matriz_supervisada(y: pd.Series, **kwargs) -> tuple[pd.DataFrame, pd.Series]:
    """Une rezagos + calendario y elimina las filas iniciales sin historia suficiente."""
    X = variables_rezagos(y, **kwargs).join(variables_calendario(y.index))
    validas = X.notna().all(axis=1)
    return X[validas], y[validas]


PARAMETROS_LGBM = {
    "n_estimators": 400,
    "learning_rate": 0.03,
    "num_leaves": 15,
    "min_child_samples": 10,
    "subsample": 0.8,
    "subsample_freq": 1,
    "colsample_bytree": 0.8,
    "verbose": -1,
}


def entrenar_lightgbm(y: pd.Series, random_state: int = 42, **params):
    """Entrena el LightGBM base sobre la matriz de rezagos + calendario de ``y``.

    Es el modelo que comparten el Módulo B (pronóstico) y el Módulo D (SHAP).
    TODO (Módulo B): ajustar hiperparámetros con walk-forward u Optuna.
    """
    from lightgbm import LGBMRegressor

    X, objetivo = matriz_supervisada(y)
    modelo = LGBMRegressor(**{**PARAMETROS_LGBM, **params}, random_state=random_state)
    modelo.fit(X, objetivo)
    return modelo


def pronostico_recursivo(
    modelo,
    historia: pd.Series,
    horizonte: int = HORIZONTE,
    construir_X: Callable[[pd.Series], pd.DataFrame] | None = None,
) -> pd.Series:
    """Estrategia multi-paso recursiva: cada predicción se usa como rezago de la siguiente.

    ``modelo`` debe tener ``predict`` y haberse entrenado con ``construir_X`` (por
    defecto ``matriz_supervisada``) sobre la misma clase de serie.
    """
    construir_X = construir_X or (lambda s: matriz_supervisada(s)[0])
    serie = historia.copy()
    for fecha in _fechas_futuras(historia, horizonte):
        serie.loc[fecha] = np.nan
        X = construir_X(serie.ffill()).loc[[fecha]]
        serie.loc[fecha] = float(modelo.predict(X)[0])
    return serie.iloc[len(historia) :].rename("recursivo")


# ---------------------------------------------------------------------------------
# Métricas
# ---------------------------------------------------------------------------------


def smape(y: np.ndarray, yhat: np.ndarray) -> float:
    """sMAPE en porcentaje (robusto a días con pocas órdenes, a diferencia del MAPE)."""
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    denom = (np.abs(y) + np.abs(yhat)) / 2
    return float(np.mean(np.where(denom == 0, 0, np.abs(y - yhat) / denom)) * 100)


def metricas(y, yhat) -> dict[str, float]:
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    return {
        "MAE": float(np.mean(np.abs(y - yhat))),
        "RMSE": float(np.sqrt(np.mean((y - yhat) ** 2))),
        "sMAPE": smape(y, yhat),
    }


def metricas_por_horizonte(resultados: pd.DataFrame) -> pd.DataFrame:
    """Métricas por paso adelante.

    ``resultados`` necesita columnas: ``modelo``, ``origen``, ``h`` (1..horizonte),
    ``y`` y ``yhat``. Devuelve una fila por (modelo, h).
    """
    return (
        resultados.groupby(["modelo", "h"])
        .apply(lambda g: pd.Series(metricas(g["y"], g["yhat"])), include_groups=False)
        .reset_index()
    )


def cobertura_empirica(y, inferior, superior) -> float:
    """Proporción de observaciones dentro del intervalo de predicción."""
    y = np.asarray(y, float)
    return float(np.mean((y >= np.asarray(inferior)) & (y <= np.asarray(superior))))


def a_formato_largo(modelo: str, origen, real: pd.Series, pred: pd.Series) -> pd.DataFrame:
    """Convierte un pronóstico de un pliegue al formato que usa ``metricas_por_horizonte``."""
    return pd.DataFrame(
        {
            "modelo": modelo,
            "origen": origen,
            "fecha": real.index,
            "h": np.arange(1, len(real) + 1),
            "y": real.to_numpy(),
            "yhat": pred.reindex(real.index).to_numpy(),
        }
    )
