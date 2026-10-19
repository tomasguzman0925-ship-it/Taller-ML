"""Estilo común de gráficos y guardado de figuras para el informe."""

from __future__ import annotations

import matplotlib.pyplot as plt
import seaborn as sns

from olist.config import FIG_DIR


def estilo() -> None:
    """Aplica un estilo uniforme a todas las figuras del proyecto."""
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams.update({"figure.figsize": (11, 4), "figure.dpi": 110, "axes.titleweight": "bold"})


def guardar(fig, nombre: str, modulo: str) -> None:
    """Guarda la figura en ``reports/figures/<modulo>/<nombre>.png`` para el informe."""
    destino = FIG_DIR / modulo
    destino.mkdir(parents=True, exist_ok=True)
    fig.savefig(destino / f"{nombre}.png", bbox_inches="tight", dpi=150)
