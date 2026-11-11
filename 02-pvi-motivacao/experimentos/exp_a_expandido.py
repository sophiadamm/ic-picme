import sys
import os

# Garante que o Python encontre a pasta 'src' ao rodar o script de dentro de 'experimentos/'
DIR_ATUAL = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(DIR_ATUAL, '..', 'src')))

import matplotlib
matplotlib.use("Agg")

from pvi.problemas import motivacao, g
from pvi.metodos import euler_explicito, euler_implicito
from pvi.plotagem import (
    configurar_estilo,
    plot_fig122,
    plot_isoclinas,
    plot_discriminante_euler,
)
from pvi.uteis import resolver, tabela_erros, diagnosticar_cruzamento_isoclina, exportar_tabela_discriminante_tex

# ----------------------------- parâmetros ---------------------------------
TF = 5.0
K = (0.2, 0.1, 0.05)
K_REFINADO = (0.0125, 0.00625, 0.003125, 0.0015625)
K_TABELA = (0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625, 0.003125, 0.0015625, 0.00078125, 0.000390625)
PASTA_ITEM = os.path.abspath(os.path.join(DIR_ATUAL, '..', 'resultados', 'item_a'))
PASTA_FIG = os.path.join(PASTA_ITEM, 'figuras')
PASTA_TAB = os.path.join(PASTA_ITEM, 'tabelas')
PASTA_DADOS = os.path.join(PASTA_ITEM, 'dados')
# ---------------------------------------------------------------------------


def executar():
    configurar_estilo()
    prob = motivacao()
    tspan = (prob.t0, TF)

    print(f"=== Executando Experimento A (Intervalo Expandido: [0, {TF}]) ===")

    # 1. Resolução para todos os passos da tabela no intervalo estendido
    sol_exp_tab = [resolver(euler_explicito, prob, k, TF) for k in K_TABELA]
    sol_imp_tab = [resolver(euler_implicito, prob, k, TF) for k in K_TABELA]

    # 2. Seleção das soluções dos passos clássicos e refinados
    sol_exp_1 = sol_exp_tab[:len(K)]
    sol_imp_1 = sol_imp_tab[:len(K)]

    sol_exp_2 = sol_exp_tab[4:8]
    sol_imp_2 = sol_imp_tab[4:8]

    # 3. Gráficos de trajetórias no intervalo estendido [0, 5]
    plot_fig122(prob, sol_exp_1, K, tspan,
                "Euler avançado (explícito)", f"{PASTA_FIG}/a_euler_avancadoT5")
    plot_fig122(prob, sol_imp_1, K, tspan,
                "Euler recuado (implícito)", f"{PASTA_FIG}/a_euler_recuadoT5")
    plot_fig122(prob, sol_exp_2, K_REFINADO, tspan,
                "Euler avançado (explícito)", f"{PASTA_FIG}/a_euler_avancadoT5_ref")
    plot_fig122(prob, sol_imp_2, K_REFINADO, tspan,
                "Euler recuado (implícito)", f"{PASTA_FIG}/a_euler_recuadoT5_ref")

    # Gráficos da malha mais fina isolada (k = 0.000390625)
    k_fixo = K_TABELA[-1]
    plot_fig122(prob, [sol_exp_tab[-1]], (k_fixo,), tspan,
                f"Euler avançado (explícito, k = {k_fixo})", f"{PASTA_FIG}/a_euler_avancado_refinado")
    plot_fig122(prob, [sol_imp_tab[-1]], (k_fixo,), tspan,
                f"Euler recuado (implícito, k = {k_fixo})", f"{PASTA_FIG}/a_euler_recuado_refinado")

    # 4. Gráficos de Isóclinas e diagnóstico de cruzamento em [0, 5]
    plot_isoclinas(
        prob,
        euler_explicito,
        K,
        TF,
        f"{PASTA_FIG}/a_isoclinas_eulerT5",
        titulo="Euler Avançado",
        g_func=g,
        x_lim_zoom=(3.0, 5.0),
    )
    plot_isoclinas(
        prob,
        euler_explicito,
        K_REFINADO,
        TF,
        f"{PASTA_FIG}/a_isoclinas_eulerT5_refinado",
        titulo="Euler Avançado (Refinado)",
        g_func=g,
        x_lim_zoom=(3.2, 5.0),
    )
    diagnosticar_cruzamento_isoclina(prob, euler_explicito, K + K_REFINADO, tf=TF)

    # 5. Gráficos de Discriminante do Euler recuado em [0, 5]
    plot_discriminante_euler(prob, K, TF, f"{PASTA_FIG}/a_discriminante_eulerT5", g_func=g)
    plot_discriminante_euler(prob, K_REFINADO, TF, f"{PASTA_FIG}/a_discriminante_eulerT5_ref", g_func=g, x_lim_zoom=(3.8, 5.02))

    # 6. Tabelas de erro computacional em [0, 5]
    tabela_erros(prob, "Euler avançado, TF = 5", sol_exp_tab, K_TABELA, pasta_tab=PASTA_TAB, pasta_dados=PASTA_DADOS)
    tabela_erros(prob, "Euler recuado, TF = 5", sol_imp_tab, K_TABELA, pasta_tab=PASTA_TAB, pasta_dados=PASTA_DADOS)

    print("Experimento expandido concluído com sucesso!")


if __name__ == "__main__":
    executar()
