#!/usr/bin/env python3
"""Gera as figuras de exemplo dos modelos (PT e EN).

Reproduz `pt/regressao.png` e `en/regression.png`: uma dispersão de pontos com a
reta ajustada por mínimos quadrados ordinários (a mesma derivada nos exemplos).

Requisitos: Python 3 com numpy e matplotlib.
Uso (a partir da raiz do repositório):  python3 tools/make_figures.py
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent


def fit_and_plot(label_points: str, out_path: Path) -> None:
    rng = np.random.default_rng(42)  # semente fixa => figura reproduzível
    n = 60
    x = rng.uniform(0, 10, n)
    y = 2.0 + 0.8 * x + rng.normal(0, 1.2, n)

    # OLS pela forma fechada: beta = (X'X)^{-1} X'y
    X = np.column_stack([np.ones(n), x])
    beta = np.linalg.inv(X.T @ X) @ X.T @ y
    xs = np.linspace(0, 10, 100)
    ys = beta[0] + beta[1] * xs

    plt.rcParams.update({"font.family": "serif", "font.size": 12, "figure.dpi": 200})
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(x, y, facecolors="none", edgecolors="black", s=36,
               linewidths=0.9, label=label_points)
    ax.plot(xs, ys, color="black", linewidth=1.8,
            label=fr"$\hat{{y}} = {beta[0]:.2f} + {beta[1]:.2f}\,x$")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.legend(frameon=False, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"escrito: {out_path.relative_to(ROOT)}  (beta = {beta.round(4).tolist()})")


if __name__ == "__main__":
    fit_and_plot("Observações", ROOT / "pt" / "regressao.png")
    fit_and_plot("Observations", ROOT / "en" / "regression.png")
