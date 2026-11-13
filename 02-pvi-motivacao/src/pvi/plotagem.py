import itertools
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from pvi.uteis import calcular_evolucao_discriminante
# =============================================================================
# 1. CONFIGURAÇÕES GERAIS E DICIONÁRIO DE ESTILOS (MAGIC NUMBERS)
# =============================================================================
MARCADORES_BASE = ["o", "s", "^", "D", "v", "p", "P", "X"]

ESTILO = {
    "exata": {"color": "k", "lw": 1.8, "zorder": 2},
    "assintota_obl": {"color": "#2ca02c", "linestyle": "--", "lw": 1.5},
    "assintota_ver": {"color": "#d62728", "linestyle": "--", "lw": 1.5},
    "cond_inicial": {"color": "#1f77b4", "marker": "o", "markersize": 6, "zorder": 5},
    "raizes": {"color": "#ff7f0e", "marker": "s", "markersize": 5, "zorder": 5},
    "isoclina_rep": {"color": "#d62728", "linestyle": "--", "lw": 1.6, "zorder": 3},
    "isoclina_atr": {"color": "#8c564b", "linestyle": ":", "lw": 1.6, "zorder": 3},
    "zona_descida": {"color": "#ff7f0e", "alpha": 0.13, "zorder": 1},
    "cores_ciclo": ["#1f77b4","#d62728", "#2ca02c", "#ff7f0e", "#9467bd"]
}

def configurar_estilo():
    plt.rcParams.update({
        "figure.figsize": (6.5, 4.5),
        "font.size": 11,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "savefig.bbox": "tight",
    })

def _salvar(fig, caminho):
    base = Path(caminho)
    base.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(base.with_suffix(".png"), dpi=200)
    plt.close(fig)

# =============================================================================
# 2. GERENCIADOR DE PAINÉIS (BOILERPLATE DE SUBPLOTS)
# =============================================================================
def _configurar_paineis(x_lim_zoom, size_simples=(7.5, 4.8), size_duplo=(12.0, 4.8)):
    """Evita repetição de if/else para criar 1 ou 2 painéis."""
    if x_lim_zoom is not None:
        fig, eixos = plt.subplots(1, 2, figsize=size_duplo)
        return fig, eixos[0], eixos[1], True
    fig, ax = plt.subplots(figsize=size_simples)
    return fig, ax, None, False

# =============================================================================
# 3. PLOTAGENS BÁSICAS DE SOLUÇÃO
# =============================================================================
def _passo_marcadores(largura, k, marker_density=30):
    """Nº de pontos da malha entre marcadores para ~`marker_density` marcadores na largura do eixo."""
    dens = marker_density if (marker_density is not None and marker_density > 0) else 30
    return max(1, round(largura / (abs(k) * dens)))


def _desenhar(ax, prob, solucoes, ks, tspan, titulo, loc_legenda="best",
              xlim=None, ylim=None, marker_density=30, markersize=None, markevery=None,
              labels=None):
    # Amostra a solução exata estritamente na janela visível para manter alta resolução no zoom
    t_min_plot = xlim[0] if xlim is not None else tspan[0]
    t_max_plot = xlim[1] if xlim is not None else tspan[1]
    t_fino = np.linspace(t_min_plot, t_max_plot, 400)
    ax.plot(t_fino, prob.solucao(t_fino), label="solução exata", **ESTILO["exata"])

    n_ks = len(ks)
    tamanhos = np.linspace(5.5, 1.5, n_ks) if n_ks > 1 else [4.5]
    marcadores = itertools.cycle(MARCADORES_BASE)
    cores = ESTILO["cores_ciclo"]

    # Largura de referência (em t) sobre a qual a densidade é medida: o eixo visível.
    largura = (xlim[1] - xlim[0]) if xlim is not None else (tspan[1] - tspan[0])

    if markevery is not None:
        passos = [max(1, int(markevery))] * n_ks
    else:
        passos = [_passo_marcadores(largura, k, marker_density) for k in ks]

    for i, (sol, k, tam, marc, passo) in enumerate(
            zip(solucoes, ks, tamanhos, marcadores, passos)):
        t, U = sol[0], sol[1]
        stats = sol[2] if len(sol) > 2 else {}
        n = len(t) - 1
        inicio = (i * passo) // n_ks
        ms = markersize if markersize is not None else 4.2
        cor = cores[i % len(cores)]
        rotulo = labels[i] if (labels is not None and i < len(labels)) else f"$k = {k}$ ({n} passos)"
        
        # Garante a interpolação por linha conectando os pontos discretos
        ax.plot(t, U, linestyle="--", color=cor, marker=marc, ms=ms, lw=1.2,
                markevery=(inicio, passo), zorder=3, label=rotulo)

        if isinstance(stats, dict) and stats.get("motivo", "concluido") != "concluido" and len(t) > 0:
            ax.plot(t[-1], U[-1], marker="X", color="red", mec="black", ms=8.0, zorder=6)

    ax.axhline(0, color="gray", lw=0.8, zorder=1)
    ax.set(xlabel="$t$", ylabel="$y$", title=titulo)
    if xlim is not None:
        ax.set_xlim(*xlim)
    if ylim is not None:
        ax.set_ylim(*ylim)
    ax.legend(loc=loc_legenda)


def plot_fig122(prob, solucoes, ks, tspan, titulo, caminho, loc_legenda="best",
               xlim=None, ylim=None, zoom=None, marker_density=30, markersize=None, markevery=None):
    if zoom is not None and xlim is None:
        xlim = zoom
    fig, ax, _, _ = _configurar_paineis(None, size_simples=(6.5, 4.5))
    _desenhar(ax, prob, solucoes, ks, tspan, titulo, loc_legenda=loc_legenda,
              xlim=xlim, ylim=ylim, marker_density=marker_density,
              markersize=markersize, markevery=markevery)
    _salvar(fig, caminho)


def plot_comparacao(prob, sol1, sol2, ks, tspan, titulo1, titulo2, caminho, loc_legenda="best",
                    xlim=None, ylim=None, zoom=None, marker_density=30, markersize=None, markevery=None):
    if zoom is not None and xlim is None:
        xlim = zoom
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    _desenhar(ax1, prob, sol1, ks, tspan, titulo1, loc_legenda=loc_legenda,
              xlim=xlim, ylim=ylim, marker_density=marker_density,
              markersize=markersize, markevery=markevery)
    _desenhar(ax2, prob, sol2, ks, tspan, titulo2, loc_legenda=loc_legenda,
              xlim=xlim, ylim=ylim, marker_density=marker_density,
              markersize=markersize, markevery=markevery)
    ax2.set_ylabel("")
    _salvar(fig, caminho)


def _nome_metodo(m):
    """Retorna uma string descritiva amigável para um método numérico."""
    nomes = {
        "euler_explicito": "Euler avançado (explícito)",
        "euler_implicito": "Euler recuado (implícito)",
        "rk4": "Runge-Kutta de 4ª Ordem (RK4)",
        "adams_moulton": "Adams-Moulton de 2 passos",
    }
    nome = getattr(m, "__name__", str(m))
    return nomes.get(nome, nome)


def plot_k_fixo( prob, metodos, k, caminho,
    tf=None, solucoes=None, x_lim_zoom=None, y_lim_zoom=None, xlim=None, ylim=None, titulo=None,
    loc_legenda="best",marker_density=30, size_duplo=(12.0, 4.8), size_simples=(6.5, 4.5),
):
    if not isinstance(metodos, (list, tuple)):
        metodos = [metodos]

    # Prepara ou resolve as soluções
    if solucoes is None:
        if tf is None:
            raise ValueError("O parâmetro `tf` deve ser fornecido quando `solucoes` não for informada.")
        from pvi.uteis import resolver
        solucoes_list = [resolver(m, prob, k, tf) for m in metodos]
    else:
        # Garante que solucoes_list seja uma lista de tuplas (t, U, stats)
        if len(solucoes) == 3 and isinstance(solucoes[0], np.ndarray):
            solucoes_list = [solucoes]
        else:
            solucoes_list = list(solucoes)

    # Determina o tspan
    t_final = tf if tf is not None else float(solucoes_list[0][0][-1])
    tspan = (prob.t0, t_final)

    # Configuração dos rótulos
    nomes_metodos = [_nome_metodo(m) for m in metodos]
    if len(metodos) == 1:
        titulo_padrao = f"{nomes_metodos[0]} ($k = {k:g}$)"
        labels = [f"$k = {k:g}$ ({len(solucoes_list[0][0]) - 1} passos)"]
    else:
        titulo_padrao = f"Comparação de Métodos ($k = {k:g}$)"
        labels = [f"{nome} ({len(s[0]) - 1} passos)" for nome, s in zip(nomes_metodos, solucoes_list)]

    tit_fig = titulo if titulo is not None else titulo_padrao

    # Gerenciamento de 1 ou 2 painéis reaproveitando _configurar_paineis
    fig, ax1, ax2, is_duplo = _configurar_paineis(x_lim_zoom, size_simples=size_simples, size_duplo=size_duplo)

    ks_list = [k] * len(solucoes_list)

    # Painel 1: Visão Global
    tit_global = f"{tit_fig} — Visão Global" if is_duplo else tit_fig
    _desenhar(ax1, prob, solucoes_list, ks_list, tspan, tit_global,
              loc_legenda=loc_legenda, xlim=xlim, ylim=ylim,
              marker_density=marker_density, labels=labels)

    # Painel 2: Zoom ajustável (se solicitado)
    if is_duplo:
        tit_zoom = f"Detalhe / Zoom ($t \\in [{x_lim_zoom[0]:g},\\, {x_lim_zoom[1]:g}]$)"
        _desenhar(ax2, prob, solucoes_list, ks_list, tspan, tit_zoom,
                  loc_legenda=loc_legenda, xlim=x_lim_zoom, ylim=y_lim_zoom,
                  marker_density=marker_density, labels=labels)
        ax2.set_ylabel("")

    fig.tight_layout()
    _salvar(fig, caminho)

# =============================================================================
# 4. PLOTAGENS ASSINTÓTICAS E AUTOVALORES 
# =============================================================================
def plot_solucao_assintotas(prob, caminho, x_lim_global=(-5.0, 40.0), x_lim_zoom=(-1.5, 5.0)):
    fig, ax1, ax2, _ = _configurar_paineis(x_lim_zoom, size_duplo=(11.5, 4.8))

    def _desenhar_assintota(ax, xlim, is_zoom):
        x_left = np.linspace(xlim[0], -1.05, 500)
        x_right = np.linspace(-0.95, xlim[1], 1000)
        
        ax.plot(x_left, prob.solucao(x_left), label=r"Solução $y(x)$", **ESTILO["exata"])
        ax.plot(x_right, prob.solucao(x_right), **ESTILO["exata"])
        ax.plot(np.linspace(*xlim, 500), np.linspace(*xlim, 500) - 4.0, label=r"Assíntota oblíqua", **ESTILO["assintota_obl"])
        ax.axvline(-1.0, label=r"Assíntota vertical", **ESTILO["assintota_ver"])
        ax.plot(0.0, 2.0, label=r"$(0, 2)$", **ESTILO["cond_inicial"])
        
        if is_zoom:
            ax.plot([1.0, 2.0], [0.0, 0.0], label=r"Raízes", **ESTILO["raizes"])
            ax.axvspan(0.0, 1.6, color="#17becf", alpha=0.15, label=r"Intervalo $[0,\, 1{,}6]$")
            ax.set(xlim=xlim, ylim=(-8.0, 14.0), title=r"Detalhe Local ($x \in [-1{,}5,\, 5]$)")
        else:
            ax.set(xlim=(xlim[0]-1.0, xlim[1]+2.0), ylim=(-25.0, 45.0), title=r"Comportamento Global ($x \in [-5,\, 40]$)")
        
        ax.axhline(0, color="gray", lw=0.8, alpha=0.5)
        ax.set(xlabel=r"$x$", ylabel=r"$y$")
        ax.legend(fontsize=9.0)

    _desenhar_assintota(ax1, x_lim_global, False)
    _desenhar_assintota(ax2, x_lim_zoom, True)
    fig.tight_layout()
    _salvar(fig, caminho)

def _desenhar_autovalor(ax, prob, xlim, is_zoom=False):
    """Função única para autovalor, evitando repetição entre visão global e zoom."""
    x_min, lam_min = np.sqrt(6.0) - 1.0, 4.0 * np.sqrt(6.0) - 10.0
    x_max, lam_max = -1.0 - np.sqrt(6.0), -4.0 * np.sqrt(6.0) - 10.0

    x_left = np.linspace(xlim[0], -1.05, 500)
    x_right = np.linspace(-0.95, xlim[1], 1000)
    x_asint = np.linspace(*xlim, 500)

    ax.plot(x_left, 2.0 * prob.solucao(x_left), color="#1f77b4", lw=1.8, label=r"Autovalor $\lambda(x)$")
    ax.plot(x_right, 2.0 * prob.solucao(x_right), color="#1f77b4", lw=1.8)
    ax.plot(x_asint, 2.0 * x_asint - 8.0, label=r"Assíntota: $\lambda = 2x - 8$", **ESTILO["assintota_obl"])
    ax.axvline(-1.0, label=r"Assíntota: $x = -1$", **ESTILO["assintota_ver"])
    ax.plot(0.0, 4.0, "o", color="#9467bd", markersize=6, zorder=5, label=r"No zero: $(0,\, 4)$")
    ax.plot([1.0, 2.0], [0.0, 0.0], label=r"Raízes $x=1,\, 2$", **ESTILO["raizes"])
    ax.plot(x_min, lam_min, "v", color="#d62728", markersize=7, zorder=5)
    
    if is_zoom:
        ax.annotate(r"$\lambda(0) = 4$", xy=(0.0, 4.0), xytext=(8, 4), textcoords="offset points", fontweight="bold", color="#4a148c")
        ax.annotate(rf"$\lambda_{{\min}} \approx {lam_min:.3f}$", xy=(x_min, lam_min), xytext=(-20, -18), textcoords="offset points", fontweight="bold", color="#b71c1c", arrowprops=dict(arrowstyle="->", color="#b71c1c"))
        ax.axvspan(0.0, 1.6, color="#17becf", alpha=0.15, label=r"Intervalo $[0,\, 1{,}6]$")
        ax.set(xlim=xlim, ylim=(-8.0, 16.0), title=r"Detalhe Local do Autovalor ($x \in [-1{,}5,\, 5]$)")
    else:
        ax.plot(x_max, lam_max, "^", color="#8c564b", markersize=6, zorder=5, label="Máximo local")
        ax.set(xlim=(xlim[0]-1.0, xlim[1]+2.0), ylim=(-45.0, 85.0), title=r"Comportamento Global do Autovalor")

    ax.axhline(0, color="gray", lw=0.8, alpha=0.5)
    ax.set(xlabel=r"$x$", ylabel=r"$\lambda(x)$")
    ax.legend(fontsize=8.8)

def plot_autovalor_assintotas(prob, caminho, x_lim_global=(-5.0, 40.0), x_lim_zoom=(-1.5, 5.0)):
    fig, ax1, ax2, _ = _configurar_paineis(x_lim_zoom, size_duplo=(11.5, 4.8))
    _desenhar_autovalor(ax1, prob, x_lim_global, False)
    _desenhar_autovalor(ax2, prob, x_lim_zoom, True)
    fig.tight_layout()
    _salvar(fig, caminho)

# =============================================================================
# 5. DISCRIMINANTE: SEPARAÇÃO ENTRE MATEMÁTICA E VIEW
# =============================================================================

def _desenhar_discriminante(ax, prob, ks, tf, g_func, t_ref, metodo, mostrar_legenda, loc_legenda, anotar_falhas=False):
    ax.axhspan(-0.25, 0.0, color="#d62728", alpha=0.06, zorder=0)
    ax.axhline(0.0, color="black", linestyle="--", lw=1.1, alpha=0.85, label=r"Limiar crítico $\Delta = 0$")

    is_am = metodo if isinstance(metodo, bool) else (str(metodo).lower() in ("adams_moulton", "am2", "am"))
    cores = ESTILO["cores_ciclo"]

    def f_exato(t_val): return prob.solucao(t_val)**2 - g_func(t_val)

    falha_rotulada = False

    for idx, k in enumerate(ks):
        cor = cores[idx % len(cores)]
        t_teor = t_ref[t_ref + k <= tf + 1e-9]

        # Trajetória Teórica Contínua (por baixo das soluções numéricas)
        if not is_am:
            c_teor = prob.solucao(t_teor) - k * g_func(t_teor + k)
            delta_teor = 1.0 - 4.0 * k * c_teor
        else:
            c_teor = prob.solucao(t_teor) + (k / 12.0) * (8.0 * f_exato(t_teor) - f_exato(t_teor - k) - 5.0 * g_func(t_teor + k))
            delta_teor = 1.0 - (5.0 * k / 3.0) * c_teor
        
        ax.plot(t_teor + k, delta_teor, "-", color=cor, lw=1.5, zorder=2, label=f"Exata ($k = {k}$)")

        # Dados Simulados (Delegação para o Motor Matemático)
        n_passos = int(round(tf / k))
        dados, _, _ = calcular_evolucao_discriminante(prob, k, n_passos, metodo=metodo, g_func=g_func)
        t_destinos = [d["tn1"] for d in dados if not np.isnan(d["delta_num"])]
        deltas_num = [d["delta_num"] for d in dados if not np.isnan(d["delta_num"])]

        markevery = max(1, len(t_destinos) // 20)
        ax.plot(t_destinos, deltas_num, "o--", color=cor, ms=3.8, lw=1.2, markevery=markevery, alpha=0.85, zorder=3, label=f"Simulada ($k = {k}$)")

        # Ponto de falha (apenas o símbolo X, sem anotação textual, com rótulo único na legenda)
        if len(deltas_num) > 0 and deltas_num[-1] < 0:
            t_f, d_f = t_destinos[-1], deltas_num[-1]
            lbl_falha = r"Falha ($\Delta < 0$)" if not falha_rotulada else None
            ax.plot(t_f, d_f, "X", color="#8b0000", ms=8.5, markeredgecolor="black", zorder=6, label=lbl_falha)
            falha_rotulada = True

    ax.set(xlabel=r"$t_{n+1}$", ylabel=r"Discriminante $\Delta$")
    if mostrar_legenda: ax.legend(loc=loc_legenda, fontsize=8.2, ncol=2)

def plot_discriminante(prob, ks, tf, caminho, metodo="euler", g_func=None, x_lim_zoom=None, loc_legenda="lower left", titulo=None):
    if g_func is None:
        from pvi.problemas import g as g_func

    t_ref = np.linspace(prob.t0, tf, 500)
    fig, ax1, ax2, is_duplo = _configurar_paineis(x_lim_zoom, size_duplo=(12.0, 4.8))

    titulo_geral = titulo or ("Adams-Moulton" if "am" in str(metodo).lower() else "Euler Implícito")

    _desenhar_discriminante(ax1, prob, ks, tf, g_func, t_ref, metodo, True, loc_legenda, False)
    ax1.set(xlim=(prob.t0 - 0.05, tf + 0.05), ylim=(-0.18, 1.10), title=rf"Visão Global ($t \in [{prob.t0:g},\, {tf:g}]$)" if is_duplo else titulo_geral)

    if is_duplo:
        _desenhar_discriminante(ax2, prob, ks, tf, g_func, t_ref, metodo, False, None, False)
        ax2.set(xlim=x_lim_zoom, ylim=(-0.15, 1.10), ylabel="", title=rf"Detalhe da Região Crítica")

    fig.tight_layout()
    _salvar(fig, caminho)

# Atalhos
def plot_discriminante_euler(prob, ks, tf, caminho, **kwargs):
    plot_discriminante(prob, ks, tf, caminho, metodo="euler", **kwargs)

def plot_discriminante_adams_moulton(prob, ks, tf, caminho, **kwargs):
    plot_discriminante(prob, ks, tf, caminho, metodo="adams_moulton", **kwargs)

def plot_discriminante_comparacao(prob, ks, tf, caminho, g_func=None, loc_legenda="lower left"):
    """
    Gera um gráfico comparativo lado a lado dos discriminantes:
    - Painel 1 (Esquerda): Euler Implícito (Delta = 1 - 4k c_n, limiar c_n <= 0.25 / k)
    - Painel 2 (Direita): Adams-Moulton 2 (Delta = 1 - (5k/3) c_til_n, limiar c_til_n <= 0.60 / k)
    """
    if g_func is None:
        from pvi.problemas import g as g_func

    t_ref = np.linspace(prob.t0, tf, 500)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.0, 4.8))

    _desenhar_discriminante(ax1, prob, ks, tf, g_func, t_ref, "euler", True, loc_legenda, False)
    ax1.set(xlim=(prob.t0 - 0.05, tf + 0.05), ylim=(-0.18, 1.10),
            title=r"Euler Implícito: $\Delta_n = 1 - 4k c_n$ ($c_n \leq \frac{0.25}{k}$)")

    _desenhar_discriminante(ax2, prob, ks, tf, g_func, t_ref, "adams_moulton", True, loc_legenda, False)
    ax2.set(xlim=(prob.t0 - 0.05, tf + 0.05), ylim=(-0.18, 1.10), ylabel="",
            title=r"Adams-Moulton 2: $\Delta_n = 1 - \frac{5k}{3}\tilde{c}_n$ ($\tilde{c}_n \leq \frac{0.60}{k}$)")

    fig.tight_layout()
    _salvar(fig, caminho)

# =============================================================================
# 6. PLOTAGEM DE ISÓCLINAS
# =============================================================================
def _desenhar_isoclinas(ax, prob, solucoes, ks, tf, g_func, mostrar_legenda, destacar_inversao, xlim, ylim, loc_legenda="lower left"):
    t_fino = np.linspace(prob.t0, tf, 1200)
    g_vals = g_func(t_fino)
    mask_pos = g_vals >= 0.0
    raiz_g = np.sqrt(np.maximum(g_vals, 0.0))

    ax.fill_between(t_fino, -raiz_g, raiz_g, where=mask_pos, label=r"Zona de descida ($y' < 0$)", **ESTILO["zona_descida"])
    ax.plot(t_fino, np.where(mask_pos, raiz_g, np.nan), label=r"Isóclina repulsora", **ESTILO["isoclina_rep"])
    ax.plot(t_fino, np.where(mask_pos, -raiz_g, np.nan), label=r"Isóclina atratora", **ESTILO["isoclina_atr"])
    ax.plot(t_fino, prob.solucao(t_fino), label=r"Solução exata $y(t)$", **ESTILO["exata"])

    marcadores = itertools.cycle(MARCADORES_BASE)
    cores = ESTILO["cores_ciclo"]
    rotulado = False

    for idx, ((t, U, _), k, marc) in enumerate(zip(solucoes, ks, marcadores)):
        cor = cores[idx % len(cores)]
        markevery = max(1, len(t) // 22)
        ax.plot(t, U, linestyle="-.", marker=marc, color=cor, ms=4.2, lw=1.2, markevery=markevery, zorder=5, label=f"$k = {k}$")

        if destacar_inversao and len(t) > 5:
            mask_t = t > 2.5
            if np.any(mask_t):
                idx_pico = np.where(mask_t)[0][np.argmax(U[mask_t])]
                if idx_pico < len(t) - 1 and U[idx_pico] > U[-1]:
                    ax.plot(t[idx_pico], U[idx_pico], "D", color="#ffd700", markeredgecolor="black", ms=6.8, zorder=7, label=r"Inversão" if not rotulado else None)
                    rotulado = True

    ax.axhline(0.0, color="gray", lw=0.8, alpha=0.5)
    ax.set(xlabel=r"$t$", ylabel=r"$y$", xlim=xlim, ylim=ylim)
    if mostrar_legenda: ax.legend(loc=loc_legenda, fontsize=8.0, ncol=2)

def plot_isoclinas(prob, solucoes, ks, tf, caminho, titulo="Análise de Isóclinas", g_func=None, x_lim_zoom=None, ylim=(-2.1, 2.3), ylim_zoom=(-1.9, 2.1), loc_legenda="lower left"):
    if g_func is None: from pvi.problemas import g as g_func

    if callable(solucoes):
        from pvi.uteis import resolver
        solucoes = [resolver(solucoes, prob, k, tf) for k in ks]

    fig, ax1, ax2, is_duplo = _configurar_paineis(x_lim_zoom, size_duplo=(12.2, 4.9))

    _desenhar_isoclinas(ax1, prob, solucoes, ks, tf, g_func, True, True, (prob.t0, tf), ylim, loc_legenda=loc_legenda)
    ax1.set_title(rf"{titulo} — Visão Global")

    if is_duplo:
        _desenhar_isoclinas(ax2, prob, solucoes, ks, tf, g_func, False, True, x_lim_zoom, ylim_zoom, loc_legenda=loc_legenda)
        ax2.set(ylabel="", title="Detalhe do Cruzamento da Isóclina")

    fig.tight_layout()
    _salvar(fig, caminho)


# =============================================================================
# 7. ITEM D: INTERVALOS QUE CONTÊM A SINGULARIDADE t = -1
# =============================================================================
def _solucao_exata_por_ramos(prob, a, b, polo=-1.0, n=3000, folga=1e-3):
    """Amostra a solução exata em [a, b] inserindo NaN no polo para não ligar os ramos."""
    t = np.linspace(a, b, n)
    with np.errstate(divide="ignore", invalid="ignore"):
        y = np.asarray(prob.solucao(t), dtype=float)
    y[np.abs(t - polo) < folga] = np.nan
    return t, y


def plot_singularidade(prob_ref, paineis, ks, intervalo, caminho, titulo, ylim,
                       polo=-1.0, marker_density=25):
    """Grade 2x2 (um painel por método) para um intervalo que contém o polo.

    `paineis`: dict {titulo_do_painel: [caso, ...]}, onde cada caso é um dict com
    'sol' = (t, U, stats), 'k' e 'prob' (o PVI usado, para marcar a condição inicial).
    A cor/marcador identifica |k|; os dois lados do polo são PVIs distintos.
    """
    a, b = intervalo
    largura = b - a
    ks_abs = [abs(k) for k in ks]
    cores = ESTILO["cores_ciclo"]

    fig, eixos = plt.subplots(2, 2, figsize=(12.0, 8.2), sharex=True, sharey=True)
    t_ex, y_ex = _solucao_exata_por_ramos(prob_ref, a, b, polo)

    for ax, (titulo_painel, casos) in zip(eixos.flat, paineis.items()):
        ax.axvline(polo, **ESTILO["assintota_ver"], zorder=1)
        ax.axhline(0, color="gray", lw=0.8, zorder=1)
        ax.plot(t_ex, y_ex, **ESTILO["exata"])

        cis = set()
        for caso in casos:
            t, U, stats = caso["sol"]
            idx = ks_abs.index(abs(caso["k"]))
            cor, marc = cores[idx % len(cores)], MARCADORES_BASE[idx % len(MARCADORES_BASE)]
            passo = _passo_marcadores(largura, caso["k"], marker_density)
            ax.plot(t, U, "--", color=cor, marker=marc, ms=4.0, lw=1.2,
                    markevery=(0, passo), zorder=3)
            # Ponto onde a integração parou (antes do instante final pedido)
            if stats.get("motivo", "concluido") != "concluido":
                ax.plot(t[-1], U[-1], "X", color=cor, mec="k", ms=8, zorder=6)
            cis.add((caso["prob"].t0, caso["prob"].y0))

        for t0, y0 in cis:
            ax.plot(t0, y0, **ESTILO["cond_inicial"])

        ax.set(title=titulo_painel, xlim=(a, b), ylim=ylim)

    for ax in eixos[1, :]:
        ax.set_xlabel("$t$")
    for ax in eixos[:, 0]:
        ax.set_ylabel("$y$")

    # Legenda única para a figura
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], **ESTILO["exata"], label="solução exata"),
               Line2D([], [], **ESTILO["assintota_ver"], label=f"polo $t = {polo:g}$"),
               Line2D([], [], linestyle="", **ESTILO["cond_inicial"], label="condição inicial")]
    handles += [Line2D([], [], linestyle="--", color=cores[i % len(cores)],
                       marker=MARCADORES_BASE[i % len(MARCADORES_BASE)], ms=4.0, lw=1.2,
                       label=f"$|k| = {k:g}$") for i, k in enumerate(ks_abs)]
    handles.append(Line2D([], [], linestyle="", marker="X", color="w", mec="k", ms=8,
                          label="parada antecipada"))
    fig.legend(handles=handles, loc="lower center", ncol=len(handles), fontsize=9.5,
               bbox_to_anchor=(0.5, -0.005))
    fig.suptitle(titulo, fontsize=13)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    _salvar(fig, caminho)



# =============================================================================
# 7. ITEM D: INTERVALOS QUE CONTÊM A SINGULARIDADE t = -1
# =============================================================================
def _solucao_exata_por_ramos(prob, a, b, polo=-1.0, n=3000, folga=1e-3):
    """Amostra a solução exata em [a, b] inserindo NaN no polo para não ligar os ramos."""
    t = np.linspace(a, b, n)
    with np.errstate(divide="ignore", invalid="ignore"):
        y = np.asarray(prob.solucao(t), dtype=float)
    y[np.abs(t - polo) < folga] = np.nan
    return t, y


def plot_singularidade(prob_ref, paineis, ks, intervalo, caminho, titulo, ylim,
                       polo=-1.0, marker_density=25):
    """Grade 2x2 (um painel por método) para um intervalo que contém o polo.

    `paineis`: dict {titulo_do_painel: [caso, ...]}, onde cada caso é um dict com
    'sol' = (t, U, stats), 'k' e 'prob' (o PVI usado, para marcar a condição inicial).
    A cor/marcador identifica |k|; os dois lados do polo são PVIs distintos.
    """
    a, b = intervalo
    largura = b - a
    ks_abs = [abs(k) for k in ks]
    cores = ESTILO["cores_ciclo"]

    fig, eixos = plt.subplots(2, 2, figsize=(12.0, 8.2), sharex=True, sharey=True)
    t_ex, y_ex = _solucao_exata_por_ramos(prob_ref, a, b, polo)

    for ax, (titulo_painel, casos) in zip(eixos.flat, paineis.items()):
        ax.axvline(polo, **ESTILO["assintota_ver"], zorder=1)
        ax.axhline(0, color="gray", lw=0.8, zorder=1)
        ax.plot(t_ex, y_ex, **ESTILO["exata"])

        cis = set()
        for caso in casos:
            t, U, stats = caso["sol"]
            idx = ks_abs.index(abs(caso["k"]))
            cor, marc = cores[idx % len(cores)], MARCADORES_BASE[idx % len(MARCADORES_BASE)]
            passo = _passo_marcadores(largura, caso["k"], marker_density)
            ax.plot(t, U, "--", color=cor, marker=marc, ms=4.0, lw=1.2,
                    markevery=(0, passo), zorder=3)
            # Ponto onde a integração parou (antes do instante final pedido)
            if stats.get("motivo", "concluido") != "concluido":
                ax.plot(t[-1], U[-1], "X", color=cor, mec="k", ms=8, zorder=6)
            cis.add((caso["prob"].t0, caso["prob"].y0))

        for t0, y0 in cis:
            ax.plot(t0, y0, **ESTILO["cond_inicial"])

        ax.set(title=titulo_painel, xlim=(a, b), ylim=ylim)

    for ax in eixos[1, :]:
        ax.set_xlabel("$t$")
    for ax in eixos[:, 0]:
        ax.set_ylabel("$y$")

    # Legenda única para a figura
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], **ESTILO["exata"], label="solução exata"),
               Line2D([], [], **ESTILO["assintota_ver"], label=f"polo $t = {polo:g}$"),
               Line2D([], [], linestyle="", **ESTILO["cond_inicial"], label="condição inicial")]
    handles += [Line2D([], [], linestyle="--", color=cores[i % len(cores)],
                       marker=MARCADORES_BASE[i % len(MARCADORES_BASE)], ms=4.0, lw=1.2,
                       label=f"$|k| = {k:g}$") for i, k in enumerate(ks_abs)]
    handles.append(Line2D([], [], linestyle="", marker="X", color="w", mec="k", ms=8,
                          label="parada antecipada"))
    fig.legend(handles=handles, loc="lower center", ncol=len(handles), fontsize=9.5,
               bbox_to_anchor=(0.5, -0.005))
    fig.suptitle(titulo, fontsize=13)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    _salvar(fig, caminho)