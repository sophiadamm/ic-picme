
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Pontos grandes, médios e pequenos
TAMANHOS = (7.0, 4.5, 2.5)
MARCADORES = ("o", "s", "^")


def configurar_estilo():
    plt.rcParams.update({
        "figure.figsize": (6.5, 4.5),
        "font.size": 11,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "savefig.bbox": "tight",
    })


def _salvar(fig, caminho):
    """Salva em PDF e PNG"""
    base = Path(caminho)
    base.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(base.with_suffix(".pdf"))
    fig.savefig(base.with_suffix(".png"), dpi=200)
    plt.close(fig)


def _desenhar(ax, prob, solucoes, ks, tspan, titulo):
    """Curva solucao + um conjunto de pontos por tamanho de passo."""
    t_fino = np.linspace(tspan[0], tspan[1], 400)
    ax.plot(t_fino, prob.solucao(t_fino), "k-", lw=1.5, label="solução exata")

    for (t, U, _), k, tam, marc in zip(solucoes, ks, TAMANHOS, MARCADORES):
        n = len(t) - 1
        ax.plot(t, U, marc, ms=tam, label=f"$k = {k}$ ({n} passos)")

    ax.axhline(0, color="gray", lw=0.8)
    ax.set_xlabel("$t$")
    ax.set_ylabel("$y$")
    ax.set_title(titulo)
    ax.legend()


def plot_fig122(prob, solucoes, ks, tspan, titulo, caminho):
    """Uma figura no estilo da Fig. 12.2 para um único método."""
    fig, ax = plt.subplots()
    _desenhar(ax, prob, solucoes, ks, tspan, titulo)
    _salvar(fig, caminho)


def plot_comparacao(prob, sol1, sol2, ks, tspan, titulo1, titulo2, caminho):
    """Compara dois métodos numéricos lado a lado, com o mesmo eixo y."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    _desenhar(ax1, prob, sol1, ks, tspan, titulo1)
    _desenhar(ax2, prob, sol2, ks, tspan, titulo2)
    ax2.set_ylabel("")  # O segundo gráfico não precisa de rótulo no eixo Y porque divide com o primeiro
    _salvar(fig, caminho)