"""Pruebas rápidas de las utilidades de series (no requieren la base de datos)."""

import numpy as np
import pandas as pd

from olist import series as ts


def _serie(n=300):
    fechas = pd.date_range("2017-01-01", periods=n, freq="D")
    return pd.Series(100 + 10 * np.sin(2 * np.pi * np.arange(n) / 7), index=fechas)


def test_rezagos_sin_fuga():
    y = _serie()
    X = ts.variables_rezagos(y)
    # el rezago 1 del día t es el valor de t-1, y la media de 7 no incluye el día t
    assert X["lag_1"].iloc[10] == y.iloc[9]
    assert np.isclose(X["media_7"].iloc[10], y.iloc[3:10].mean())


def test_walk_forward_no_solapa_validacion_con_entrenamiento():
    y = _serie()
    for p in ts.walk_forward(y, n_pliegues=4, horizonte=28):
        assert p.entrenamiento.index.max() < p.validacion.index.min()
        assert len(p.validacion) == 28


def test_ingenuo_estacional_repite_ultima_semana():
    y = _serie()
    pred = ts.pronostico_ingenuo_estacional(y, horizonte=14)
    assert np.allclose(pred.iloc[:7].to_numpy(), y.iloc[-7:].to_numpy())


def test_black_friday_2017():
    assert ts.black_friday(2017) == pd.Timestamp("2017-11-24")
