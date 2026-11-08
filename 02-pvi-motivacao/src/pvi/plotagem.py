
import itertools
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Lista base de marcadores (suporta quantidade infinita através de ciclo)
MARCADORES_BASE = ["o", "s", "^", "D", "v", "p", "P", "X"]

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

    n_ks = len(ks)
    # Interpola os tamanhos linearmente: começa em 5.5 (menor que os antigos 7.0) e vai até 1.5
    tamanhos = np.linspace(5.5, 1.5, n_ks) if n_ks > 1 else [4.5]
    
    # Cria um iterador que repete os marcadores caso existam mais de 8 passos
    marcadores = itertools.cycle(MARCADORES_BASE)

    for (t, U, _), k, tam, marc in zip(solucoes, ks, tamanhos, marcadores):
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


def plot_solucao_assintotas(prob, caminho, x_lim_global=(-5.0, 40.0), x_lim_zoom=(-1.5, 5.0)):
    """Plota a solução analítica exata evidenciando as assíntotas e os regimes assintóticos.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.8))

    # --- Painel 1: Visão Global [-5, 40] ---
    x_left1 = np.linspace(x_lim_global[0], -1.05, 500)
    x_right1 = np.linspace(-0.95, x_lim_global[1], 1000)
    y_left1 = prob.solucao(x_left1)
    y_right1 = prob.solucao(x_right1)

    x_asint1 = np.linspace(x_lim_global[0], x_lim_global[1], 500)
    y_asint1 = x_asint1 - 4.0

    ax1.plot(x_left1, y_left1, "k-", lw=1.8, label=r"Solução analítica $y(x)$")
    ax1.plot(x_right1, y_right1, "k-", lw=1.8)
    ax1.plot(x_asint1, y_asint1, color="#2ca02c", linestyle="--", lw=1.5, label=r"Assíntota oblíqua: $y = x - 4$")
    ax1.axvline(-1.0, color="#d62728", linestyle="--", lw=1.5, label=r"Assíntota vertical: $x = -1$")
    ax1.plot(0.0, 2.0, "o", color="#1f77b4", markersize=6, zorder=5, label=r"Condição inicial $(0, 2)$")

    ax1.axhline(0, color="gray", lw=0.8, alpha=0.5)
    ax1.set_xlim(x_lim_global[0] - 1.0, x_lim_global[1] + 2.0)
    ax1.set_ylim(-25.0, 45.0)
    ax1.set_xlabel(r"$x$")
    ax1.set_ylabel(r"$y$")
    ax1.set_title(r"Comportamento Global e Assíntotas ($x \in [-5,\, 40]$)")
    ax1.legend(loc="upper left", fontsize=9.5)

    # --- Painel 2: Zoom na Região dos Experimentos Iniciais [-1.5, 5] ---
    x_left2 = np.linspace(x_lim_zoom[0], -1.05, 200)
    x_right2 = np.linspace(-0.95, x_lim_zoom[1], 600)
    y_left2 = prob.solucao(x_left2)
    y_right2 = prob.solucao(x_right2)

    x_asint2 = np.linspace(x_lim_zoom[0], x_lim_zoom[1], 300)
    y_asint2 = x_asint2 - 4.0

    ax2.plot(x_left2, y_left2, "k-", lw=1.8, label=r"Solução $y(x)$")
    ax2.plot(x_right2, y_right2, "k-", lw=1.8)
    ax2.plot(x_asint2, y_asint2, color="#2ca02c", linestyle="--", lw=1.5, label=r"Assíntota: $y = x - 4$")
    ax2.axvline(-1.0, color="#d62728", linestyle="--", lw=1.5, label=r"Assíntota: $x = -1$")

    ax2.plot(0.0, 2.0, "o", color="#1f77b4", markersize=6, zorder=5, label=r"$(0, 2)$ (inicial)")
    ax2.plot([1.0, 2.0], [0.0, 0.0], "s", color="#ff7f0e", markersize=5, zorder=5, label=r"Raízes $x=1, 2$")
    ax2.axvspan(0.0, 1.6, color="#17becf", alpha=0.15, label=r"Intervalo $[0,\, 1{,}6]$")

    ax2.axhline(0, color="gray", lw=0.8, alpha=0.5)
    ax2.set_xlim(x_lim_zoom[0], x_lim_zoom[1])
    ax2.set_ylim(-8.0, 14.0)
    ax2.set_xlabel(r"$x$")
    ax2.set_ylabel(r"$y$")
    ax2.set_title(r"Detalhe Local e Singularidade ($x \in [-1{,}5,\, 5]$)")
    ax2.legend(loc="upper right", fontsize=9.0)

    fig.tight_layout()
    _salvar(fig, caminho)
