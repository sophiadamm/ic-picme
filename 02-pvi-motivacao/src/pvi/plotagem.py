
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
    #fig.savefig(base.with_suffix(".pdf"))
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
        if n > 120:
            markevery = max(1, n // 30)
            ax.plot(t, U, linestyle="--", marker=marc, ms=4.0, lw=1.2,
                    markevery=markevery, label=f"$k = {k}$ ({n} passos)")
        else:
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


def _desenhar_autovalor_global(ax, prob, x_lim_global=(-5.0, 40.0)):
    x_min = np.sqrt(6.0) - 1.0
    lam_min = 4.0 * np.sqrt(6.0) - 10.0
    x_max = -1.0 - np.sqrt(6.0)
    lam_max = -4.0 * np.sqrt(6.0) - 10.0
    lam_zero = 4.0

    x_left = np.linspace(x_lim_global[0], -1.05, 500)
    x_right = np.linspace(-0.95, x_lim_global[1], 1000)
    lam_left = 2.0 * prob.solucao(x_left)
    lam_right = 2.0 * prob.solucao(x_right)

    x_asint = np.linspace(x_lim_global[0], x_lim_global[1], 500)
    lam_asint = 2.0 * x_asint - 8.0

    ax.plot(x_left, lam_left, color="#1f77b4", lw=1.8, label=r"Autovalor $\lambda(x) = 2y(x)$")
    ax.plot(x_right, lam_right, color="#1f77b4", lw=1.8)
    ax.plot(x_asint, lam_asint, color="#2ca02c", linestyle="--", lw=1.5, label=r"Assíntota: $\lambda = 2x - 8$")
    ax.axvline(-1.0, color="#d62728", linestyle="--", lw=1.5, label=r"Assíntota: $x = -1$")

    ax.plot(0.0, lam_zero, "o", color="#9467bd", markersize=6, zorder=5, label=r"No zero: $(0,\, 4)$")
    ax.plot([1.0, 2.0], [0.0, 0.0], "s", color="#ff7f0e", markersize=5, zorder=5, label=r"Raízes $x=1,\, 2$ ($\lambda=0$)")
    ax.plot(x_min, lam_min, "v", color="#d62728", markersize=6, zorder=5, label=rf"Mínimo $(\approx {x_min:.2f},\, {lam_min:.2f})$")
    ax.plot(x_max, lam_max, "^", color="#8c564b", markersize=6, zorder=5, label=rf"Máximo $(\approx {x_max:.2f},\, {lam_max:.2f})$")

    ax.axhline(0, color="gray", lw=0.8, alpha=0.5)
    ax.set_xlim(x_lim_global[0] - 1.0, x_lim_global[1] + 2.0)
    ax.set_ylim(-45.0, 85.0)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$\lambda(x)$")
    ax.set_title(r"Comportamento Global do Autovalor ($x \in [-5,\, 40]$)")
    ax.legend(loc="upper left", fontsize=8.8)


def _desenhar_autovalor_zoom(ax, prob, x_lim_zoom=(-1.5, 5.0)):
    x_min = np.sqrt(6.0) - 1.0
    lam_min = 4.0 * np.sqrt(6.0) - 10.0
    lam_zero = 4.0

    x_left = np.linspace(x_lim_zoom[0], -1.05, 200)
    x_right = np.linspace(-0.95, x_lim_zoom[1], 600)
    lam_left = 2.0 * prob.solucao(x_left)
    lam_right = 2.0 * prob.solucao(x_right)

    x_asint = np.linspace(x_lim_zoom[0], x_lim_zoom[1], 300)
    lam_asint = 2.0 * x_asint - 8.0

    ax.plot(x_left, lam_left, color="#1f77b4", lw=1.8, label=r"Autovalor $\lambda(x)$")
    ax.plot(x_right, lam_right, color="#1f77b4", lw=1.8)
    ax.plot(x_asint, lam_asint, color="#2ca02c", linestyle="--", lw=1.5, label=r"Assíntota: $\lambda = 2x - 8$")
    ax.axvline(-1.0, color="#d62728", linestyle="--", lw=1.5, label=r"Assíntota: $x = -1$")

    ax.plot(0.0, lam_zero, "o", color="#9467bd", markersize=6, zorder=5, label=r"No zero: $(0,\, 4)$")
    ax.annotate(
        r"$\lambda(0) = 4$",
        xy=(0.0, lam_zero),
        xytext=(8, 4),
        textcoords="offset points",
        fontsize=9,
        fontweight="bold",
        color="#4a148c"
    )

    ax.plot([1.0, 2.0], [0.0, 0.0], "s", color="#ff7f0e", markersize=5, zorder=5, label=r"Raízes $x=1,\, 2$")
    ax.plot(x_min, lam_min, "v", color="#d62728", markersize=7, zorder=5, label=rf"Mínimo $(\approx {x_min:.2f},\, {lam_min:.3f})$")
    ax.annotate(
        rf"$\lambda_{{\min}} \approx {lam_min:.3f}$",
        xy=(x_min, lam_min),
        xytext=(-20, -18),
        textcoords="offset points",
        fontsize=9,
        fontweight="bold",
        color="#b71c1c",
        arrowprops=dict(arrowstyle="->", color="#b71c1c", lw=0.9)
    )

    ax.axvspan(0.0, 1.6, color="#17becf", alpha=0.15, label=r"Intervalo $[0,\, 1{,}6]$")

    ax.axhline(0, color="gray", lw=0.8, alpha=0.5)
    ax.set_xlim(x_lim_zoom[0], x_lim_zoom[1])
    ax.set_ylim(-8.0, 16.0)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$\lambda(x)$")
    ax.set_title(r"Detalhe Local do Autovalor ($x \in [-1{,}5,\, 5]$)")
    ax.legend(loc="upper right", fontsize=8.8)


def plot_autovalor_individual(prob, caminho_global, caminho_zoom, x_lim_global=(-5.0, 40.0), x_lim_zoom=(-1.5, 5.0)):
    """Gera as figuras do autovalor individualmente para cada intervalo."""
    fig1, ax1 = plt.subplots(figsize=(6.5, 4.5))
    _desenhar_autovalor_global(ax1, prob, x_lim_global=x_lim_global)
    fig1.tight_layout()
    _salvar(fig1, caminho_global)

    fig2, ax2 = plt.subplots(figsize=(6.5, 4.5))
    _desenhar_autovalor_zoom(ax2, prob, x_lim_zoom=x_lim_zoom)
    fig2.tight_layout()
    _salvar(fig2, caminho_zoom)



def plot_autovalor_assintotas(prob, caminho, x_lim_global=(-5.0, 40.0), x_lim_zoom=(-1.5, 5.0)):
    """Plota o autovalor local lambda(x) = 2 y(x) em dois painéis lado a lado
    (visão global e detalhe local dos experimentos), espelhando plot_solucao_assintotas.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.8))
    _desenhar_autovalor_global(ax1, prob, x_lim_global=x_lim_global)
    _desenhar_autovalor_zoom(ax2, prob, x_lim_zoom=x_lim_zoom)
    fig.tight_layout()
    _salvar(fig, caminho)


def _desenhar_discriminante(ax, prob, ks, tf, g_func, t_ref, cores, mostrar_legenda=True, loc_legenda="lower left", ncol_legenda=2, anotar_falhas=False):
    """Auxiliar para renderizar as curvas do discriminante num determinado eixo."""
    ax.axhspan(-0.25, 0.0, color="#d62728", alpha=0.06, zorder=0)
    ax.axhline(0.0, color="black", linestyle="--", lw=1.1, alpha=0.85, label=r"Limiar crítico $\Delta = 0$")

    for idx, k in enumerate(ks):
        cor = cores[idx % len(cores)]

        # 1. Curva teorica continua baseada na solucao exata y(t)
        t_teor = t_ref[t_ref + k <= tf + 1e-9]
        c_teor = prob.solucao(t_teor) - k * g_func(t_teor + k)
        delta_teor = 1.0 - 4.0 * k * c_teor
        ax.plot(t_teor + k, delta_teor, "-", color=cor, lw=1.5,
                label=f"Exata ($k = {k}$)")

        # 2. Valores reais simulados do Euler Implicito
        n_passos = int(round(tf / k))
        t_num = [prob.t0]
        u_num = [prob.y0]
        deltas_num = []
        t_destinos = []

        for step in range(n_passos):
            tn = t_num[-1]
            un = u_num[-1]
            tn1 = prob.t0 + (step + 1) * k
            c_n = un - k * g_func(tn1)
            delta_n = 1.0 - 4.0 * k * c_n
            deltas_num.append(delta_n)
            t_destinos.append(tn1)

            if delta_n < 0:
                break
            un1 = (1.0 - np.sqrt(delta_n)) / (2.0 * k)
            t_num.append(tn1)
            u_num.append(un1)

        # Melhora na densidade de marcadores: amostra uniforme para evitar sobreposicao excessiva
        n_pts = len(t_destinos)
        markevery = max(1, n_pts // 20)
        ax.plot(t_destinos, deltas_num, "o--", color=cor, ms=3.8, lw=1.2,
                markevery=markevery, alpha=0.85, label=f"Simulada ($k = {k}$)")

        # Destaca o ponto onde o discriminante cruza/fica negativo se houver falha
        if deltas_num[-1] < 0:
            t_f = t_destinos[-1]
            d_f = deltas_num[-1]
            ax.plot(t_f, d_f, "X", color="#8b0000", ms=8.5,
                    markeredgecolor="black", markeredgewidth=0.8, zorder=6,
                    label=f"Falha $\\Delta < 0$ ($k = {k}$)")
            if anotar_falhas:
                offset = (-32, -16) if idx % 2 == 0 else (-48, 12)
                ax.annotate(
                    f"$t = {t_f:.2f}$",
                    xy=(t_f, d_f),
                    xytext=offset,
                    textcoords="offset points",
                    fontsize=8.5,
                    fontweight="bold",
                    color="#8b0000",
                    arrowprops=dict(arrowstyle="->", color="#8b0000", lw=0.8)
                )

    ax.set_xlabel(r"$t_{n+1}$ (instante alvo do passo)")
    ax.set_ylabel(r"Discriminante $\Delta$")
    if mostrar_legenda:
        ax.legend(loc=loc_legenda, fontsize=8.2, ncol=ncol_legenda, framealpha=0.92)


def plot_discriminante_euler(prob, ks, tf, caminho, g_func=None, x_lim_zoom=None, loc_legenda=None, ncol_legenda=None):
    """
    Plota o discriminante Delta = 1 - 4k*c do Euler Implicito:
    1) Delta_teorico(t) = 1 - 4k*(y(t) - k*g(t+k)) ao longo da solucao exata y(t).
    2) Pontos discretos Delta_n com os valores numericos simulados do Euler Implicito.
    Caso x_lim_zoom seja especificado, gera painel duplo (visao global + zoom na regiao critica).
    """
    if g_func is None:
        from pvi.problemas import g as g_func

    cores = ["#d62728", "#1f77b4", "#2ca02c", "#ff7f0e"]
    t_ref = np.linspace(prob.t0, tf, 500)

    if x_lim_zoom is not None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 4.8))

        # Painel 1: Visao global
        loc_leg1 = loc_legenda or "lower left"
        ncol_leg1 = ncol_legenda or 2
        _desenhar_discriminante(ax1, prob, ks, tf, g_func, t_ref, cores,
                                mostrar_legenda=True, loc_legenda=loc_leg1, ncol_legenda=ncol_leg1, anotar_falhas=False)
        ax1.set_xlim(prob.t0 - 0.05, tf + 0.05)
        ax1.set_ylim(-0.18, 1.06)
        ax1.set_title(rf"Visão Global ($t \in [{prob.t0:g},\, {tf:g}]$)")

        # Painel 2: Zoom na regiao critica
        _desenhar_discriminante(ax2, prob, ks, tf, g_func, t_ref, cores,
                                mostrar_legenda=False, anotar_falhas=True)
        ax2.set_xlim(x_lim_zoom[0], x_lim_zoom[1])
        ax2.set_ylim(-0.15, 1.05)
        ax2.set_ylabel("")  # Compartilha visualmente a escala y
        ax2.set_title(rf"Detalhe da Região Crítica ($t \in [{x_lim_zoom[0]:g},\, {x_lim_zoom[1]:g}]$)")

        fig.tight_layout()
        _salvar(fig, caminho)
    else:
        fig, ax = plt.subplots(figsize=(7.5, 4.8))
        if loc_legenda is not None:
            loc_leg = loc_legenda
            ncol_leg = ncol_legenda or 1
        elif tf > 2.0:
            loc_leg = "upper right"
            ncol_leg = 1
        else:
            loc_leg = "lower right"
            ncol_leg = 1
        _desenhar_discriminante(ax, prob, ks, tf, g_func, t_ref, cores,
                                mostrar_legenda=True, loc_legenda=loc_leg, ncol_legenda=ncol_leg, anotar_falhas=False)
        ax.set_xlim(prob.t0, tf)
        ax.set_title("Discriminante do Euler Implícito: Solução Exata vs. Simulação Real")
        fig.tight_layout()
        _salvar(fig, caminho)


def _desenhar_isoclinas(ax, prob, solucoes, ks, tf, g_func, cores,
                        mostrar_legenda=True, loc_legenda="upper left", ncol_legenda=1,
                        destacar_inversao=True, mostrar_campo=True, xlim=None, ylim=None):
    """Auxiliar para desenhar as isóclinas de derivada nula y = +-sqrt(g(t)),
    a regiao de descida (y' < 0), o campo de direcoes e as trajetorias numericas.
    """
    t_fino = np.linspace(prob.t0, tf, 1200)
    g_vals = g_func(t_fino)
    mask_pos = g_vals >= 0.0
    raiz_g = np.sqrt(np.maximum(g_vals, 0.0))

    iso_sup = np.where(mask_pos, raiz_g, np.nan)
    iso_inf = np.where(mask_pos, -raiz_g, np.nan)

    # 1. Campo de direcoes sutil ao fundo
    if mostrar_campo:
        t_min, t_max = xlim if xlim is not None else (prob.t0, tf)
        y_min, y_max = ylim if ylim is not None else (-2.2, 2.3)
        tg = np.linspace(t_min, t_max, 18)
        yg = np.linspace(y_min, y_max, 14)
        TG, YG = np.meshgrid(tg, yg)
        DY = YG**2 - g_func(TG)
        DT = np.ones_like(DY)
        norma = np.hypot(DT, DY)
        ax.quiver(TG, YG, DT / norma, DY / norma, color="gray", alpha=0.22,
                  angles="xy", scale_units="xy", scale=12.0, width=0.003, zorder=0)

    # 2. Sombreado da zona onde y' < 0 (entre -sqrt(g) e +sqrt(g))
    ax.fill_between(t_fino, -raiz_g, raiz_g, where=mask_pos,
                    color="#ff7f0e", alpha=0.13, zorder=1,
                    label=r"Zona de descida ($y' < 0$)")

    # 3. Curvas das isoclinas de derivada nula (y' = 0)
    ax.plot(t_fino, iso_sup, "--", color="#d62728", lw=1.6, zorder=3,
            label=r"Isóclina repulsora $+\sqrt{g(t)}$")
    ax.plot(t_fino, iso_inf, ":", color="#8c564b", lw=1.6, zorder=3,
            label=r"Isóclina atratora $-\sqrt{g(t)}$")

    # 4. Solucao analitica exata
    ax.plot(t_fino, prob.solucao(t_fino), "k-", lw=2.0, zorder=4,
            label=r"Solução exata $y(t)$")

    # 5. Trajetorias numericas
    marcadores = itertools.cycle(MARCADORES_BASE)
    ponto_inversao_rotulado = False

    for idx, ((t, U, _), k, marc) in enumerate(zip(solucoes, ks, marcadores)):
        cor = cores[idx % len(cores)]
        n_pts = len(t)
        markevery = max(1, n_pts // 22)

        ax.plot(t, U, linestyle="-.", marker=marc, color=cor, ms=4.2, lw=1.2,
                markevery=markevery, alpha=0.9, zorder=5,
                label=f"$k = {k}$ ({n_pts - 1} passos)")

        # Detecta o pico local em t > 2.5 (cruzamento com a isoclina +sqrt(g))
        if destacar_inversao and len(t) > 5:
            mask_t = t > 2.5
            if np.any(mask_t):
                indices_t = np.where(mask_t)[0]
                idx_pico = indices_t[np.argmax(U[indices_t])]
                # Se não for o último ponto (ou seja, realmente virou para baixo)
                if idx_pico < len(t) - 1 and U[idx_pico] > U[-1]:
                    lbl_inv = r"Inversão ($U_n \approx +\sqrt{g}$)" if not ponto_inversao_rotulado else None
                    ax.plot(t[idx_pico], U[idx_pico], "D", color="#ffd700",
                            markeredgecolor="black", markeredgewidth=0.9, ms=6.8,
                            zorder=7, label=lbl_inv)
                    ponto_inversao_rotulado = True

    ax.axhline(0.0, color="gray", lw=0.8, alpha=0.5)
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$y$")
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)
    if mostrar_legenda:
        ax.legend(loc=loc_legenda, fontsize=8.0, ncol=ncol_legenda, framealpha=0.92)


def plot_isoclinas(prob, solucoes_ou_metodo, ks, tf, caminho, titulo="Análise de Isóclinas e Bifurcação",
                   g_func=None, x_lim_zoom=None, ylim=(-2.1, 2.3), ylim_zoom=(-1.9, 2.1)):
    """
    Plota as isóclinas de derivada nula y = +-sqrt(g(t)), a região onde f(t, y) < 0,
    a solução exata e as trajetórias numéricas para explicar a reversão de derivada.
    
    Pode ser reutilizada para qualquer método:
    - 'solucoes_ou_metodo' pode ser uma lista de soluções [(t, U, stats), ...] já calculadas,
      OU diretamente a função do método numérico (ex: euler_explicito, rk4, adams_moulton).
    - Se 'x_lim_zoom' for fornecido (ex: (3.2, 5.0)), gera painel duplo (Visão Global + Detalhe).
    """
    if g_func is None:
        from pvi.problemas import g as g_func

    if callable(solucoes_ou_metodo):
        from pvi.uteis import resolver
        solucoes = [resolver(solucoes_ou_metodo, prob, k, tf) for k in ks]
    else:
        solucoes = solucoes_ou_metodo

    cores = ["#1f77b4", "#2ca02c", "#9467bd", "#ff7f0e", "#17becf"]

    if x_lim_zoom is not None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.2, 4.9))

        # Painel 1: Visao Global
        _desenhar_isoclinas(ax1, prob, solucoes, ks, tf, g_func, cores,
                            mostrar_legenda=True, loc_legenda="lower left", ncol_legenda=2,
                            destacar_inversao=True, mostrar_campo=True,
                            xlim=(prob.t0, tf), ylim=ylim)
        ax1.set_title(rf"{titulo} — Visão Global ($t \in [{prob.t0:g},\, {tf:g}]$)")

        # Painel 2: Zoom na bifurcacao / cruzamento da isoclina
        _desenhar_isoclinas(ax2, prob, solucoes, ks, tf, g_func, cores,
                            mostrar_legenda=False, destacar_inversao=True, mostrar_campo=True,
                            xlim=x_lim_zoom, ylim=ylim_zoom)
        ax2.set_ylabel("")
        ax2.set_title(rf"Detalhe do Cruzamento da Isóclina ($t \in [{x_lim_zoom[0]:g},\, {x_lim_zoom[1]:g}]$)")

        fig.tight_layout()
        _salvar(fig, caminho)
    else:
        fig, ax = plt.subplots(figsize=(7.8, 4.9))
        _desenhar_isoclinas(ax, prob, solucoes, ks, tf, g_func, cores,
                            mostrar_legenda=True, loc_legenda="lower left", ncol_legenda=2,
                            destacar_inversao=True, mostrar_campo=True,
                            xlim=(prob.t0, tf), ylim=ylim)
        ax.set_title(titulo)
        fig.tight_layout()
        _salvar(fig, caminho)





