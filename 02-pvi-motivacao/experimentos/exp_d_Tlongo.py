import os
import sys

# Garante que o Python encontre a pasta 'src' e a própria pasta 'experimentos'
DIR_ATUAL = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(DIR_ATUAL, '..', 'src')))
if DIR_ATUAL not in sys.path:
    sys.path.append(DIR_ATUAL)

import matplotlib
matplotlib.use("Agg")

from pvi.problemas import motivacao
from pvi.metodos import euler_explicito, euler_implicito, rk4, adams_moulton
from pvi.plotagem import (
    configurar_estilo,
    plot_fig122,
    plot_k_fixo,
)
from pvi.uteis import resolver, erro_max

# ----------------------------- parâmetros ---------------------------------
T = 40.0
# Malhas:
#  - 0.2 e 0.000390625: malhas clássicas para as figuras 122 e estudo de oscilação
#  - 1e-5: hiper-refinamento intermediário (N = 4 * 10^6 passos)
#  - 4e-6: hiper-refinamento limite (N = 10^7 passos)
K = (0.2, 0.000390625, 1e-5, 4e-6)

K_PLOTS = (0.2, 0.000390625)   # Passos exibidos nas Figuras 122
K_FIXO = 0.2                    # Passo para o estudo da ruptura por oscilação
K_LIMITES = (1e-5, 4e-6)        # Passos limites de máquina consolidados na tabela LaTeX

PASTA_ITEM = os.path.abspath(os.path.join(DIR_ATUAL, '..', 'resultados', 'item_d'))
PASTA_FIG = os.path.join(PASTA_ITEM, 'figuras')
PASTA_TAB = os.path.join(PASTA_ITEM, 'tabelas')
PASTA_DADOS = os.path.join(PASTA_ITEM, 'dados')

# Janelas de visualização.
XLIM_EXP, YLIM_EXP = (0.0, T), (-48.0, 45.0)
XLIM_IMP, YLIM_IMP = (0.0, 10.0), (0.0, 30.0)
DENS_EXP, DENS_IMP = 20, 15
# ---------------------------------------------------------------------------


def gerar_relatorio_e_tabela_latex(prob, mapa_solucoes, k_valores, pasta_tab, pasta_dados):
    """
    Gera o relatório final de limites de máquina, exporta diretamente para tabela LaTeX
    e CSV, e imprime no terminal a visualização formatada.
    """
    os.makedirs(pasta_tab, exist_ok=True)
    os.makedirs(pasta_dados, exist_ok=True)

    caminho_tex = os.path.join(pasta_tab, "tabela_limites_refinamento.tex")
    caminho_csv = os.path.join(pasta_dados, "tabela_limites_refinamento.csv")

    linhas = []
    for k in k_valores:
        idx = K.index(k)
        for nome, lista_sols in mapa_solucoes.items():
            t, U, stats = lista_sols[idx]
            passos = len(t) - 1
            t_fim = t[-1] if len(t) > 0 else 0.0
            cpu_seg = stats.get('runtime', 0.0)
            cpu_ms = cpu_seg * 1000.0
            motivo = stats.get('motivo', 'concluido')
            e_max = erro_max(prob, t, U) if len(t) > 0 else float('nan')

            linhas.append({
                "metodo": nome,
                "k": f"{k:g}",
                "passos": passos,
                "tf": f"{t_fim:.3f}",
                "status": motivo,
                "cpu_s": f"{cpu_seg:.2f}",
                "cpu_ms": f"{cpu_ms:.1f}",
                "nfev": stats.get('nfev', 0),
                "erro": f"{e_max:.3e}",
                "raw": (nome, k, motivo, passos, t_fim, cpu_seg, e_max)
            })

    # 1. Impressão formatada no terminal
    print("\n" + "=" * 96)
    print(f"{'RELATÓRIO FINAL: LIMITES DE REFINAMENTO DA MÁQUINA (T = 40)':^96}")
    print("=" * 96)
    print(f"{'Método':<26} | {'Passo k':<8} | {'Status':<12} | {'Passos':>9} | {'t_fim':>7} | {'CPU (s)':>8} | {'Erro Máx':>12}")
    print("-" * 96)

    k_anterior = None
    for item in linhas:
        nome, k, motivo, passos, t_fim, cpu_seg, e_max = item["raw"]
        if k_anterior is not None and k != k_anterior:
            print("-" * 96)
        k_anterior = k
        print(f"{nome:<26} | {k:<8g} | {motivo:<12} | {passos:>9d} | {t_fim:>7.3f} | {cpu_seg:>8.2f} | {e_max:>12.4e}")

    print("=" * 96)

    # 2. Exportação em LaTeX (booktabs, ideal para publicação)
    with open(caminho_tex, "w", encoding="utf-8") as f:
        f.write("% Tabela gerada automaticamente por exp_d_Tlongo.py\n")
        f.write("\\begin{table}[H]\n")
        f.write("    \\centering\n")
        f.write("    \\caption{Comparação de desempenho e limites de máquina para passos hiper-refinados ($T = 40$).}\n")
        f.write("    \\label{tab:d_limites_refinamento}\n")
        f.write("    \\resizebox{\\textwidth}{!}{%\n")
        f.write("    \\begin{tabular}{lccccccc}\n")
        f.write("        \\toprule\n")
        f.write("        \\textbf{Método} & \\textbf{Passo $k$} & \\textbf{Passos $N$} & \\textbf{$t_{\\text{parada}}$} & \\textbf{Status} & \\textbf{NFEV} & \\textbf{CPU (s)} & \\textbf{Erro Máximo} \\\\\n")
        f.write("        \\midrule\n")

        k_atual = None
        for item in linhas:
            if k_atual is not None and item["k"] != k_atual:
                f.write("        \\midrule\n")
            k_atual = item["k"]
            f.write(f"        {item['metodo']} & {item['k']} & {item['passos']:,d} & {item['tf']} & {item['status']} & {item['nfev']:,d} & {item['cpu_s']} & {item['erro']} \\\\\n")

        f.write("        \\bottomrule\n")
        f.write("    \\end{tabular}%\n")
        f.write("    }\n")
        f.write("\\end{table}\n")

    # 3. Exportação em CSV
    with open(caminho_csv, "w", encoding="utf-8") as f:
        f.write("metodo,k,passos,t_parada,status,nfev,cpu_s,cpu_ms,erro_max\n")
        for item in linhas:
            f.write(f"{item['metodo']},{item['k']},{item['passos']},{item['tf']},{item['status']},{item['nfev']},{item['cpu_s']},{item['cpu_ms']},{item['erro']}\n")

    print(f"\n-> Tabela LaTeX salva com sucesso em:")
    print(f"   [LaTeX] {caminho_tex}")
    print(f"   [CSV]   {caminho_csv}")


def executar():
    configurar_estilo()
    prob = motivacao()
    tspan = (prob.t0, T)

    print(f"=== Executando Experimento D (Intervalo: [0, {T}]) ===")
    print(f"Passos avaliados: K = {K}")
    print(f"Passos limites consolidados na tabela: {K_LIMITES}")

    # 1. Resoluções numéricas para todos os passos
    print("\n1. Resolvendo equações diferenciais...")
    print("  -> Euler explícito...")
    sol_exp = [resolver(euler_explicito, prob, k, T) for k in K]

    print("  -> Euler implícito...")
    sol_imp = [resolver(euler_implicito, prob, k, T) for k in K]

    print("  -> Runge-Kutta 4...")
    sol_rk4 = [resolver(rk4, prob, k, T) for k in K]

    print("  -> Adams-Moulton 2...")
    sol_am = [resolver(adams_moulton, prob, k, T) for k in K]

    mapa_solucoes = {
        "Euler avançado": sol_exp,
        "Euler recuado": sol_imp,
        "Runge-Kutta 4": sol_rk4,
        "Adams-Moulton 2": sol_am,
    }

    # 2. Gráficos de trajetória com o padrão plot 122 (apenas K_PLOTS = (0.2, 0.000390625))
    print("\n2. Gerando gráficos de trajetória (Figuras 122)...")
    plot_fig122(
        prob, sol_exp[:2], K_PLOTS, tspan,
        "Euler avançado (explícito)",
        f"{PASTA_FIG}/d_euler_avancado",
        xlim=XLIM_EXP, ylim=YLIM_EXP,
        loc_legenda="upper left",
    )

    plot_fig122(
        prob, sol_imp[:2], K_PLOTS, tspan,
        "Euler recuado (implícito)",
        f"{PASTA_FIG}/d_euler_recuado",
        xlim=XLIM_IMP, ylim=YLIM_IMP,
        loc_legenda="upper right",
    )

    plot_fig122(
        prob, sol_rk4[:2], K_PLOTS, tspan,
        "Runge-Kutta de 4ª Ordem (RK4)",
        f"{PASTA_FIG}/d_rk4",
        xlim=XLIM_EXP, ylim=YLIM_EXP,
        marker_density=DENS_EXP,
        loc_legenda="upper left",
    )

    plot_fig122(
        prob, sol_am[:2], K_PLOTS, tspan,
        "Adams-Moulton de 2 passos",
        f"{PASTA_FIG}/d_adams_moulton",
        xlim=XLIM_IMP, ylim=YLIM_IMP,
        loc_legenda="upper right",
    )

    # 3. Gráficos com passo fixo
    print(f"\n3. Gerando gráficos de passo fixo...")
    # 3.1. Ruptura por oscilação em k = 0.2 (Seção 4.2.1 do relatório)
    plot_k_fixo(
        prob=prob,
        metodos=(euler_explicito, rk4),
        k=K_FIXO,
        tf=T,
        solucoes=(sol_exp[0], sol_rk4[0]),
        caminho=f"{PASTA_FIG}/d_explicitos_k02_T40",
        xlim=(0, 20),
        ylim=(-25, 25),
        marker_density=DENS_EXP,
        loc_legenda='upper left',
    )

    # 3.2. Gráficos de passo fixo para os passos hiper-refinados (1e-5 e 4e-6)
    for k_lim in K_LIMITES:
        idx_lim = K.index(k_lim)
        tag = "k1e5" if k_lim == 1e-5 else "k4e6"

        print(f"  -> Gerando gráficos comparativos para k = {k_lim:g} ({tag})...")

        # Explícitos (Euler avançado e RK4)
        plot_k_fixo(
            prob=prob,
            metodos=(euler_explicito, rk4),
            k=k_lim,
            tf=T,
            solucoes=(sol_exp[idx_lim], sol_rk4[idx_lim]),
            caminho=f"{PASTA_FIG}/d_explicitos_{tag}",
            xlim=(0, 40),
            ylim=(-40, 40),
            marker_density=DENS_EXP,
            loc_legenda='upper right',
        )

        # Implícitos (Adams-Moulton 2 e Euler recuado)
        plot_k_fixo(
            prob=prob,
            metodos=(adams_moulton, euler_implicito),
            k=k_lim,
            tf=T,
            solucoes=(sol_am[idx_lim], sol_imp[idx_lim]),
            caminho=f"{PASTA_FIG}/d_implicitos_{tag}",
            xlim=(0, 40),
            ylim=(-10, 40),
            marker_density=DENS_EXP,
            loc_legenda='upper right',
        )

    # Mantém também os nomes canônicos d_explicitos_k_limite para o menor passo (4e-6)
    plot_k_fixo(
        prob=prob,
        metodos=(euler_explicito, rk4),
        k=K[-1],
        tf=T,
        solucoes=(sol_exp[-1], sol_rk4[-1]),
        caminho=f"{PASTA_FIG}/d_explicitos_k_limite",
        xlim=(0, 40),
        ylim=(-10, 80),
        marker_density=DENS_EXP,
        loc_legenda='upper right',
    )

    plot_k_fixo(
        prob=prob,
        metodos=(adams_moulton, euler_implicito),
        k=K[-1],
        tf=T,
        solucoes=(sol_am[-1], sol_imp[-1]),
        caminho=f"{PASTA_FIG}/d_implicitos_k_limite",
        xlim=(0, 40),
        ylim=(-10, 80),
        marker_density=DENS_EXP,
        loc_legenda='upper right',
    )

    # 4. Relatório final e Tabela LaTeX consolidada de limites de máquina
    # (As tabelas individuais erros_euler_avancado etc. não são geradas aqui para preservar as tabelas clássicas)
    print("\n4. Gerando relatório final e exportando tabela LaTeX...")
    gerar_relatorio_e_tabela_latex(prob, mapa_solucoes, K_LIMITES, PASTA_TAB, PASTA_DADOS)

    print("\nExperimento D concluído com sucesso!")


if __name__ == "__main__":
    executar()
